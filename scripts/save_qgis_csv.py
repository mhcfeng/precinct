import csv
curr_county='097-sonoma'

layer = qgis.utils.iface.activeLayer()
features = layer.getFeatures() # Here you get a list of selected features

columns=['pct16','NEIGHBORS','Hill%2'] #here you write the columns you want to export. Or use a list with the columns

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