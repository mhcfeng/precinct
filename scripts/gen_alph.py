import gudhi
import numpy as np
import itertools
from scipy import spatial
import sys

def form_simplicial_complex(county, candidate):
    input = '../data/extractcentroids/' + candidate + '/' + county + '.csv'
    data = np.genfromtxt(input, delimiter=',')
    dat_output = '../data/vrcomplex/' + candidate + '/' + county + '.dat'
    entry_output='../data/vrcomplex/' + candidate + '/' + county + '_entry_times.csv'
    coords = data[:,1:3]
    alpha_complex = gudhi.AlphaComplex(points=coords)
    max_filtration_size = np.median(spatial.distance.pdist(coords))

    simplex_tree = alpha_complex.create_simplex_tree(max_alpha_square=max_filtration_size)

    test=simplex_tree.get_filtration()
    simplices, entryres = map(list, zip(*test))
    num_filtrations = 20
    filtration_width = max_filtration_size/num_filtrations
    print('\n'.join(map(str,(np.floor(entryres/filtration_width)).astype(int))), file=open(entry_output, "w"))

    f = open(dat_output, "w+")
    for k in range(len(simplices)):
        if len(simplices[k])==1:
            f.write('0\n')
        else:
            subsimplices = [list(i) for i in list(itertools.combinations(simplices[k],len(simplices[k])-1))]
            f.write(str(len(subsimplices)-1) + ' ' + ' '.join(map(str,[simplices.index(subsimplices[i]) for i in range(len(subsimplices))])) + '\n')

    f.close()

if (len(sys.argv)!=3):
    print("Syntax: build_distance.py county candidate")
else:
    form_simplicial_complex(sys.argv[1],sys.argv[2])