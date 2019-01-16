from qgis.utils import iface
from PyQt4.QtCore import QVariant

shp = iface.activeLayer()

shp.startEditing()

#step 1
myField = QgsField( 'Hill%2', QVariant.Double)
shp.addAttribute( myField )
idx = shp.fieldNameIndex( 'Hill%2' )

#step 2
e = QgsExpression( 'if("csv_pres_clinton" + "csv_pres_trump">0,("csv_pres_clinton"-"csv_pres_trump")/("csv_pres_clinton"+"csv_pres_trump"),0)' )
e.prepare( shp.pendingFields() )

for f in shp.getFeatures():
    f[idx] = e.evaluate( f )
    shp.updateFeature( f )

shp.commitChanges()