#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 09:37:11 2017

@author: michellefeng
"""

import csv
import numpy as np
import sys
import invr

def parse_csv_to_adjacencies(filename):
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        data = list(readCSV)
        preferences = np.zeros((len(data),))
        adjacencies = []
        rowIdx = 0
        for row in data:
            if row[2] == "":
                row[2] = 0
            print(row[1])
            row[1] = [int(i) for i in row[1].split()]
            print(row[1])
            adjacencies.append(row[1])
            preferences[rowIdx] = float(row[2])
            rowIdx = rowIdx+1
    return adjacencies,preferences


def form_simplicial_complex(filename,candidate):
    inputDir = \
        '../data/adjacency/'
    maxDimension = 3
    if(candidate == "trump"):
        [adjacencies,preferences] = parse_csv_to_adjacencies(inputDir
            + "trump/" + filename + ".csv")
        V = []
        V = invr.incremental_vr(V,adjacencies,maxDimension)
        outputDir = \
            '../data/simplicialcomplex/trump/'
    elif(candidate=="hill"):
        [adjacencies,preferences] = parse_csv_to_adjacencies(inputDir
            + "hill/" + filename + ".csv")
        V = []
        V = invr.incremental_vr(V,adjacencies,maxDimension)
        outputDir = \
            '../data/simplicialcomplex/hill/'
    else:
        print('Invalid Candidate')
        return

    entryTimes = np.floor((1-np.abs(preferences))*100/5)

    entryTimesSub = [entryTimes[max(simplex)-1] for simplex in V]

    np.savetxt(outputDir + filename + '_entry_times.csv',entryTimesSub,
               delimiter=' ',fmt='%i')

    phatFormatV = invr.replace_face(V)


    # F = open(outputDir + filename + ".dat","w")
    #
    # for face in phatFormatV:
    #     F.write(str(len(face)-1))
    #     if len(face) > 1:
    #         for simplex in face:
    #             F.write(" " + str(simplex))
    #     F.write("\n")
    # F.close()

# if (len(sys.argv)!=3):
#     print "Syntax: build_adjacency.py county candidate"
# else:
#     form_simplicial_complex(sys.argv[1],sys.argv[2])
# #cProfile.run("form_simplicial_complex('107-tulare','trump')")

if __name__ == '__main__':
    form_simplicial_complex('001-alameda', 'hill')
