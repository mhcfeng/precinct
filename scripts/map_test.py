from qgis.utils import iface
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import (QgsGraduatedSymbolRendererV2, QgsSymbolV2, QgsRendererRangeV2)
from qgis.core import *
from qgis.gui import *

layer = iface.activeLayer()

file = open("/Users/michellefeng/Documents/research/precinct/results/adjacency/hill/025-imperial-loops","r")
lines = file.read().split("\n")
ids = []
for line in lines[0:len(lines)-1]:
    precincts = line.split(" ")
    precincts = precincts[0:len(precincts)-1]
    if len(precincts) >= 3:
        for precinct in precincts:
            for f in layer.getFeatures():
                if f['pct16'] == precinct:
                    ids.append(f.id())
        iface.mapCanvas().setSelectionColor( QColor("#053061") )
        layer.setSelectedFeatures( ids )
        layer.triggerRepaint()
