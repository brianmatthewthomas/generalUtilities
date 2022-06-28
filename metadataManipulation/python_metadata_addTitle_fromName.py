import os
import shutil
import lxml.etree as ET
from preservation_utilities import preservation_utilities

print("this will add a dcterms:title tag to a file")
print("this is based on the item name in the regular file") 
print("so if that isn't what you want don't run this script")
print("files to upload corrections on will be added to the correcto directory")
print("")
walker = input("directory to add titles to: ")
output = input("directory to copy updated files to: ")
logger = open("log_titleAddedto.txt", "a")
counter = 0
for dirpath, dirnames, filenames in os.walk(walker):
	for filename in filenames:
		if "metadata" in filename:
			filename1 = os.path.join(dirpath, filename)
			filename2 = os.path.join(output, filename)
			with open(filename1, "r") as f:
				filedata = f.read()
				if "title>" not in filedata:
					print(filename1, "missing title, adding")
					file2 = filename1[:-15] + ".xml"
					dom = ET.parse(file2)
					#construct the namespaces for later on
					root = dom.getroot()
					namespaces = root.nsmap
					namespaces['xmlns'] = namespaces[None]
					namespaces.pop(None,None)
					namespaces['dcterms'] = "http://dublincore.org/documents/dcmi-terms/"
					namespaces['tslac'] = 'https://www.tsl.texas.gov/'
					namespaces['MetadataResponse'] = namespaces['xmlns']
					namespaces['EntityResponse'] = namespaces['xmlns']
					namespaces['ChildrenResponse'] = namespaces['xmlns']
					title = dom.find(".//xip:Title", namespaces=namespaces).text
					if len(title) < 9:
						title2 = title
					else:
						title2 = title[:-3]
					filedata = filedata.replace("</dcterms:dcterms>","<dcterms:title>" + title + "</dcterms:title></dcterms:dcterms>")
					with open(filename1, "w") as w:
						w.write(filedata)
						w.close()
						logger.write(filename1 + "\n")
						preservation_utilities.dirMaker(filename2)
						shutil.copy(filename1,filename2)
						print(filename1,"processed")
						counter = counter + 1
logger.close()
print("all done")
print(counter,"files updated")