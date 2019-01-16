from qgis.core import QgsField, QgsExpression, QgsFeature
from qgis.utils import iface
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import (QgsGraduatedSymbolRendererV2, QgsSymbolV2, QgsRendererRangeV2)
from qgis.core import *
from qgis.gui import *
import csv
import sys

# TODO: Split this into smaller methods and then create a main
def saveMap():
    qgis.utils.iface.mapCanvas().saveAsImage("/Users/michellefeng/Documents/research/precinct/data/maps/"+curr_county+'.png')

QgsMapLayerRegistry.instance().removeAllMapLayers()
curr_county='001-alameda'
print curr_county
shp = QgsVectorLayer('/Users/michellefeng/Documents/research/precinct/data/shapefiles/'+curr_county+'.shp',curr_county,'ogr')
if not shp.isValid():
  print "Layer failed to load!"
QgsMapLayerRegistry.instance().addMapLayer(shp)
csvfile = QgsVectorLayer('/Users/michellefeng/Documents/research/precinct/data/final-results/'+curr_county+'.csv', 'csv', 'delimitedtext')
QgsMapLayerRegistry.instance().addMapLayer(csvfile)

shpField='pct16'
csvField='pct16'
joinObject = QgsVectorJoinInfo()
joinObject.joinLayerId = csvfile.id()
joinObject.joinFieldName = csvField
joinObject.targetFieldName = shpField
joinObject.memoryCache = True
shp.addJoin(joinObject)

shp.startEditing()

#step 1
myField = QgsField( 'Hill%', QVariant.Double)
shp.addAttribute( myField )
idx = shp.fieldNameIndex( 'Hill%' )

#step 2
e = QgsExpression( 'if("csv_pres_clinton" + "csv_pres_trump">0,("csv_pres_clinton"-"csv_pres_trump")/("csv_pres_clinton"+"csv_pres_trump"),0)' )
e.prepare( shp.pendingFields() )

for f in shp.getFeatures():
    f[idx] = e.evaluate( f )
    shp.updateFeature( f )

shp.commitChanges()
shp.startEditing()

#step 1
myField = QgsField( 'X', QVariant.Double)
myField2 = QgsField( 'Y', QVariant.Double)
shp.addAttribute( myField )
shp.addAttribute( myField2 )
idx = shp.fieldNameIndex( 'X' )
idx2 = shp.fieldNameIndex( 'Y' )

#step 2
for f in shp.getFeatures():
    f[idx] = f.geometry().centroid().asPoint().x()
    f[idx2] = f.geometry().centroid().asPoint().y()
    shp.updateFeature( f )

shp.commitChanges()

################################################################################
# Copyright 2014 Ujaval Gandhi
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
################################################################################


# Replace the values below with values from your layer.
# For example, if your identifier field is called 'XYZ', then change the line
# below to _NAME_FIELD = 'XYZ'
_NAME_FIELD = 'pct16'
# Replace the value below with the field name that you want to sum up.
# For example, if the # field that you want to sum up is called 'VALUES', then
# change the line below to _SUM_FIELD = 'VALUES'
_SUM_FIELD = 'area'

# Names of the new fields to be added to the layer
_NEW_NEIGHBORS_FIELD = 'NEIGHBORS'
_NEW_SUM_FIELD = 'SUM'

layer = shp

# Create 2 new fields in the layer that will hold the list of neighbors and sum
# of the chosen field.
layer.startEditing()
layer.dataProvider().addAttributes(
        [QgsField(_NEW_NEIGHBORS_FIELD, QVariant.String),
         QgsField(_NEW_SUM_FIELD, QVariant.Int)])
layer.updateFields()
# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

# Build a spatial index
index = QgsSpatialIndex()
for f in feature_dict.values():
    index.insertFeature(f)

# Loop through all features and find features that touch each feature
for f in feature_dict.values():
    print 'Working on %s' % f[_NAME_FIELD]
    geom = f.geometry()
    # Find all features that intersect the bounding box of the current feature.
    # We use spatial index to find the features intersecting the bounding box
    # of the current feature. This will narrow down the features that we need
    # to check neighboring features.
    intersecting_ids = index.intersects(geom.boundingBox())
    # Initalize neighbors list and sum
    neighbors = []
    neighbors_sum = 0
    for intersecting_id in intersecting_ids:
        # Look up the feature from the dictionary
        intersecting_f = feature_dict[intersecting_id]

        # For our purpose we consider a feature as 'neighbor' if it touches or
        # intersects a feature. We use the 'disjoint' predicate to satisfy
        # these conditions. So if a feature is not disjoint, it is a neighbor.
        if (f != intersecting_f and
            not intersecting_f.geometry().disjoint(geom)):
            neighbors.append(intersecting_f[_NAME_FIELD])
            neighbors_sum += intersecting_f[_SUM_FIELD]
    f[_NEW_NEIGHBORS_FIELD] = ','.join(neighbors)
    f[_NEW_SUM_FIELD] = neighbors_sum
    # Update the layer with new attribute values.
    layer.updateFeature(f)

