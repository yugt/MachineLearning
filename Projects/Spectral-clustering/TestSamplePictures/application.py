import spectral_clustering_lpca as lpca
from scipy.ndimage.interpolation import zoom

#
#pic=Image.open('eqn01.png')
#
#pic= np.array(pic.getdata())
#pic=zoom(pic,0.2)
#plt.imshow(pic)

lpca.plot_spectral_clustering(picture_name ='eqn01.png',
                         color_threshold = 30,
                         r = 50.0,
                         eps = 25.0,
                         eta = 1.0,
                         d = 10,
                         K = 3)