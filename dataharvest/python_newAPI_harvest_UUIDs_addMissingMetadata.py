import getpass
import os
import requests
import sys
import time

import lxml.etree as ET

from preservation_utilities import preservation_utilities


def newDirpath (dirpath):
	str(dirpath)
	if dirpath.endswith("/"):
		dirpath = dirpath[:-1]
	try:
		dirlevel2 = int(dirpath[-2:])
		dirlevel2 += 1
		return dirlevel2
	except:
		dirlevel2 = int(dirpath[-1:])
		dirlevel2 += 1
		return dirlevel2

username = input("Enter your username: ")
password = getpass.getpass("Enter password: ")
#	p = input("Enter your password: ")
prefix = input("Enter your prefix name: ")
tenancy = input("Enter tenancy: ")
url = f"https://{prefix}.preservica.com/api/accesstoken/login"
payload = {'username': username, 'password': password, 'tenant': tenancy}
print("Logging in...")
headers = preservation_utilities.login(url, payload)
print(headers)
version = input("preservica platform number: ")
#create a basic timer
timer = time.time() + 600
# create a logger for fails
logger = open("log_UUIDv4-potential_fails.txt", "a")
logger2 = open("log_UUIDv4-MD-addedTo.txt", "a")
# create the folder level counter
level = 1
addCounter = 0
counter = 0
#set base level variables
base_url = f'https://{prefix}.preservica.com/api/entity/'
so = "structural-objects/"
io = "information-objects/"
dublinCore = "http://dublincore.org/documents/dcmi-terms/"
namespaces = {'xip': f'http://preservica.com/XIP/{version}',
'EntityResponse': f'http://preservica.com/EntityAPI/{version}',
'ChildrenResponse': f'http://preservica.com/EntityAPI/{version}'}
realfilepath = input("absolute or relative filepath to put the harvested files: ")
metadata = input("Name of metadata file to insert if none exists: ")
#start with the root structural object
homefries = input("UUID for the collection to harvest: ")
jumpPoint = base_url + so + homefries
#target = input("target directory to save crawl to: ")
response = requests.get(jumpPoint, headers=headers)
status = response.status_code
dirlevel = realfilepath + "level" + str(level) + "/"
filename = dirlevel + "SO_" + homefries + ".xml"
level += 1
dirlevel = dirlevel + "level" + str(level) + "/"
childrenOfTheObject = dirlevel + "SO_" + homefries + "_children.xml"
preservation_utilities.dirMaker(filename)
preservation_utilities.dirMaker(childrenOfTheObject)
preservation_utilities.filemaker(filename, response)
response = requests.get(jumpPoint + "/children?start=0&max=1000", headers=headers)
status = response.status_code
if status == 401:
	print(childrenOfTheObject,"may have failed, logging back in")
	logger.write(childrenOfTheObject + "\n")
	preservation_utilities.login(url, payload)
	headers = preservation_utilities.login(url, payload)
	response = requests.get(jumpPoint + "/children?start=0&max=1000", headers=headers)
	preservation_utilities.filemaker(childrenOfTheObject, response)
else:
	preservation_utilities.filemaker(childrenOfTheObject, response)
dom3 = ET.parse(childrenOfTheObject)
root3 = dom3.getroot()
things = root3.xpath('.//ChildrenResponse:TotalResults', namespaces=namespaces)
for thing in things:
	hits = int(thing.text)
	children_start = 1000
	root_child = jumpPoint + "/children?start="
	max_child = "&max=1000"
	if hits > 1000:
		while children_start <= hits:
			childfile = os.path.join(dirlevel, "SO_" + homefries + "_" + str(children_start) + "_children.xml")
			response = requests.get(root_child + str(children_start) + max_child, headers=headers)
			preservation_utilities.filemaker(childfile, response)
			children_start = children_start + 1000
dirlevel2 = dirlevel
#make the dummy directory structure
while level != 21:
	level += 1
	dirlevel2 = dirlevel2 + "level" + str(level) + "/"
	dummy = os.path.join(dirlevel2,"filename.txt")
	preservation_utilities.dirMaker(dummy)
# continue with processing
dom = ET.parse(filename)
root = dom.getroot()
elements = root.xpath(f'.//EntityResponse:Fragment[not((@schema="http://preservica.com/LegacyXIP") or (@schema="http://preservica.com/ExtendedXIP/{version}"))]',namespaces=namespaces)
elementCounter = 0
list = []
for element in elements:
	type = element.get('schema')
	list.append(type)
if dublinCore not in list:
	purl2 = jumpPoint + "/metadata"
	responsible = requests.post(purl2, headers=headers, data = open(metadata, 'rb'))
	response = requests.get(jumpPoint, headers=headers)
	addCounter += 1
	preservation_utilities.filemaker(filename, response)
	dom = ET.parse(filename)
	root = dom.getroot()
	elements = root.xpath(f'.//EntityResponse:Fragment[not((@schema="http://preservica.com/LegacyXIP") or (@schema="http://preservica.com/ExtendedXIP/{version}"))]',namespaces=namespaces)
