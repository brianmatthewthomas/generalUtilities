# program will take user input to iterate over many files,
# locate a specific term and apply a transform as a result
# all inapplicable files are left alone
# to know what files were affected look at the last modified date

# may in the future need to improve iteration over directories
import os, sys, csv
import lxml.etree as ET
from openpyxl import Workbook
import time

def getNamespaces(root):
    namespaces = root.nsmap
    namespaces['xmlns'] = namespaces[None]
    namespaces.pop(None, None)
    namespaces['dcterms'] = "http://dublincore.org/documents/dcmi-terms/"
    namespaces['tslac'] = 'https://www.tsl.texas.gov/'
    namespaces['MetadataResponse'] = namespaces['xmlns']
    namespaces['EntityResponse'] = namespaces['xmlns']
    namespaces['ChildrenResponse'] = namespaces['xmlns']
    return namespaces

#remind user what they need to do before proceeding
print("If you do not pay attention to the above everything will go wrong and I will slap you with a fish")

#user-defined inputs
seriousFilepath = input("path to harvested files: ")
workbookfilename = input("excel filename with relative filepath: ")
worksheetName = input("excel worksheet name, Sheet1 if for UUIDs: ")
collectionName = input("collection name: ")
type = input("LSTA? y/n: ")
if type == "y":
	type1 = "LSTA"
else:
	type1 = "Born-digital"
wb = Workbook(workbookfilename)
ws = wb.create_sheet(worksheetName)
processed = 0
# total file count inspected
total = 0

# to document the tag being searched
print()
print("initiating UUID collection")
ws.append(['UUIDs', 'filename'])
ws.append([collectionName,type1])
dir = ""
folderCount = 0
for dirpath, dirnames, filenames in os.walk(seriousFilepath):
	# load directory to crawl
	for filename in filenames:
		filename  = os.path.join(dirpath, filename)
		if filename.endswith((".xml")):
			total = total + 1
			if dir != dirpath:
				current = time.asctime()
				print(dirpath,"started at",current)
				dir = dirpath
				folderCount = 0
			folderCount = folderCount + 1
			if folderCount == 25000|50000|75000|100000|125000|150000|175000|200000:
				current = time.asctime()
				print(dir,"@",folderCount,"@",current)
			if "metadata" not in filename:
				with open(filename, "r") as f:
					filedata = f.read()
					if "<xip:Title>" in filedata:
						dom = ET.parse(filename)
						# construct the namespaces for later on
						root = dom.getroot()
						namespaces = getNamespaces(root)
						try:
							tree = ET.parse(filename)
							root = tree.getroot()
							title = root.find(".//xip:Title", namespaces=namespaces).text
							uuid = root.find(".//xip:Ref", namespaces=namespaces).text
							ws.append([uuid,title])
							processed = processed + 1
						except:
							print("something is wrong with",filename)
wb.save(workbookfilename)
wb.close()
print(processed,"files processed")
print(total,"files reviewed overall")