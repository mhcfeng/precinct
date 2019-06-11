import csv
import invr
import numpy as np
import time


def split_precincts(county_csv, split_key, header=True):
    hillary_list = []
    trump_list = []
    with open(county_csv) as file:
        csv_reader = csv.reader(file)
        if header:
            next(csv_reader)

        for line in csv_reader:
            if float(line[split_key]) > 0:
                hillary_list.append(line)
            elif float(line[split_key]) < 0:
                trump_list.append(line)

    hillary_list.sort(key=lambda x: float(x[split_key]), reverse=True)
    trump_list.sort(key=lambda x: float(x[split_key]))
    return hillary_list, trump_list


def generate_keys(county, candidate, precinct_list, sc_type):
    key_file = '../data/keys/' + sc_type + '/' + candidate + '/' + county + '-key'
    with open(key_file, 'w') as file:
        csv_writer = csv.writer(file)
        i = 0
        for precinct in precinct_list:
            csv_writer.writerow([precinct[0], i])
            precinct[0] = i
            i += 1
    return precinct_list


def replace_neighbour_keys(county, candidate, precinct_list, sc_type):
    key_file = '../data/keys/' + sc_type + '/' + candidate + '/' + county + '-key'
    key_dictionary = {}
    with open(key_file) as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            key_dictionary[line[0]] = line[1]

    for precinct in precinct_list:
        neighbours = precinct[1]
        neighbours_array = neighbours.split(',')
        neighbour_keys = []
        for neighbour in neighbours_array:
            if neighbour in key_dictionary:
                neighbour_keys.append(int(key_dictionary.get(neighbour)))
        neighbour_keys.sort()
        precinct[1] = neighbour_keys

    return precinct_list


def form_simplicial_complex(county, candidate, precinct_list):
    maxDimension = 3
    adjacencies = list(map(lambda m: m[1], precinct_list))
    preferences = np.asarray(list(map(lambda m: float(m[2]), precinct_list)))
    V = []
    V = invr.incremental_vr(V, adjacencies, maxDimension)
    outputDir = '../data/sc/adj/' + candidate + '/'

    entryTimes = np.floor((1 - np.abs(preferences)) * 100 / 5)

    entryTimesSub = [entryTimes[max(simplex) - 1] for simplex in V]

    np.savetxt(outputDir + county + '_entry_times.csv', entryTimesSub,
               delimiter=' ', fmt='%i')

    phatFormatV = invr.replace_face(V)

    F = open(outputDir + county + ".dat", "w")

    for face in phatFormatV:
        F.write(str(len(face) - 1))
        if len(face) > 1:
            for simplex in face:
                F.write(" " + str(simplex))
        F.write("\n")
    F.close()


def main():
    with open('../full-list') as county_file:
        sc_type = 'adj'
        timing_csv = '../runtimes/' + sc_type + '_times.csv'
        with open(timing_csv, 'w') as timing_file:
            for county in county_file:
                county = county.split('\n')[0]
                input_csv = '../data/adjacency/' + county + '.csv'
                hillary_list, trump_list = split_precincts(input_csv, 2)
                hillary_list = generate_keys(county, 'hillary', hillary_list, sc_type)
                trump_list = generate_keys(county, 'trump', trump_list, sc_type)
                hillary_list = replace_neighbour_keys(county, 'hillary', hillary_list, sc_type)
                trump_list = replace_neighbour_keys(county, 'trump', trump_list, sc_type)
                start_time = time.time()
                if hillary_list:
                    form_simplicial_complex(county, 'hillary', hillary_list)
                timing_file.write(county + ',adj,hillary,' + str(time.time() - start_time) + '\n')
                start_time = time.time()
                if trump_list:
                    form_simplicial_complex(county, 'trump', trump_list)
                timing_file.write(county + ',adj,trump,' + str(time.time() - start_time) + '\n')


if __name__ == '__main__':
    main()
