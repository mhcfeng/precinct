#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 12:31:03 2017

@author: michellefeng
"""

import csv
from matplotlib import collections  as mc
import matplotlib.pyplot as pl
from pylab import MaxNLocator
import numpy as np
import os.path
import logging


def parse_csv_to_birth_death(filename):
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        data = list(readCSV)
        dim_zero_it=1
        dim_one_it=1
        dim_zero=[]
        dim_one=[]
        for row in data:
            if row[0] == "0":
                birth_tup = (row[1],dim_zero_it)
                death_tup = (row[2],dim_zero_it)
                dim_zero.append([birth_tup,death_tup])
                dim_zero_it += 1
            if row[0] == "1":
                birth_tup = (row[1],dim_one_it)
                death_tup = (row[2],dim_one_it)
                dim_one.append([birth_tup,death_tup])
                dim_one_it += 1
    return dim_zero,dim_one


def pairs_to_barcodes(county, candidate, sc_type):
    results_dir = '../results/'+sc_type+'/'+candidate+'/'
    if os.path.isfile(results_dir+county+'.csv'):
        [dim_zero,dim_one] = parse_csv_to_birth_death(results_dir+county+'.csv')

        dim_zero_lines = mc.LineCollection(dim_zero, linewidths=2)
        dim_one_lines = mc.LineCollection(dim_one, linewidth=2)
        fig, ax = pl.subplots(2, sharex=True)
        ax[0].add_collection(dim_zero_lines)
        ax[1].add_collection(dim_one_lines)
        ax[0].autoscale()
        ax[1].autoscale()
        ax[0].set_title("$H_0$", fontsize=20)
        ax[1].set_title("$H_1$", fontsize=20)
        ya = ax[0].get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))
        ya = ax[1].get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))
        a = ax[1].get_xticks().tolist()
        if sc_type == 'adj':
            b = list((19-np.asarray(a))*5)
        else:
            b = a
        ax[0].set_xticklabels(b)
        ax[0].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
        ax[1].set_xticklabels(b)
        ax[1].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
        if sc_type == 'adj':
            ax[1].set_xlabel('Strength of Preference', fontsize=20)
        elif sc_type == 'ls':
            ax[1].set_xlabel('T', fontsize=20)
        else:
            ax[1].set_xlabel('$\epsilon$', fontsize=20)
        pl.tight_layout()
        barcode_dir = '../results/barcodes/'+sc_type+'/'+candidate+'/'
        fig.savefig(barcode_dir+county+'.png')
        pl.close(fig)
    else:
        logging.warning('No results file for ' + county + ', ' + candidate + ', ' + sc_type)
    
# if (len(sys.argv)!=3):
#     print "Wrong number of arguments"
# else:
#     pairs_to_barcodes(sys.argv[1],sys.argv[2])
def main():
    logging.basicConfig(filename='../logs/barcodes.log', filemode='w', level=logging.WARNING)
    with open('../full-list') as county_file:
        for county in county_file:
            county = county.split('\n')[0]
            for candidate in ['hillary', 'trump']:
                for sc_type in ['ls','adj','rips','alpha']:
                    pairs_to_barcodes(county, candidate, sc_type)


if __name__ == '__main__':
    main()

