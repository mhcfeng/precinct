import csv
import gudhi
import numpy as np
import itertools
from scipy import spatial
import logging
import time
import os.path


def split_precincts(county_csv, split_key, header=True):
    with open(county_csv) as file:
        csv_reader = csv.reader(file)
        if header:
            next(csv_reader)
        precinct_list = list(csv_reader)

    hillary_list = []
    trump_list = []
    for precinct in precinct_list:
        if float(precinct[split_key]) > 0:
            hillary_list.append(precinct)
        elif float(precinct[split_key]) < 0:
            trump_list.append(precinct)
    return hillary_list, trump_list


def write_key(county, candidate, precinct_list, sc_type):
    key_file = '../data/keys/' + sc_type + '/' + candidate + '/' + county + '-key'
    with open(key_file, 'w') as file:
        csv_writer = csv.writer(file)
        i = 0
        for precinct in precinct_list:
            csv_writer.writerow([precinct[0], i])
            precinct[0] = i
            i += 1
    return precinct_list


def form_alpha_complex(precinct_list, candidate, county):
    dat_output = '../data/sc/alpha/' + candidate + '/' + county + '.dat'
    entry_output = '../data/sc/alpha/' + candidate + '/' + county + '_entry_times.csv'

    data = np.asarray(precinct_list)
    coords = data[:, 1:3].astype(np.float)

    alpha_complex = gudhi.AlphaComplex(points=coords)
    max_filtration_size = np.median(spatial.distance.pdist(coords))

    simplex_tree = alpha_complex.create_simplex_tree(max_alpha_square=max_filtration_size)

    filtration_times = simplex_tree.get_filtration()
    if filtration_times:
        simplices, entryres = map(list, zip(*filtration_times))
        num_filtrations = 1000
        filtration_width = max_filtration_size/num_filtrations
        print('\n'.join(map(str, (np.floor(entryres/filtration_width)).astype(int))), file=open(entry_output, "w"))

        f = open(dat_output, "w+")
        for k in range(len(simplices)):
            if len(simplices[k]) == 1:
                f.write('0\n')
            else:
                subsimplices = [list(i) for i in list(itertools.combinations(simplices[k], len(simplices[k])-1))]

                num_subsimps = len(subsimplices)
                boundary_simps = ' '.join(map(str, [simplices.index(subsimplices[i]) for i in range(num_subsimps)]))

                f.write(str(num_subsimps-1) + ' ' + boundary_simps + '\n')

        f.close()

    else:
        logging.warning(county + ' ' + candidate + ' resulted in empty filtration')


def form_rips_complex(precinct_list, candidate, county):
    dat_output = '../data/sc/rips/' + candidate + '/' + county + '.dat'
    entry_output = '../data/sc/rips/' + candidate + '/' + county + '_entry_times.csv'

    data = np.asarray(precinct_list)
    coords = data[:, 1:3].astype(np.float)

    if coords.shape[0] < 150:
        max_filtration_size = np.median(spatial.distance.pdist(coords))
        rips_complex = gudhi.RipsComplex(points=coords, max_edge_length=max_filtration_size)

        simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)

        filtration_times = simplex_tree.get_filtration()
        if filtration_times:
            simplices, entryres = map(list, zip(*filtration_times))
            num_filtrations = 40
            filtration_width = max_filtration_size/num_filtrations
            print('\n'.join(map(str, (np.floor(entryres/filtration_width)).astype(int))), file=open(entry_output, "w"))

            f = open(dat_output, "w+")
            for k in range(len(simplices)):
                if len(simplices[k]) == 1:
                    f.write('0\n')
                else:
                    subsimplices = [list(i) for i in list(itertools.combinations(simplices[k], len(simplices[k])-1))]

                    num_subsimps = len(subsimplices)
                    boundary_simps = ' '.join(map(str, [simplices.index(subsimplices[i]) for i in range(num_subsimps)]))

                    f.write(str(num_subsimps-1) + ' ' + boundary_simps + '\n')

            f.close()

        else:
            logging.warning(county + ' ' + candidate + ' resulted in empty filtration')
    else:
        logging.warning(county + ' ' + candidate + ' had too many precincts to get rips complex')


def form_complex(precinct_list, candidate, county, sc_type):
    if sc_type == 'rips':
        form_rips_complex(precinct_list, candidate, county)
    elif sc_type == 'alpha':
        form_alpha_complex(precinct_list, candidate, county)


def main():
    with open('../full-list') as county_file:
        for sc_type in ['alpha']:
            timing_csv = '../runtimes/'+sc_type+'_times.csv'
            logging.basicConfig(filename='../logs/'+sc_type+'.log', filemode='w', level=logging.WARNING)
            with open(timing_csv, 'w') as timing_file:
                for county in county_file:
                    county = county.split('\n')[0]
                    input_csv = '../data/extractcentroids/' + county + '.csv'
                    hillary_list, trump_list = split_precincts(input_csv, 3)
                    hillary_list = write_key(county, 'hillary', hillary_list, sc_type)
                    trump_list = write_key(county, 'trump', trump_list, sc_type)

                    start_time = time.time()
                    if hillary_list:
                        form_complex(hillary_list, 'hillary', county, sc_type)
                    timing_file.write(county+',rips,hillary,'+str(time.time()-start_time)+'\n')

                    start_time = time.time()
                    if trump_list:
                        form_complex(trump_list, 'trump', county, sc_type)
                    timing_file.write(county+',rips,trump,'+str(time.time()-start_time)+'\n')


if __name__ == '__main__':
    main()
