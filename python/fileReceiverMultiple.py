#!/usr/bin/env python3

#Sanitization needs to be implemented, basic functionality currently.

import cgi, os

print('Content-Type: text/html')
print()

formData = cgi.FieldStorage()

def addFileToFilesystem(fileitem):
    fn = os.path.basename(fileitem.filename)
    file = fileitem.file
    saveFile = open("uploads/%s"%fn, 'wb+')
    #make this grab maybe 50KB then write 50KB and so on to 
    #increase disk efficiency
    for data in file:
        saveFile.write(data)
    saveFile.close()

def processFormData(number_of_files):
    for i in range(number_of_files):
        fileitem = formData['file[%d]'%i]
        #if its a file & is of type pdf
        if fileitem.file and fileitem.filename.split(".")[-1]=="pdf":
            addFileToFilesystem(fileitem)

if len(formData)!=0:
    processFormData(len(formData))
