from qgis.core import QgsField, QgsExpression, QgsFeature
from qgis.utils import iface
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import (QgsGraduatedSymbolRendererV2, QgsSymbolV2, QgsRendererRangeV2)
from qgis.core import *
from qgis.gui import *
import os.path

with open('/Users/michellefeng/Documents/research/precinct/remaining-list') as countylist:
    for county in countylist:
        county=county.split('\n')[0]
        for candidate in ['hillary','trump']:
            for type in ['adj', 'alpha', 'rips']:
                print(county, candidate, type)
                QgsMapLayerRegistry.instance().removeAllMapLayers()
                shp = QgsVectorLayer('/Users/michellefeng/Documents/research/precinct/data/shapefiles/'+county+'.shp',county,'ogr')
                if not shp.isValid():
                  print "Layer failed to load!"
                QgsMapLayerRegistry.instance().addMapLayer(shp)
                csvfile = QgsVectorLayer('/Users/michellefeng/Documents/research/precinct/data/final-results/'+county+'.csv', 'csv', 'delimitedtext')
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

                layer=shp

                targetField = "Hill%"
                rangeList = []

                values = (
                    ('-1 - -.75', -1, -.75, QColor('#f3c0ac')),
                    ('-.75 - -.5', -.75, -.5, QColor('#f4cdbe')),
                    ('-.5 - -.25', -.5, -.25, QColor('#f5dbd1')),
                    ('-.25 - 0', -.25, -0.001, QColor('#f6e9e4')),
                    ('0', -0.001, 0.001, QColor('#f7f7f7')),
                    ('0 - .25', 0.001, .25, QColor('#e5edf2')),
                    ('.25 - .5', .25, .5, QColor('#d3e3ed')),
                    ('.5 - .75', .5, .75, QColor('#c1d9e8')),
                    ('.75 - 1', .75, 1.0, QColor('#afd0e3')),
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
                path = "/Users/michellefeng/Documents/research/precinct/results/"+type+"/"+candidate+"/"

                hillColour = QColor("#053061")
                trumpColour = QColor("#67001f")
                ids = []
                if os.path.isfile(path + county + '_replaced_id.csv'):
                    with open(path + county + '_replaced_id.csv') as loop_file:
                        for line in loop_file:
                            line = line.split('\n')[0]
                            precincts = line.split(',')[3]
                            precincts = precincts.split(' ')
                            if len(precincts) >= 3:
                                for precinct in precincts:
                                    for f in layer.getFeatures():
                                        if f['pct16'] == precinct:
                                            ids.append(f.id())

                    if candidate == 'trump':
                        iface.mapCanvas().setSelectionColor( trumpColour )
                    elif candidate == 'hillary':
                        iface.mapCanvas().setSelectionColor( hillColour )
                    layer.setSelectedFeatures( ids )
                    layer.triggerRepaint()

                    img = QImage(QSize(800, 600), QImage.Format_ARGB32_Premultiplied)

                    # set image's background color
                    color = QColor(255, 255, 255)
                    img.fill(color.rgb())

                    iface.mapCanvas().resize(QSize(1280,960 ))
                    canvas = iface.mapCanvas()
                    canvas.setCanvasColor(Qt.white)
                    canvas.enableAntiAliasing(True)
                    canvas.setExtent(layer.extent())
                    canvas.setLayerSet([QgsMapCanvasLayer(layer)])
                    settings = canvas.mapSettings()
                    job = QgsMapRendererSequentialJob(settings)
                    job.start()
                    job.waitForFinished()
                    img = job.renderedImage()
                    map_path = "/Users/michellefeng/Documents/research/precinct/results/maps/"+type+"/"+candidate+"/"
                    img.save(map_path +county+".png",'png')


