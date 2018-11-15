import csv
import sys

# This script inserts a column of data from stdin into the data column of the
# specified csv file, and outputs the modified CSV file to stdout. Run this
# script with
#
# python col2csv.py [csv-file] [dataset-name] [division-factor]
#
# The division factor is optional, and defaults to 1.0

new_data_col = []
division_factor = 1.0

if len(sys.argv) > 3:
    division_factor = float(sys.argv[3])

while True:

    col_entry = sys.stdin.readline()

    if col_entry == "":
        break
    
    col_entry = col_entry.replace("\n", "")

    new_data_col.append(str(float(col_entry)/division_factor))

with open(sys.argv[1], 'r', newline='') as csvfile:

    reader = csv.reader(csvfile)
    firstrow = True
    rownum = 0 

    for row in reader:

        for col_i in range(len(row)):

            if col_i != 2:
                print(row[col_i], end='')
            else:

                if firstrow:
                    print(sys.argv[2], end='')
                    firstrow = False
                else:
                    print(new_data_col[rownum-1], end='')
            
            if col_i != len(row) - 1:
                print(",",end="")
        
        print("")
        
        rownum += 1
