import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import matplotlib.pyplot as plt
import networkx as nx
import time
# Algorithm 1 in the paper, which is used in Algorithm 4
def SpectralGraphPartitioning(W, K):
    W_rowsum = W.sum(axis=1)
    Z = W / np.sqrt(np.outer(W_rowsum, W_rowsum)) # Step 1, Compute Z
    eigen_value, eigen_vector = np.linalg.eig(Z)
    top_index = eigen_value.argsort()[::-1][0:K]
    out_matrix = eigen_vector[:, top_index]       # Step 2, Extract the top K eigenvectors of Z
    out_matrix = out_matrix / np.c_[np.linalg.norm(out_matrix, axis=1)] # Step 3, Renormalize each row of the resulting n * K matrix

    kmeans = KMeans(n_clusters=K, random_state=0).fit(out_matrix) # Step 4, Apply K-means to the row vector
    return kmeans.labels_

# Algorithm 2: Connected Component Extraction: Comparing Covariances
def comparing_covariance(input_data, r, eps, eta):
    n = len(input_data)
    full_index_list = list(range(n))
    C=[]

    #step 1 covariance matrix
    for x_i in input_data:
        N_x_i_list = list(
            [i for i in full_index_list if np.linalg.norm(input_data[i] - x_i) <= r])  # Get N(x_i)'s index
        N_x_i = input_data[N_x_i_list]  # Get N(x_i)
        N_x_i = np.concatenate([N_x_i, x_i.reshape(1, 2)], axis=0)  # Merge x_i and N(x_i)
        N_x_i_list.append(x_i)  # Merge x_i's index and N(x_i)'s index
        C_i = np.cov(N_x_i, rowvar=0, bias=0)  # Covariance Matrix for N(x_i)
        C.append(C_i)

    # Algorithm 2, Step 2, remove x_i
    remaining_index_list = list(range(n))

    x_group_list = []

    while remaining_index_list:
        x_seed_num = np.random.choice(remaining_index_list)  # Pick up x_i's index randomly
        remaining_index_list.remove(x_seed_num)
        x_i=input_data[x_seed_num]
        C_i=C[x_seed_num]
        N_x_i_list = list(
            [i for i in remaining_index_list if (np.linalg.norm(input_data[i] - x_i) <= r) and (np.linalg.norm(C[i] - C_i,2) > eta*r**2)])
        N_x_i = input_data[N_x_i_list]
        number_set = set(remaining_index_list) - set(N_x_i_list)
        remaining_index_list = list(number_set)
        x_group_list.append([x_seed_num,
                             x_i,
                            N_x_i_list,
                            N_x_i,
                            C[x_seed_num]])

    # Algorithm 2, Step 3: compute matrix W

    n0 = len(x_group_list)
    W = nx.Graph()
    W.add_nodes_from(range(n0))

    for i in range(n0):
        for j in range(n0):
            if np.linalg.norm(x_group_list[i][1] - x_group_list[j][1])<=eps and np.linalg.norm(x_group_list[i][4] - x_group_list[j][4],2)<=eta*r**2:
                W.add_edge(i,j)

    # Algorithm 2, Step 4: Extract the connected components of the resulting graph.
    sg = list(nx.connected_component_subgraphs(W))

    K=len(sg)

    #step 5 Each point removed in Step 2 is grouped with the closest point that survived Step 2.

    result_data = np.empty((0, 3), float)

    for i in range(K):
        grp=list(sg[i].node)
        for j in grp:
            x_num=x_group_list[j][0]
            result_data = np.append(result_data, [[input_data[x_num][0], input_data[x_num][1], i]], axis=0)
            for l in x_group_list[j][2]:
                result_data = np.append(result_data, [[input_data[l][0], input_data[l][1], i]], axis=0)

    return result_data,K

# Algorithm 3
def comparing_projection(input_data, r, eps, eta):
    n = len(input_data)
    full_index_list = list(range(n))
    Q=[]

    #step 1,2 covariance matrix and Q
    for x_i in input_data:
        N_x_i_list = list(
            [i for i in full_index_list if np.linalg.norm(input_data[i] - x_i) <= r])  # Get N(x_i)'s index
        N_x_i = input_data[N_x_i_list]  # Get N(x_i)
        N_x_i = np.concatenate([N_x_i, x_i.reshape(1, 2)], axis=0)  # Merge x_i and N(x_i)
        N_x_i_list.append(x_i)  # Merge x_i's index and N(x_i)'s index
        C_i = np.cov(N_x_i, rowvar=0, bias=0)  # Covariance Matrix for N(x_i)
        sn=np.linalg.norm(C_i,2)

        eigen_value, eigen_vector = np.linalg.eig(C_i)
        index = [i for i in eigen_value if i>np.sqrt(eta)*sn]
        d=len(index)
        top_index = eigen_value.argsort()[::-1][0:d]
        P = eigen_vector[:, top_index]  # P is a matrix whose columns are the top d eigenvectors of C
        Q_i= np.dot(P, P.T)  # Get the orthogonal projection matrix
        Q.append(Q_i)

    # Algorithm 3, Step 3: compute matrix W
    W = nx.Graph()
    W.add_nodes_from(range(n))

    for i in range(n):
         for j in range(n):
            if np.linalg.norm(input_data[i] -input_data[j])<=eps and np.linalg.norm(Q[i] - Q[j],2)<=eta:
                W.add_edge(i,j)

    # Algorithm 3, Step 4: Extract the connected components of the resulting graph.
    sg = list(nx.connected_component_subgraphs(W))

    K=len(sg)

    #step 5 Each point removed in Step 2 is grouped with the closest point that survived Step 2.

    result_data = np.empty((0, 3), float)

    for i in range(K):
        grp=list(sg[i].node)
        for j in grp:
            result_data = np.append(result_data, [[input_data[j][0], input_data[j][1], i]], axis=0)

    return result_data,K

