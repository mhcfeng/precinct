import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import collections as mc
from matplotlib.patches import Polygon
import os


def read_dat(county, candidate, sc_type):
    dat_path = '../data/sc/' + sc_type + '/' + candidate + '/' + county + '.dat'
    entry_times_path = '../data/sc/' + sc_type + '/' + candidate + '/' + county + '_entry_times.csv'

    vertices = {}
    edges = {}
    faces = {}
    vertex_idx = 0
    simplex_idx = 0
    with open(dat_path) as dat_file:
        for line in dat_file:
            line = line.split('\n')[0]
            line = line.split(' ')
            if line[0] == '0':
                vertices[simplex_idx] = vertex_idx
                vertex_idx += 1
            elif line[0] == '1':
                edges[simplex_idx] = [int(v) for v in line[1:]]
            elif line[0] == '2':
                faces[simplex_idx] = [int(s) for s in line[1:]]
            simplex_idx += 1

    entry_times = []
    with open(entry_times_path) as entry_times_csv:
        csv_reader = csv.reader(entry_times_csv)
        for line in csv_reader:
            entry_times.append(int(line[0]))
    return vertices, edges, faces, entry_times


def get_vertex_coords_and_colors(vertices, county, candidate, sc_type, entry_times):
    key_path = '../data/keys/' + sc_type + '/' + candidate + '/' + county + '-key'
    precinct_key = {}
    with open(key_path) as key_csv:
        csv_reader = csv.reader(key_csv)
        for line in csv_reader:
            precinct_key[int(line[1])] = line[0]

    vertex_coords = {}
    if sc_type != 'ls':
        centroid_path = '../data/extractcentroids/' + county + '.csv'
        with open(centroid_path) as centroid_csv:
            csv_reader = csv.reader(centroid_csv)
            next(csv_reader)
            for line in csv_reader:
                if line[0] in precinct_key.values():
                    vertex_coords[line[0]] = np.asarray([float(line[1]), float(line[2])])
    else:
        img_path = '../data/tif/' + candidate + '/' + county + '.tif'
        img_array = plt.imread(img_path)
        rows, cols = img_array.shape
        vertex_coords_idx = np.asarray([int(coord) for coord in precinct_key.values()])
        vertex_y = (vertex_coords_idx/cols).astype(int)
        vertex_x = vertex_coords_idx%cols
        for i in range(len(vertex_coords_idx)):
            vertex_coords[str(vertex_coords_idx[i])] = np.asarray([vertex_x[i], -vertex_y[i]])

    c = np.linspace(0,1,max(entry_times)+1)
    vertex_colors = [c[entry_times[simplex_id]] for simplex_id in vertices.keys()]

    return precinct_key, vertex_coords, vertex_colors


def get_edge_coords_and_colors(edges, vertices, precinct_key, vertex_coords, entry_times):
    line_coords = []
    edge_colors = []
    c = np.linspace(0,1,max(entry_times)+1)
    for e in edges.keys():
        next_line = np.asarray([vertex_coords[precinct_key[vertices[v]]] for v in edges[e]])
        line_coords.append(next_line)
        edge_colors.append(c[entry_times[e]])

    viridis = cm.get_cmap('viridis', 12)
    edge_rgba = [viridis(color) for color in edge_colors]
    edge_collection = mc.LineCollection(line_coords, colors=edge_rgba, linewidths=0.3)
    return edge_collection


def get_edge_coords_and_colors_by_time(edges, vertices, precinct_key, vertex_coords, entry_times, T):
    line_coords = []
    edge_colors = []
    c = np.linspace(0,1,max(entry_times)+1)
    for e in edges.keys():
        if entry_times[e] == T:
            next_line = np.asarray([vertex_coords[precinct_key[vertices[v]]] for v in edges[e]])
            line_coords.append(next_line)
            edge_colors.append(c[entry_times[e]])

    viridis = cm.get_cmap('viridis', 12)
    edge_rgba = [viridis(color) for color in edge_colors]
    edge_collection = mc.LineCollection(line_coords, colors=edge_rgba, linewidths=0.3)
    return edge_collection


