#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 13:39:42 2017

@author: michellefeng
"""
import numpy as np


def lower_neighbors(adjacencies, vertex):
    return [v for v in adjacencies[vertex] if v < vertex]


def incremental_vr(V, adjacencies, maxDimension):
    Vnew = list(V)
    for vertex in np.arange(len(adjacencies)):
        N = sorted(lower_neighbors(adjacencies, vertex))
        add_cofaces(adjacencies, maxDimension, [vertex], N, Vnew)
    return Vnew


def add_cofaces(adjacencies, maxDimension, face, N, V):
    if sorted(face) not in V:
        V.append(sorted(face))
    if len(face) >= maxDimension:
        return
    else:
        for vertex in N:
            coface = list(face)
            coface.append(vertex)
            M = list(set(N) & set(lower_neighbors(adjacencies, vertex)))
            add_cofaces(adjacencies, maxDimension, coface, M, V)


def replace_face(V):
    Vnew = []
    for face in V:
        if len(face) == 1:
            Vnew.append([len(Vnew)])
        else:
            Vnew_face = []
            for vertexIdx in np.arange(len(face)):
                subface = list(face)
                subface.pop(vertexIdx)
                subfaceIdx = V.index(subface)
                Vnew_face.append(subfaceIdx)
            Vnew.append(sorted(Vnew_face))
    return Vnew