# Algorithm 4
def spectral_clustering_lpca(input_data, r, eps, eta, d, K):
    np.random.seed(0)
    n = len(input_data)
    ramaining_index_list = list(range(n))
    full_index_list = list(range(n))

    N_y_list = []

    while ramaining_index_list:
        y_seed_num = np.random.choice(ramaining_index_list)  # Pick up y_i's index randomly
        ramaining_index_list.remove(y_seed_num)  # Remove y_i's index form the residual list
        y_i = input_data[y_seed_num]  # Get y_i

        N_y_i_list = list(
            [i for i in full_index_list if np.linalg.norm(input_data[i] - y_i) < r])  # Get N(y_i)'s index
        N_y_i = input_data[N_y_i_list]  # Get N(y_i)
        N_y_i = np.concatenate([N_y_i, y_i.reshape(1, 2)], axis=0)  # Merge y_i and N(y_i)

        number_set = set(ramaining_index_list) - set(N_y_i_list)
        ramaining_index_list = list(number_set)  # Remove N(y_i)'s index form the residual list

        N_y_i_list.append(y_seed_num)  # Merge y_i's index and N(y_i)'s index

        C = np.cov(N_y_i, rowvar=0, bias=0)  # Covariance Matrix for N(y_i)

        eigen_value, eigen_vector = np.linalg.eig(C)
        top_index = eigen_value.argsort()[::-1][0:d]
        P = eigen_vector[:, top_index]  # P is a matrix whose columns are the top d eigenvectors of C
        Q = np.dot(P, P.T)  # Get the orthogonal projection matrix

        # OUTPUT
        N_y_list.append([y_i,
                         N_y_i_list,
                         N_y_i,
                         C,
                         Q])

    # Algorithm 4, Step 2, Compute the following affinities W_ij
    n0 = len(N_y_list)
    W = np.zeros([n0, n0])
    for i in range(n0):
        for j in range(n0):
            W[i][j] = np.exp(-np.linalg.norm(N_y_list[i][0] - N_y_list[j][0]) ** 2 / eps ** 2) \
                      * np.exp(-np.linalg.norm(N_y_list[i][4] - N_y_list[j][4]) ** 2 / eta ** 2)

    # Algorithm 4, Step 3
    # Use algorithm 1, Spectral Graph Partitioning
    y_class = SpectralGraphPartitioning(W=W, K=K)

    # Create y array for the next calculation to find the closest y_j
    y = np.empty((0, 2), float)
    for i in range(n0):
        y = np.append(y, np.r_[N_y_list[i][0]].reshape(1, 2), axis=0)

    # Algorithm 4, Step 4
    # For all input data x_i, find the closest y_j
    result_data = np.empty((0, 3), float)
    for i in range(n):
        min_index = np.argmin(np.linalg.norm(y - np.r_[input_data[i]], axis=1))
        result_data = np.append(result_data, [[input_data[i][0], input_data[i][1], y_class[min_index]]], axis=0)

    return result_data

# Visualization
def plot_spectral_clustering(picture_name, color_threshold, r, eps, eta, d=1, K=3, algorithm=4):
    im1 = Image.open(picture_name)
    pixel_array = np.array(im1.getdata())
    black_flag = (pixel_array[:, 0] < color_threshold) \
                 * (pixel_array[:, 1] < color_threshold) \
                 * (pixel_array[:, 2] < color_threshold)
    black_flag = black_flag.reshape(im1.height, im1.width)

    sample_data = np.empty((0, 2), float)
    for i in range(im1.height):
        for j in range(im1.width):
            if black_flag[i][j]:
                sample_data = np.append(sample_data, np.array([[j, (im1.height - 1) - i]]),
                                        axis=0)  # (x, y) = (width index, height index)

    # Plot the input data
    fig = plt.figure(figsize=(12, 4))  # Create an empty figure.
    sub1 = fig.add_subplot(1, 2, 1)  # Notice we are creating a 2x2 plot.
    sub2 = fig.add_subplot(1, 2, 2)  # 2nd one.
    sub1.plot(sample_data[:, 0], sample_data[:, 1], "o", markersize=1)

    if algorithm == 2:
        [result_data, K] = comparing_covariance(input_data=sample_data, r=r, eps=eps, eta=eta)
    if algorithm == 3:
        [result_data, K] = comparing_projection(input_data=sample_data, r=r, eps=eps, eta=eta)
    if algorithm == 4:
        result_data = spectral_clustering_lpca(input_data=sample_data, r=r, eps=eps, eta=eta, d=d, K=K)


    # Plot the final result
    color_list = ['red', 'blue', 'green', 'cyan', 'magenta', 'yellow', 'black']
    for i in range(K):
        sub2.plot(result_data[:, 0][result_data[:, 2] == i], result_data[:, 1][result_data[:, 2] == i], "o",
                  markersize=1) #, c=color_list[i]

