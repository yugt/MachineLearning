'''
To use the algorithm for Spectral Clustering based on Local PCA,
import this file and use the function.

*** Example ***
import spectral_clustering_lpca as sc
sc.plot_spectral_clustering(picture_name = 'cross_shaped.png',
                         color_threshold = 15,
                         r = 15.0,
                         eps = 15.0,
                         eta = 0.5,
                         d = 1,
                         K = 2)
'''

import numpy as np
from sklearn.cluster import KMeans  # used in Algorithm 1 (Spectral Graph Partitioning)
from PIL import Image               # used to handle input figures
import matplotlib.pyplot as plt

# Algorithm 1 (Spectral Graph Partitioning) in the paper, which is used in Algorithm 4 *********************************
def SpectralGraphPartitioning(W, K):
    '''
    ***Input***
    W: float, 2d-array (N * N, where N is the number of data point)
        Affinity matrix
    K: int
        The number of clusters

    ***Return***
    kmeans.labels_: int, 1d-array (with length N)
        The labels of each data point
    '''
    W_rowsum = W.sum(axis=1)
    Z = W / np.sqrt(np.outer(W_rowsum, W_rowsum)) # Step 1, Compute Z
    eigen_value, eigen_vector = np.linalg.eig(Z)
    top_index = eigen_value.argsort()[::-1][0:K]
    out_matrix = eigen_vector[:, top_index]       # Step 2, Extract the top K eigenvectors of Z
    # Step 3, Renormalize each row of the resulting n * K matrix
    out_matrix = out_matrix / np.c_[np.linalg.norm(out_matrix, axis=1)]
    # Step 4, Apply K-means to the row vector
    kmeans = KMeans(n_clusters=K, random_state=0).fit(out_matrix)
    return kmeans.labels_

# Algorithm 4 (main algorithm), used in "plot_spectral_clustering" function ********************************************
def spectral_clustering_lpca(input_data, r, eps, eta, d, K):
    '''
    ***Input***
    input_data:

    r: float
        neighborhood radius parameter, r > 0.
    eps: float
        spatial scale parameter, eps > 0.
    eta: float
        projection scale parameter, eps > 0.
    d: int
        intrinsic dimension, d >= 1.
    K: int
        number of clusters, K >= 2.

    ***Return***
    result_data: float, 2d-array (n * 3, where n is the number of "black pixels" of the input figure)
        Each row corresponds to each pixel of the input figure.
        Each row data means [ x-coordinate, y-coordinate, label ].
    '''
    np.random.seed(0)
    n = len(input_data)
    ramaining_index_list = list(range(n))
    full_index_list = list(range(n))

    N_y_list = []

    # 1st and 2nd Step: Creates y_i, N(y_i), C_i, Q_i
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
        Q = np.dot(P, P.T)              # Get the orthogonal projection matrix

        # intermediate output about N(y_i)
        N_y_list.append([y_i,
                         N_y_i_list,
                         N_y_i,
                         C,
                         Q])

    # 3rd Step: Compute the following affinities W_ij
    n0 = len(N_y_list)
    W = np.zeros([n0, n0])
    for i in range(n0):
        for j in range(n0):
            # Note N_y_list[i][0] is y_i and N_y_list[i][4] is Q_i, created above.
            # Note the first norm is a vector norm and the second is a matrix norm.
            W[i][j] = np.exp(-np.linalg.norm(N_y_list[i][0] - N_y_list[j][0]) ** 2 / eps ** 2) \
                      * np.exp(-np.linalg.norm(N_y_list[i][4] - N_y_list[j][4]) ** 2 / eta ** 2)

    # 4th Step: Use algorithm 1 (Spectral Graph Partitioning) for W
    y_class = SpectralGraphPartitioning(W=W, K=K)

    # Create y array to prepare for the next calculation to find the closest y_j
    y = np.empty((0, 2), float)
    for i in range(n0):
        y = np.append(y, np.r_[N_y_list[i][0]].reshape(1, 2), axis=0)

    # 5th Step: For all input data x_i, find the closest y_j
    result_data = np.empty((0, 3), float)
    for i in range(n):
        min_index = np.argmin(np.linalg.norm(y - np.r_[input_data[i]], axis=1))
        result_data = np.append(result_data, [[input_data[i][0], input_data[i][1], y_class[min_index]]], axis=0)

    return result_data

# Called for Visualization *********************************************************************************************
# Accepts a input file name and generates a png output file in the same folder
def plot_spectral_clustering(picture_name, color_threshold, r, eps, eta, d, K, *, fig_width=6, fig_height=4):
    '''
    ***Input***
    picture_name: str
        File name of the input figure such as "sample.png".
        The file should be saved in the same folder.
    color_threshold: int
        Parameter used to convert the original figure into the pixel-coordinate array.
        If all of (Red, Green, Blue) is smaller than this threshold, the pixel is recognized as "black point".
        0 < color_threshold < 255.
    r: float
        neighborhood radius parameter, r > 0.
    eps: float
        spatial scale parameter, eps > 0.
    eta: float
        projection scale parameter, eps > 0.
    d: int
        intrinsic dimension, d >= 1.
    K: int
        number of clusters, K >= 2.
    (optional) fig_width: int
        width of output figure in inch. the default value is 6.
    (optional) fig_height: int
        height of output figure in inch. the default value is 4.

    ***Return***
    This function doesn't have a return value but generates plots and png files in the same folder.
    '''
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

    # Call Algorithm 4
    result_data = spectral_clustering_lpca(input_data=sample_data, r=r, eps=eps, eta=eta, d=d, K=K)

    # Plot the input data
    fig = plt.figure(figsize=(2*fig_width, fig_height))  # Create an empty figure.
    sub1 = fig.add_subplot(1, 2, 1)    # creating 2 plots. 1st one.
    sub2 = fig.add_subplot(1, 2, 2)    # 2nd one.
    sub1.plot(sample_data[:, 0], sample_data[:, 1], "o", markersize=1)

    # Plot the final result (Input and Result in the same row)
    color_list = ['red', 'blue', 'green', 'cyan', 'magenta', 'yellow',
                  'tan', 'gold', 'orange', 'plum', 'brown', 'pink', 'crimson']  # prepare  colors
    for i in range(K):
        sub2.plot(result_data[:, 0][result_data[:, 2] == i], result_data[:, 1][result_data[:, 2] == i], "o",
                  markersize=1, c=color_list[i % len(color_list)])
    fig.savefig(picture_name[:-4] + '_output_1.png')

    # Plot the final result (Result only)
    fig = plt.figure(figsize=(fig_width, fig_height))
    for i in range(K):
        plt.plot(result_data[:, 0][result_data[:, 2] == i], result_data[:, 1][result_data[:, 2] == i], "o",
                  markersize=1, c=color_list[i % len(color_list)])
    fig.savefig(picture_name[:-4] + '_output_2.png')