def get_face_coords_and_colors(faces, vertices, edges, precinct_key, vertex_coords, entry_times):
    face_colors = []
    c =np.linspace(0,1,max(entry_times)+1)
    patches = []
    for f in faces.keys():
        vertex_ids = list(set(sum([edges[e] for e in faces[f]],[])))
        current_face = Polygon(np.asarray([vertex_coords[precinct_key[vertices[v]]] for v in vertex_ids]), True)
        patches.append(current_face)
        face_colors.append(c[entry_times[f]])

    viridis = cm.get_cmap('viridis', 12)
    face_rgba = [viridis(color) for color in face_colors]
    face_collection = mc.PatchCollection(patches, alpha=1, facecolors=face_rgba)

    return face_collection


def get_face_coords_and_colors_by_time(faces, vertices, edges, precinct_key, vertex_coords, entry_times, T):
    face_colors = []
    c =np.linspace(0,1,max(entry_times)+1)
    patches = []
    for f in faces.keys():
        if entry_times[f] == T:
            vertex_ids = list(set(sum([edges[e] for e in faces[f]],[])))
            current_face = Polygon(np.asarray([vertex_coords[precinct_key[vertices[v]]] for v in vertex_ids]), True)
            patches.append(current_face)
            face_colors.append(c[entry_times[f]])

    viridis = cm.get_cmap('viridis', 12)
    face_rgba = [viridis(color) for color in face_colors]
    face_collection = mc.PatchCollection(patches, alpha=1, facecolors=face_rgba)

    return face_collection


def visualize_simplicial_complex(county, candidate, sc_type, animate = False):
    vertices, edges, faces, entry_times = read_dat(county, candidate, sc_type)
    precinct_key, vertex_coords, vertex_colors = get_vertex_coords_and_colors(vertices, county, candidate, sc_type, entry_times)
    vertex_coords_array = np.asarray([v for v in vertex_coords.values()])

    viridis = cm.get_cmap('viridis', max(entry_times)+1)
    cmap_idx = np.linspace(0, 1, max(entry_times)+1)

    if animate:
        fig, ax = plt.subplots()
        # ax.axis('off')
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        total_T = max(entry_times)
        steps = 3
        increment = int(total_T/steps)

        for T in range(max(entry_times)+1):
            curr_color = viridis(cmap_idx[T])

            outdir = '../vis/sc/' + sc_type + '/' + candidate + '/' + county + '/'
            if not os.path.isdir(outdir):
                os.makedirs(outdir)
            outfile = outdir + str(int(T/increment)) + '.png'

            current_vertex_coords_array = []
            for v in vertices.keys():
                if entry_times[v] == T:
                    current_vertex_coords_array.append(np.asarray(vertex_coords[precinct_key[vertices[v]]]))

            if current_vertex_coords_array:
                current_vertex_coords_array = np.asarray(current_vertex_coords_array)
                ax.scatter(current_vertex_coords_array[:,0], current_vertex_coords_array[:,1], color=curr_color)

            curr_edge_collection = get_edge_coords_and_colors_by_time(edges, vertices, precinct_key, vertex_coords, entry_times, T)
            ax.add_collection(curr_edge_collection)

            curr_face_collection = get_face_coords_and_colors_by_time(faces, vertices, edges, precinct_key, vertex_coords, entry_times, T)
            ax.add_collection(curr_face_collection)

            if T%increment == 0:
                plt.savefig(outfile, bbox_inches='tight')

        plt.close(fig)

    else:
        edge_collection = get_edge_coords_and_colors(edges, vertices, precinct_key, vertex_coords, entry_times)

        face_collection = get_face_coords_and_colors(faces, vertices, edges, precinct_key, vertex_coords, entry_times)

        fig, ax = plt.subplots()
        # ax.axis('off')
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        vertex_rgba = [viridis(color) for color in vertex_colors]
        ax.scatter(vertex_coords_array[:,0], vertex_coords_array[:,1], color=vertex_rgba)
        ax.add_collection(edge_collection)
        ax.add_collection(face_collection)

        outdir = '../vis/sc/' + sc_type + '/' + candidate + '/'
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        outfile = outdir + county + '.png'
        plt.savefig(outfile, bbox_inches='tight')
        plt.close(fig)

def main():
    for county in ['025-imperial']:
        for candidate in ['hillary', 'trump']:
            for sc_type in ['ls']:
                visualize_simplicial_complex(county, candidate, sc_type, True)


if __name__ == '__main__':
    main()