for element in elements:
	try:
		elemental = element.text
		elementCounter = elementCounter + 1
		response = requests.get(elemental, headers=headers)
		preservation_utilities.filemaker(filename[:-4] + "_metadata-" + str(elementCounter) + ".xml", response)
	except:
		continue
# create a file list to qa when done harvesting
list_of_files = []
list_of_existing_files = []
print("getting list of existing files")
for dirpath, dirnames, filenames in os.walk(dirlevel):
	for filename in filenames:
		filename = os.path.join(dirpath, filename)
		list_of_existing_files.append(filename)
print("list generation complete")
for dirpath, dirnames, filenames in os.walk(dirlevel):
	for filename in filenames:
		filename = os.path.join(dirpath, filename)
		if "_children" in filename:
			try:
				dom = ET.parse(filename)
			except OSError:
				print("trouble reading",filename,",",addCounter,"files had dcterms added to them")
				sys.exit()
			root = dom.getroot()
			elements = root.xpath(".//ChildrenResponse:Child[@type='SO']",namespaces=namespaces)
			for element in elements:
				try:
					elemental = element.text
					type = element.get('type')
					uuid = element.get('ref')
					newFile = os.path.join(dirpath, type + "_" + uuid + ".xml")
					list_of_files.append(newFile)
					if newFile not in list_of_existing_files:
						response = requests.get(elemental, headers=headers)
						status = response.status_code
						#harvest error handling
						if status == 401:
							print(newFile,"may have failed, logging back in")
							logger.write(newFile + "\n")
							headers = preservation_utilities.login(url, payload)
							response = requests.get(elemental, headers=headers)
							preservation_utilities.filemaker(newFile, response)
						else:
							preservation_utilities.filemaker(newFile, response)
					dom2 = ET.parse(newFile)
					root2 = dom2.getroot()
					things = root2.xpath('.//EntityResponse:Fragment', namespaces=namespaces)
					list = []
					for thing in things:
						dcType = thing.get('schema')
						list.append(dcType)
					print(list)					
					if dublinCore not in list:
						print(uuid,"missing dcterms, adding them")
						purl2 = elemental + "/metadata"
						responsible = requests.post(purl2, headers=headers, data = open(metadata, 'rb'))
						response = requests.get(elemental, headers=headers)
						addCounter += 1
						preservation_utilities.filemaker(newFile, response)
						logger2.write(elemental + "\n")
					dom2 = ET.parse(newFile)
					root2 = dom2.getroot()
					things = root2.xpath(f'.//EntityResponse:Fragment[not((@schema="http://preservica.com/LegacyXIP") or (@schema="http://preservica.com/ExtendedXIP/{version}"))]',namespaces=namespaces)
					elementCounter2 = 0
					for thing in things:
						elementCounter2 = elementCounter2 + 1
						anotherNewFile = newFile[:-4] + "_metadata-" + str(elementCounter2) + ".xml"
						try:
							elementals = thing.text
							list_of_files.append(anotherNewFile)
							if anotherNewFile not in list_of_existing_files:
								response = requests.get(elementals, headers=headers)
								status = response.status_code
								if status == 401:
									print(anotherNewFile,"may have failed, logging back in")
									logger.write(anotherNewFile + "\n")
									headers = preservation_utilities.login(url, payload)
									response = requests.get(elementals, headers=headers)
									preservation_utilities.filemaker(anotherNewFile, response)
								else:
									preservation_utilities.filemaker(anotherNewFile, response)
						except:
							print("exception happened around",newFile,"or",anotherNewFile)
					#nest that structure properly
					dirlevel2 = newDirpath(dirpath)					
					childfile = os.path.join(dirpath, "level" + str(dirlevel2), type + "_" + uuid + "_children.xml")
					list_of_files.append(childfile)
					if childfile not in list_of_existing_files:
						preservation_utilities.dirMaker(childfile)
						response = requests.get(elemental + "/children?start=0&max=1000", headers=headers)
						status = response.status_code
						if status == 401:
							print(childfile,"may have failed, logging back in")
							logger.write(childfile + "\n")
							headers = preservation_utilities.login(url, payload)
							response = requests.get(elemental + "/children?start=0&max=1000", headers=headers)
							preservation_utilities.filemaker(childfile, response)
						else:
							preservation_utilities.filemaker(childfile, response)
					dom3 = ET.parse(childfile)
					root3 = dom3.getroot()
					things = root3.xpath('.//ChildrenResponse:TotalResults', namespaces=namespaces)
					for thing in things:
						hits = int(thing.text)
						children_start = 1000
						root_child = elemental + "/children?start="
						max_child = "&max=1000"
						if hits > 1000:
							while children_start <= hits:
								childfile = os.path.join(dirpath, "level" + str(dirlevel2), type + "_" + uuid + "_" + str(children_start) + "_children.xml")
								response = requests.get(root_child + str(children_start) + max_child, headers=headers)
								status = response.status_code
								if status == 401:
									print(childfile,"may have failed, logging back in")
									logger.write(childfile + "\n")
									headers = preservation_utilities.login(url, payload)
									response = requests.get(root_child + str(children_start) + max_child, headers=headers)
									preservation_utilities.filemaker(childfile, response)
								else:
									preservation_utilities.filemaker(childfile, response)
									children_start += 1000
				except:
					print("exception happened near",filename,"or",newFile,"or",anotherNewFile)
			elements = root.xpath(".//ChildrenResponse:Child[@type='IO']",namespaces=namespaces)
			for element in elements:
				try:
					elemental = element.text
					type = element.get('type')
					uuid = element.get('ref')
					titleist = element.get('title')
					titleist = titleist.replace(" ","_")
					titleist = titleist.replace("&","and")
					titleist = titleist.replace(":","_")
					titleist = titleist.replace("/","_")
					titleist = titleist.replace('"','_')
					titleist = titleist.replace('?','_')
					titleist = titleist.replace('*','_')
					titleist = titleist[:10]
					newFile = os.path.join(dirpath, type + "_" + titleist + "_" + uuid + ".xml")
					list_of_files.append(newFile)
					if newFile not in list_of_existing_files:
						response = requests.get(elemental, headers=headers)
						status = response.status_code
						if status == 401:
							print(newFile,"may have failed, logging back in")
							logger.write(newFile + "\n")
							headers = preservation_utilities.login(url, payload)
							response = requests.get(elemental, headers=headers)
							preservation_utilities.filemaker(newFile, response)
						else:
							preservation_utilities.filemaker(newFile, response)
					dom2 = ET.parse(newFile)
					root2 = dom2.getroot()
					things = root2.xpath('.//EntityResponse:Fragment', namespaces=namespaces)
					list = []
					for thing in things:
						dcType = thing.get('schema')
						list.append(dcType)
					print(list)
					if dublinCore not in list:
						print(uuid,"missing dcterms, adding them")
						purl2 = elemental + "/metadata"
						responsible = requests.post(purl2, headers=headers, data = open(metadata, 'rb'))
						response = requests.get(elemental, headers=headers)
						addCounter += 1
						preservation_utilities.filemaker(newFile, response)
						logger2.write(elemental + "\n")
					dom2 = ET.parse(newFile)
					root2 = dom2.getroot()
					things = root2.xpath(f'.//EntityResponse:Fragment[not((@schema="http://preservica.com/LegacyXIP") or (@schema="http://preservica.com/ExtendedXIP/{version}"))]',namespaces=namespaces)
					elementCounter2 = 0
					for thing in things:
						try:
							elementals = thing.text
							elementCounter2 = elementCounter2 + 1
							anotherNewFile = newFile[:-4] + "_metadata-" + str(elementCounter2) + ".xml"
							list_of_files.append(anotherNewFile)
							if anotherNewFile not in list_of_existing_files:
								response = requests.get(elementals, headers=headers)
								status = response.status_code
								if status == 401:
									print(anotherNewFile,"may have failed, logging back in")
									logger.write(anotherNewFile + "\n")
									headers = preservation_utilities.login(url, payload)
									response = requests.get(elementals, headers=headers)
									preservation_utilities.filemaker(anotherNewFile, response)
								else:
									preservation_utilities.filemaker(anotherNewFile, response)
						except:
							print("exception happened for some weird reason around",newFile,"or",anotherNewFile)
					if timer <= time.time():
						print("time to log back in")
						headers = preservation_utilities.login(url, payload)
						timer = time.time() + 600
				except:
					print("exception happened for some weird reason around",newFile,"or",anotherNewFile)
logger.close()
logger2.close()
# now check that all of the files are actually there
print("QAing harvest")
#generate a list of actual files that exist
list_of_actual_files = []
for dirpath, dirnames, filenames in os.walk(dirlevel):
	for filename in filenames:
		filename = os.path.join(dirpath, filename)
		list_of_actual_files.append(filename)
# error counter
error_counter = 0
# cross check list of actual files with files that should be there
# there will be more files in existence than those on the list
for item in list_of_files:
	if item not in list_of_actual_files:
		print(item,"not in harvest")
		error_counter += 1
print("all done")
if error_counter == 0:
	print("nothing missing")
else:
	print(str(error_counter), "errors")
print(addCounter,"files had dcterms added to them")