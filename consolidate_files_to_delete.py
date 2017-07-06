#!/usr/bin/python

import os
import csv

#variables
DIRECTORY_OF_CSV_FILES = '/home/jedaube/scratch/download_test/'
rows_to_write_to_csv = []
FINAL_FILE_FOR_CROWN = '/home/jedaube/scratch/final_file/file_for_crown.csv'

for filename in os.listdir(DIRECTORY_OF_CSV_FILES):
    file = open(DIRECTORY_OF_CSV_FILES + filename)
    csv_file = csv.reader(file)
    for row in csv_file:
        if (row[0] == ''):
            rows_to_write_to_csv.append(row)

with open (FINAL_FILE_FOR_CROWN, 'wb') as csv_file:
    writer = csv.writer(csv_file,delimiter=',',quoting=csv.QUOTE_ALL)
    header_row = ["Mark X to keep document", "Content ID", "Content URL", \
                  "Content title", "Author", "Published date", "Updated date", \
                  "Parent URL", "Number of views in last year"]
    writer.writerow(header_row)
    for row in rows_to_write_to_csv:
        writer.writerow(row)
    




