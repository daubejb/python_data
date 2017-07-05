#!/usr/bin/python
import csv

# load Ken's list of stale Mojo 
mojo = open('mojo.csv')
csv_mojo = csv.reader(mojo)

# load usernames and active status 
ldap = open('LDAP_status.csv')
csv_ldap = csv.reader(ldap)

uniqueNames = [] 
tempList = []
inactiveNames = []
uniqueActiveNames = []

def getUserContent(uniqueName):
    tempList = []
    mojo.seek(0)
    for row in csv_mojo:
        if row[4] == uniqueName:
            tempList.append(row)
    return tempList

def writeUserContentToCSV(uniqueActiveName, userContents):
    tempFileName = '/home/jedaube/scratch/lists/' + uniqueActiveName + '.csv' 
    
    with open (tempFileName, 'wb') as csv_file:
        writer = csv.writer(csv_file,delimiter=',',quoting=csv.QUOTE_ALL)
        header_row = ["Mark X to keep document", "Content ID", "Content URL", \
                "Content title", "Author", "Published date", "Updated date", \
                "Parent URL", "Number of views in last year"]
        writer.writerow(header_row)
        for userContent in userContents: 
            writer.writerow(userContent)

#Create list of unique names that have stale content
uniqueNameCount = 0
for row in csv_mojo:
    if row[4] not in uniqueNames:
        uniqueNames.append(row[4])
        uniqueNameCount = uniqueNameCount + 1

#Read through LDAP file and create a list of users that are inactive
inactiveNameCount = 0
for row in csv_ldap:
    if row[1] == 'TRUE':
        inactiveNames.append(row[0])
        inactiveNameCount += 1

#cull only active names from the uniqueNames
activeNameCount = 0
for uniqueName in uniqueNames:
    if uniqueName not in inactiveNames:
        uniqueActiveNames.append(uniqueName)
        activeNameCount = activeNameCount + 1

print "{}{}".format('count of unique names on file: ',  uniqueNameCount) 

print "{}{}".format('count of inactive ldap names: ',  inactiveNameCount) 

print "{}{}".format('count of unique active names: ', activeNameCount)

#Loop through each unique name and build a file with just that data
for uniqueActiveName in uniqueActiveNames:
    userContents = []
    userContents = getUserContent(uniqueActiveName)
    writeUserContentToCSV(uniqueActiveName, userContents)
    
