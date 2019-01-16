#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 13:40:47 2017

@author: michellefeng
"""

from numpy import genfromtxt
from scipy.spatial.distance import pdist,squareform
import numpy as np
import invr
import sys
import cProfile

def form_simplicial_complex(filename,candidate):

    inputDir = "../data/extractcentroids/" + candidate + "/"
    outputDir="../data/vrcomplex/" + candidate + "/"
    centroid_data = genfromtxt(inputDir+filename+".csv",delimiter=",")
    distances = pdist(centroid_data[:,1:3])
    max_filtration_size = np.median(distances)/2
    num_filtrations = 10
    maxDimension = 3

    V = []
    entryTimesSub = []

    for entryTime in np.arange(num_filtrations):
        currNumEntries = len(entryTimesSub)
        curr_filtration_value = max_filtration_size*(entryTime+1)/num_filtrations
        adjacency = squareform(distances < curr_filtration_value)
        list_edges = np.array(adjacency.nonzero())
        neighbors = []
        for vertexId in np.arange(centroid_data.shape[0]):
            row = list(list_edges[1,list_edges[0,:]==vertexId] + 1)
            neighbors.append(row)
        V=invr.incremental_vr(V,neighbors,maxDimension)
        newNumEntries = len(V) - currNumEntries
        entryTimesSub = entryTimesSub + [entryTime]*newNumEntries

    phatFormatV = invr.replace_face(V)

    np.savetxt(outputDir + filename + '_entry_times.csv',entryTimesSub,
               delimiter=' ',fmt='%i')
    
    
    F = open(outputDir + filename + ".dat","w")

    for face in phatFormatV:
        F.write(str(len(face)-1))
        if len(face) > 1:
            for simplex in face:
                F.write(" " + str(simplex))
        F.write("\n")
    F.close()
    

if (len(sys.argv)!=3):
    print "Syntax: build_distance.py county candidate"
else:
    form_simplicial_complex(sys.argv[1],sys.argv[2])
#cProfile.run("form_simplicial_complex('107-tulare','trump')")