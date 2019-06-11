import csv
import os.path
import time
import numpy as np
import matplotlib.pyplot as plt
from osgeo import ogr, osr
import gdal
import math


def match_simplex_key(county, candidate, sc_type):
    dat_dir = '../data/sc/'+sc_type+'/'+candidate+'/'
    key_dir = '../data/keys/'+sc_type+'/'+candidate+'/'

    vertex_ids = []
    simplex_dict = {}
    try:
        with open(dat_dir + county + '.dat') as dat_file:
            i = 0
            for line in dat_file:
                line = line.split('\n')[0]
                dim = line.split(' ')[0]
                if dim == '0':
                    vertex_ids.append(i)
                elif dim == '1':
                    simplex_dict[i] = [int(v) for v in line.split(' ')[1:]]
                elif dim == '2':
                    lines = [int(v) for v in line.split(' ')[1:]]
                    vertices = [vertex for line in lines for vertex in simplex_dict[line]]
                    simplex_dict[i] = list(set(vertices))
                i = i+1

        key_list = []
        with open(key_dir + county + '-key') as key_file:
            reader = csv.reader(key_file)
            for line in reader:
                key_list.append(line[0])
        key_dict = dict(zip(vertex_ids, key_list))
        return key_dict, simplex_dict
    except IOError:
        return {}, {}


def read_results(county_csv):
    try:
        with open(county_csv) as county_file:
            reader = csv.reader(county_file)
            features = list(reader)
        return features
    except IOError:
        return []


def replace_loop_boundaries(key_dict, simplex_dict, features):
    for feature in features:
        dim = int(feature[0])
        if dim == 1:
            boundary = feature[3]
            boundary_simplices = boundary.split(' ')[0:-1]
            verts = [vert for simplex_id in boundary_simplices for vert in simplex_dict[int(simplex_id)] ]
            boundary_precincts = [key_dict[vert] for vert in list(set(verts))]
            feature[3] = ' '.join(boundary_precincts)
    return features


def replace_ids_centroids(features, county, candidate, sc_type):
    centroid_path = '../data/extractcentroids/' + county + '.csv'
    centroid_dict = {}
    with open(centroid_path) as centroid_file:
        reader = csv.reader(centroid_file)
        next(reader)
        for line in reader:
            centroid_dict[line[0]] = np.asarray([float(line[1]), float(line[2])])

    for f in features:
        if int(f[0]) == 1:
            precincts = (f[3].split(' '))
            f[3] = np.asarray([centroid_dict[p] for p in precincts])
    return features


def generate_base_image(county, candidate, max_pixels):
    shp = '../data/shapefiles/' + county + '.shp'

    source_ds = ogr.Open(shp, 1)
    source_layer = source_ds.GetLayer()

    fd = ogr.FieldDefn('r', ogr.OFTInteger)
    source_layer.CreateField(fd)
    fd2 = ogr.FieldDefn('g', ogr.OFTInteger)
    source_layer.CreateField(fd2)
    fd3 = ogr.FieldDefn('b', ogr.OFTInteger)
    source_layer.CreateField(fd3)
    source_srs = source_layer.GetSpatialRef()

    for feat in source_layer:
        hill_pct = feat.GetField('Hill%')
        r = g = b = 255
        if hill_pct>0:
            hill_grade = int(hill_pct*5)+1
            r = 255 - 22*hill_grade
            g = 255 - 12*hill_grade
            b = 255 - 7*hill_grade
        elif hill_pct<0:
            hill_grade = int(-hill_pct*5)+1
            r = 255 - 2*hill_grade
            g = 255 - 18*hill_grade
            b = 255 - 25*hill_grade
        feat.SetField('r', r)
        feat.SetField('g', g)
        feat.SetField('b', b)
        source_layer.SetFeature(feat)

    x_min, x_max, y_min, y_max = source_layer.GetExtent()
    max_cols = max_rows = max_pixels
    max_pixel_width = (x_max - x_min) / max_cols
    max_pixel_height = (y_max - y_min) / max_rows
    pixel_width = pixel_height = max(max_pixel_width, max_pixel_height)
    cols = int((x_max - x_min) / pixel_width)
    rows = int((y_max - y_min) / pixel_height)

    out_tiff = '../data/maps/' + county + '.tif'

    target_ds = gdal.GetDriverByName('Gtiff').Create(out_tiff, cols, rows, 3, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixel_width, 0, y_max, 0, -pixel_height))

    if source_srs:
        target_ds.SetProjection(source_srs.ExportToWkt())
    else:
        target_ds_srs = osr.SpatialReference()
        target_ds_srs.ImportFromEPSG(4326)
        target_ds.SetProjection(target_ds_srs.ExportToWkt())

    for i in range(3):
        band = target_ds.GetRasterBand(i+1)
        band.SetNoDataValue(255)

    gdal.RasterizeLayer(target_ds, [1], source_layer, options=["ATTRIBUTE=%s" % "r"])
    gdal.RasterizeLayer(target_ds, [2], source_layer, options=["ATTRIBUTE=%s" % "g"])
    gdal.RasterizeLayer(target_ds, [3], source_layer, options=["ATTRIBUTE=%s" % "b"])
    target_ds = None

    source_ds = None

    source_ds = gdal.OpenEx(shp, gdal.OF_VECTOR | gdal.OF_UPDATE)
    source_ds.ExecuteSQL("ALTER TABLE "+county+" DROP COLUMN r")
    source_ds.ExecuteSQL("ALTER TABLE "+county+" DROP COLUMN g")
    source_ds.ExecuteSQL("ALTER TABLE "+county+" DROP COLUMN b")

    source_ds = None


