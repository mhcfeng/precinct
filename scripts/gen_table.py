import csv

with open('junk.fin') as file:
    csv_reader = csv.reader(file)
    for line in csv_reader:
        county_name = line[0].split('-')
        county_name_str = ' '.join(county_name[1:3])
        county_name_str = county_name_str.title()
        print(county_name_str + ' & %.3g s & %.3g s & %.3g s & %.3g s & %.3g s & %.3g s & %.3g s & %.3g s \\\\' %(float(line[1]),float(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6]), float(line[7]), float(line[8])))