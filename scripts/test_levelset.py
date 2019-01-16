#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 15:29:18 2018

@author: michellefeng
"""

import fiona
import rasterio
import numpy as np
import rasterio.mask
from rasterio import features
from affine import Affine
from matplotlib import pyplot

def levelset_ph(gridsize,phi_init,width=1600,height=1200,dt=1,t_end=500):
    t=0;
    phi_curr=phi_init.copy()
    F=np.zeros((height,width))+1
    F[0:height:gridsize,:]=0;
    F[:,0:width:gridsize]=0;
    while t<t_end:
        t=t+dt
        gradxvals=phi_curr[:,1:width]-phi_curr[:,0:width-1]
        gradyvals=phi_curr[1:height,:]-phi_curr[0:height-1,:]
        gradxpos=np.zeros((height,width))
        gradypos=gradxpos.copy()
        gradxpos[:,0]=gradxvals[:,0]
        gradxpos[:,1:width]=gradxvals
        gradypos[0,:]=gradyvals[0,:]
        gradypos[1:height,:]=gradyvals
        
        gradpos=np.sqrt(gradxpos*gradxpos + gradypos*gradypos)
        phi_curr=np.sign(phi_curr-dt*((F>0)*gradpos));
    return phi_curr

with fiona.open("../data/shapefiles/107-tulare.shp") as shapefile:
    precincts = [feature["geometry"] for feature in shapefile if feature["properties"]["Hill%"]<0]


src=rasterio.open('../data/maps/107-tulare.png')
#out_image, out_transform = rasterio.mask.mask(src, precincts, invert=True)
#out_meta = src.meta.copy()

src_transform=src.transform
leftbound=src_transform[0]
rightbound=src_transform[0]+600*src_transform[1]
botbound=src_transform[3]
topbound=src_transform[3]+800*src_transform[5]
newwidth=1600
newheight=1200
newtransform=Affine((rightbound-leftbound)/newheight,0,leftbound,
                    0,(topbound-botbound)/newwidth,botbound)
shapes = ((g,255) for g in precincts)
image = features.rasterize(
            shapes, out_shape=(newheight,newwidth), transform=newtransform)

#pyplot.imshow(image,cmap='Greys')

init=image.astype(np.int)
init=-(init/255*2)+1

phi_end=levelset_ph(75,init)
newim=(phi_end+1)/2*255
pyplot.imshow(newim,cmap='Greys')
pyplot.savefig('../results/levelset/lstulare-4.png')