def check_clockwise_angle(point):
    point = np.asarray(point)
    lenvector = np.sqrt(np.sum(np.power(point,2)))
    if lenvector == 0:
        return -math.pi, 0
    normalized = point/lenvector
    refvec = np.asarray([0, 1])
    dotprod = np.dot(normalized, refvec)
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]
    angle = math.atan2(diffprod, dotprod)
    if angle < 0:
        return 2*math.pi + angle, lenvector
    return angle, lenvector


def gen_clockwise_around_centroid(xdata, ydata):
    n = len(xdata)
    centroid = np.asarray([np.sum(xdata)/n, np.sum(ydata)/n])
    points = [list(item) for item in zip(xdata-centroid[0], ydata-centroid[1])]
    sorted_pts = sorted(points, key=check_clockwise_angle)
    return np.asarray([np.asarray(item)+centroid for item in sorted_pts])


def read_ls_loops(county, candidate, features, immediate_only = True):
    img_path = '../data/maps/' + county + '.tif'
    img_array = plt.imread(img_path)
    (rows, cols, bands) = img_array.shape
    dim_1_features = [f for f in features if f[0]=='1']
    fig, ax = plt.subplots()
    ax.imshow(img_array, extent = [0, cols, 0, rows])
    for f in dim_1_features:
        entry_time = int(f[1])
        boundary = f[3].split(' ')
        boundary = np.asarray([int(b) for b in boundary])
        persistence = (20 - (int(f[2])-int(f[1])))/20
        persistence_scaling = int(persistence*5)
        if candidate == 'hillary':
                r = 65 - persistence_scaling*12
                g = 148 - persistence_scaling*20
                blue = 197 - persistence_scaling*20
        elif candidate == 'trump':
                r = 213 - persistence_scaling*22
                g = 95 - persistence_scaling*19
                blue = 76 - persistence_scaling*9
        ydata = rows - (boundary/cols).astype(np.int)
        xdata = boundary%cols
        ordered_xy = gen_clockwise_around_centroid(xdata, ydata)
        xdata = ordered_xy[:,0]
        xdata = np.append(xdata, xdata[0])
        ydata = ordered_xy[:,1]
        ydata = np.append(ydata, ydata[0])
        color_tuple = (r/255,g/255,blue/255)
        if (immediate_only and entry_time==0) or not immediate_only :
            ax.plot(xdata,ydata, linewidth=2*(persistence_scaling/5), color=color_tuple)

    # fig.patch.set_visible(False)
    ax.axis('off')
    output_file = '../results/maps/ls/' + candidate + '/' + county + '.png'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close(fig)



