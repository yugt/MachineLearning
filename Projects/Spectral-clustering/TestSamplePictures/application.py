import spectral_clustering_lpca as lpca

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.transform import resize
#
#pic=Image.open('eqn01.png')
#
#pic= np.array(pic.getdata())
#pic=zoom(pic,0.2)
#plt.imshow(pic)


raw=Image.open('test1.png')
arr= np.array(raw.getdata())
arr=np.min(arr,axis=1)
arr=np.reshape(arr, newshape=np.array([raw.height,raw.width]))
plt.imshow(1-arr,cmap='Greys')

arr = resize(arr, (10*(raw.height//10), 10*(raw.width//10)), mode='reflect')
arr = arr.reshape(raw.height//10,10,raw.width//10,10).min(axis=(1,3))
arr=arr/np.max(arr)
result = np.argwhere(arr<np.mean(arr))


#plt.imshow(1-arr,cmap='Greys')
#plt.savefig(fname='test3.png')

result=lpca.spectral_clustering_lpca(result, 3, 3, 1.0, 1, 30)
result[:,[0,1]] = 10*result[:,[1,0]]
lpca.plot_spectral_clustering(result, 30)


#np.einsum('ijkl->ik',arr.reshape(5,20,5,20))


#lpca.plot_spectral_clustering(picture_name ='test1.png',
#                         color_threshold = 30,
#                         r = 500.0,
#                         eps = 200.0,
#                         eta = 1.0,
#                         d = 1,
#                         K = 20)