layer.commitChanges()
print 'Processing complete.'


features = layer.getFeatures() # Here you get a list of selected features

columns=['pct16','NEIGHBORS','Hill%'] #here you write the columns you want to export. Or use a list with the columns

# Here you write for every selected feature a list with only the columsn you have defined
filteredFields = []    
for feature in features:
    attrs = [feature[column] for column in columns]
    filteredFields.append(attrs)

# Now you can write the filterField list with the list of selected attributes into your csv file.
with open('/Users/michellefeng/Documents/research/precinct/data/adjacency/'+curr_county+'.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',') #as delimiter you can use other character as well
    writer.writerow([u'pct16',u'NEIGHBORS','HILLPCT'])
    for field in filteredFields:
        writer.writerow(field)

features = layer.getFeatures() # Here you get a list of selected features

columns=['pct16','X','Y','Hill%'] #here you write the columns you want to export. Or use a list with the columns

# Here you write for every selected feature a list with only the columsn you have defined
filteredFields = []    
for feature in features:
    attrs = [feature[column] for column in columns]
    filteredFields.append(attrs)
    
with open('/Users/michellefeng/Documents/research/precinct/data/extractcentroids/'+curr_county+'.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',') #as delimiter you can use other character as well
    writer.writerow([u'pct16',u'X',u'Y','HILLPCT'])
    for field in filteredFields:
        writer.writerow(field)


targetField = "Hill%"
rangeList = []

values = (
    ('-1 - -.75', -1, -.75, QColor('#ef8a62')),
    ('-.75 - -.5', -.75, -.5, QColor('#f1a587')),
    ('-.5 - -.25', -.5, -.25, QColor('#f3c0ac')),
    ('-.25 - 0', -.25, -0.001, QColor('#f5dbd1')),
    ('0', -0.001, 0.001, QColor('#f7f7f7')),
    ('0 - .25', 0.001, .25, QColor('#d3e3ed')),
    ('.25 - .5', .25, .5, QColor('#afd0e3')),
    ('.5 - .75', .5, .75, QColor('#8bbcd9')),
    ('.75 - 1', .75, 1.0, QColor('#67a9cf')),
)

for label, min, max, color in values:
    symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
    symbol.setColor(color)
    rng = QgsRendererRangeV2(min, max, symbol, label)
    rangeList.append(rng)
    
renderer = QgsGraduatedSymbolRendererV2( targetField, rangeList )
renderer.setMode(QgsGraduatedSymbolRendererV2.Custom)
layer.setRendererV2(renderer)

iface.mapCanvas().refreshAllLayers()

img = QImage(QSize(800, 600), QImage.Format_ARGB32_Premultiplied)

# set image's background color
color = QColor(255, 255, 255)
img.fill(color.rgb())

# create painter
p = QPainter()
p.begin(img)
p.setRenderHint(QPainter.Antialiasing)

render = QgsMapRenderer()

# set layer set
lst = [layer.id()]  # add ID of every layer
render.setLayerSet(lst)

# set extent
rect = QgsRectangle(render.fullExtent())
rect.scale(1.1)
render.setExtent(rect)

# set output size
render.setOutputSize(img.size(), img.logicalDpiX())

# do the rendering
render.render(p)

p.end()

# save image
#img.save("/Users/michellefeng/Documents/research/precinct/data/maps/"+curr_county+".png","png")

QTimer.singleShot(10000, saveMap)


layer.startEditing()
layer.deleteAttribute(layer.fieldNameIndex('NEIGHBORS'))
layer.deleteAttribute(layer.fieldNameIndex('SUM'))
#layer.deleteAttribute(layer.fieldNameIndex('Hill%'))
#layer.deleteAttribute(layer.fieldNameIndex('X'))
#layer.deleteAttribute(layer.fieldNameIndex('Y'))
layer.commitChanges()

def main():
    pass

if __name__ == '__main__':
    main()