def read_centroid_loops(county, candidate, features, sc_type, max_pixels):
    shp = '../data/shapefiles/' + county + '.shp'

    source_ds = ogr.Open(shp, 1)
    source_layer = source_ds.GetLayer()

    x_min, x_max, y_min, y_max = source_layer.GetExtent()
    max_cols = max_rows = max_pixels
    max_pixel_width = (x_max - x_min) / max_cols
    max_pixel_height = (y_max - y_min) / max_rows
    pixel_width = pixel_height = max(max_pixel_width, max_pixel_height)

    source_ds = None

    translation = np.transpose(np.asarray([x_min, y_min]))
    affine = np.asarray([[pixel_width, 0], [0, pixel_height]])

    img_path = '../data/maps/' + county + '.tif'
    img_array = plt.imread(img_path)
    (rows, cols, bands) = img_array.shape
    fig, ax = plt.subplots()
    ax.imshow(img_array, extent = [0, cols, 0, rows])

    deaths = [int(f[2]) for f in features]
    max_persistence = max(deaths)

    for f in features:
        if f[0] == '1':
            f[3] = np.transpose((np.linalg.inv(affine)@np.transpose(f[3]-translation)).astype(int))

            persistence = int(f[2])-int(f[1])
            persistence_scaling = int((max_persistence - persistence)/(max_persistence)*5)
            persistence_scaling = max(0, persistence_scaling)
            persistence_scaling = min(persistence_scaling, 5)

            if candidate == 'hillary':
                r = 65 - persistence_scaling*12
                g = 148 - persistence_scaling*20
                blue = 197 - persistence_scaling*20
            elif candidate == 'trump':
                r = 213 - persistence_scaling*22
                g = 95 - persistence_scaling*19
                blue = 76 - persistence_scaling*9

            xdata = (f[3])[:, 0]
            ydata = (f[3])[:, 1]
            ordered_xy = gen_clockwise_around_centroid(xdata, ydata)
            xdata = ordered_xy[:,0]
            xdata = np.append(xdata, xdata[0])
            ydata = ordered_xy[:,1]
            ydata = np.append(ydata, ydata[0])
            color_tuple = (r/255, g/255, blue/255)
            ax.plot(xdata,ydata, linewidth=(persistence_scaling/5+1), color=color_tuple)

    ax.axis('off')
    output_file = '../results/maps/' + sc_type + '/' + candidate + '/' + county + '.png'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close(fig)


def post_processing(county, candidate, sc_type):
    if sc_type in ['adj', 'alpha', 'rips', 'ls']:
        timing_csv = '../runtimes/post_time.csv'
        with open(timing_csv, 'w+') as timing_file:
            start_time = time.time()
            key_dict, simplex_dict = match_simplex_key(county, candidate, sc_type)

            base_map_path = '../data/maps/' + county + '.tif'
            if not os.path.isfile(base_map_path):
                generate_base_image(county, candidate, 250)

            result_dir = '../results/' + sc_type + '/' + candidate+ '/'
            if os.path.isfile(result_dir + county + '.csv'):
                features = read_results(result_dir + county + '.csv')
                if features:
                    features = replace_loop_boundaries(key_dict, simplex_dict, features)
                    if sc_type in ['adj', 'alpha', 'rips']:
                        features = replace_ids_centroids(features, county, candidate, sc_type)
                        read_centroid_loops(county, candidate, features, sc_type, 250)
                    elif sc_type in ['ls']:
                        read_ls_loops(county, candidate, features)
                    # with open(result_dir + county + '_replaced_id.csv', 'w') as output_file:
                    #     csv_writer = csv.writer(output_file)
                    #     csv_writer.writerows(features)
            # timing_file.write(county + ',' + sc_type + ',' + candidate + ',' + str(time.time() - start_time))


def main():
    with open('../full-list') as county_file:
        # for county in county_file:
        for county in ['025-imperial', '037-los-angeles', '055-napa', '107-tulare']:
            # county = county.split('\n')[0]
            for candidate in ['hillary', 'trump']:
            # for candidate in ['hillary']:
            #     for sc_type in ['adj', 'alpha', 'rips','ls']:
                for sc_type in ['adj', 'alpha', 'rips', 'ls']:
                    post_processing(county, candidate, sc_type)


if __name__ == '__main__':
    main()
