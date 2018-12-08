### Import the main function file
# Put "spectral_clustering_lpca.py" in the same folder
# Need pillow package
import spectral_clustering_lpca as sc

### Function Description
print(sc.plot_spectral_clustering.__doc__)

### Figure 2: Clustering example
sc.plot_spectral_clustering(picture_name = 'cross_shaped.png',
                         color_threshold = 15,
                         r = 15.0,
                         eps = 15.0,
                         eta = 0.5,
                         d = 1,
                         K = 2)

'''
### Figure 3: Example of intersection cluster
sc.plot_spectral_clustering(picture_name = 'infinity_shaped.png',
                         color_threshold = 15,
                         r = 15.0,
                         eps = 15.0,
                         eta = 0.3,
                         d = 1,
                         K = 2)

### Figure 4: Failure at the corner
sc.plot_spectral_clustering(picture_name = 'sharp_720.png',
                         color_threshold = 10,
                         r = 10.0,
                         eps = 10.0,
                         eta = 0.5,
                         d = 1,
                         K = 3)

### Figure 5-1: Successful results with smooth data
sc.plot_spectral_clustering(picture_name = 'smooth_720_1.png',
                         color_threshold = 10,
                         r = 10.0,
                         eps = 10.0,
                         eta = 0.5,
                         d = 1,
                         K = 3)

### Figure 5-2: Successful results with smooth data
sc.plot_spectral_clustering(picture_name = 'smooth_720_2.png',
                         color_threshold = 10,
                         r = 10.0,
                         eps = 10.0,
                         eta = 0.5,
                         d = 1,
                         K = 3)

### Figure 6: [Left]: eta = 0.1
sc.plot_spectral_clustering(picture_name = 'smooth_720_1.png',
                         color_threshold = 10,
                         r = 10.0,
                         eps = 10.0,
                         eta = 0.1,
                         d = 1,
                         K = 3)

### Figure 6: [Right]: eta = 1.0
sc.plot_spectral_clustering(picture_name = 'smooth_720_1.png',
                         color_threshold = 10,
                         r = 10.0,
                         eps = 10.0,
                         eta = 1.0,
                         d = 1,
                         K = 3)

### Figure 7: [Left]: r = 3.0
sc.plot_spectral_clustering(picture_name = 'smooth_720_1.png',
                         color_threshold = 10,
                         r = 3.0,
                         eps = 10.0,
                         eta = 0.5,
                         d = 1,
                         K = 3)

### Figure 7: [Right]: r = 40.0
sc.plot_spectral_clustering(picture_name = 'smooth_720_1.png',
                         color_threshold = 10,
                         r = 40.0,
                         eps = 10.0,
                         eta = 0.5,
                         d = 1,
                         K = 3)

### Figure 8: [Left]: eps = 3.0
sc.plot_spectral_clustering(picture_name = 'smooth_720_1.png',
                         color_threshold = 10,
                         r = 10.0,
                         eps = 3.0,
                         eta = 0.5,
                         d = 1,
                         K = 3)

### Figure 8: [Right]: eps = 40.0
sc.plot_spectral_clustering(picture_name = 'smooth_720_1.png',
                         color_threshold = 10,
                         r = 10.0,
                         eps = 40.0,
                         eta = 0.5,
                         d = 1,
                         K = 3)
'''