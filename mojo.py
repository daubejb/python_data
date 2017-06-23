import csv
mojo = open('test.csv')
csv_mojo = csv.reader(mojo)


uniqueNames = [] 
tempList = []

def getUserContent(uniqueName):
    tempList = []
    mojo.seek(0)
    for row in csv_mojo:
        if row[3] == uniqueName:
            tempList.append(row)
    return tempList

def writeUserContentToCSV(uniqueName, userContents):
    tempFileName = '/home/jedaube/scratch/lists/' + uniqueName + '.csv' 
    
    with open (tempFileName, 'wb') as csv_file:
        writer = csv.writer(csv_file,delimiter=',',quoting=csv.QUOTE_ALL)
        for userContent in userContents: 
            writer.writerow(userContent)
    


#Create list of unique names
for row in csv_mojo:
    if row[3] not in uniqueNames:
        uniqueNames.append(row[3])

#Loop through each unique name and build a file with just that data
print uniqueNames
for uniqueName in uniqueNames:
    userContents = []
    userContents = getUserContent(uniqueName)
    writeUserContentToCSV(uniqueName, userContents)
    


