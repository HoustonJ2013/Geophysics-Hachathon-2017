import os
import sys
from obspy.io.segy.core import _read_segy
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib
from PIL import Image
import PIL
from sklearn.cluster import KMeans
import time
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope,MinCovDet
import math

st1 = _read_segy("teapot_dome_filt_mig.sgy")

# Convert the obspy stream data into a matrix of the same size
def str_to_matrix(st):
    n1 = len(st)   # No of traces
    n2 = len(st[0].data)  # no of samples per trace
    mat = np.zeros([n1,n2])
#    print n1,n2
    for i in range(n1):
        mat[i,:] = st[i].data
    return mat

class img2d_plot :
    def __init__(self,imgarray,figsize = (10,10),colormap= "Greys"):
        self.img = imgarray
        self.figsize = figsize
        self.colormap = colormap
    def plot_2d_il(self,index1,index2,gain = -2):
        img = self.img[index1:index2]
        crange = np.sqrt(np.mean(np.square(img)))
        vmin = - math.exp(-gain) * crange
        vmax = -vmin
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111)
        ax.imshow(img.T,cmap = self.colormap,vmin = vmin, vmax = vmax)
        ax.set_aspect(0.2)
        fig.show()
        return

## Data is in matrix form  : x number of traces y no. of samples
img01 = str_to_matrix(st1)
plot2d = img2d_plot(img01)

## Counts the data for non-continuous seismic images
def index_gap_find(binary_input):
    index1 =[]
    index2 =[]
    for i in range(len(binary_input)):
        if binary_input[i] == True and binary_input[i-1] == False :
            index1.append(i)
        if i > 1 :
            if binary_input[i] == False and binary_input[i - 1] == True :
                index2.append(i)
    return index1, index2
tem = img01[:,700]
index1, index2 = index_gap_find(tem != 0)


## Return a 3D array imgcrop (nx,ny,num_img)
def image_split(img,step,size = (50,50)):
    img = img[:,200:1200]
    nx,ny = img.shape
    sizex,sizey = size
    img_list = []
    if sizex > nx or sizey > ny :
        return None
    for i in range(0,nx-sizex,step):
        for j in range(0,ny-sizey,step):
            img_list.append(list(img[i:i+sizex,j:j+sizey]))
    return np.array(img_list)

def plot_img(img,figsize = (2,2), gain = -1):
    crange = np.sqrt(np.mean(np.square(img)))
    vmin = - math.exp(-gain) * crange
    vmax = -vmin
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    ax.imshow(img.T,cmap = "Greys",vmin = vmin, vmax = vmax)
    ax.set_aspect(1)
    fig.show()


n_ils = len(index1)
imgindex = 0
for i in range(n_ils):
    imgcrop = image_split(img01[index1[i]:index2[i],:],20,size = (50,50))
    print("Finished " + str(i))
    if imgcrop is not None :
        ncrop = imgcrop.shape[0]
        for j in range(ncrop):
            np.savetxt("Teapot_dome/sec_"+ str(i) + "_p" + str(imgindex),imgcrop[j,:,:])
            imgindex = imgindex + 1

## QC sections
imgtst = np.loadtxt("Teapot_dome/sec_" + str(np.random.randint(0,46000)))
plot_img(imgtst)
