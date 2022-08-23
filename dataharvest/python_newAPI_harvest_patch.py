import csv
import getpass
import os
import requests
import time

import lxml.etree as ET
from preservation_utilities import preservation_utilities


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
#create a basic timer
timer = time.time() + 600
# create a logger for fails
logger = open("log_potential_fails_patch.txt", "a")
#set base level variables
base_url = 'https://tsl.preservica.com/api/entity/'
#additional information
valuables = input("name or error log file: ")
file = open(valuables, "r", encoding='utf-8')
csvin = csv.reader(file)
for row in csvin:
	try:
		uuidUrl = row[0]
		directory = row[1]
		xip_file = row[2]
		type = row[3]
		newFile = directory + "/" + xip_file
		print(newFile)
		preservation_utilities.dirMaker(newFile)
		response = requests.get(uuidUrl, headers=headers)
		status = response.status_code
		if status == 401:
			print(newFile,"may have failed, logging back in")
			logger.write(newFile + "\n")
			headers = preservation_utilities.login(url, payload)
			response = requests.get(uuidUrl, headers=headers)
			preservation_utilities.filemaker(newFile, response)
		else:
			preservation_utilities.filemaker(newFile, response)
		dom = ET.parse(newFile)
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
		things = root.xpath('.//EntityResponse:Fragment[not((@schema="http://preservica.com/LegacyXIP") or (@schema="http://preservica.com/ExtendedXIP/v6.0"))]', namespaces=namespaces)
		elementCounter = 0
		for thing in things:
			try:
				elementals = thing.text
				elementCounter = elementCounter + 1
				anotherNewFile = newFile[:-4] + "_metadata-" + str(elementCounter) + ".xml"
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
				continue
		if type == "SO":
			childfile = os.path.join(directory, "level", xip_file[:-4] + "_children.xml")
			preservation_utilities.dirMaker(childfile)
			response = requests.get(uuidUrl + "/children?start=0&max=1000", headers=headers)
			status = response.status_code
			if status == 401:
				print(childfile, "may have failed, logging back in")
				logger.write(childfile + "\n")
				headers = preservation_utilities.login(url, payload)
				response = requests.get(uuidUrl + "/children?start=0&max=1000", headers=headers)
				preservation_utilities.filemaker(childfile, response)
			else:
				preservation_utilities.filemaker(childfile, response)
			dom3 = ET.parse(childfile)
			root3 = dom3.getroot()
			things = root3.xpath('.//ChildrenResponse:TotalResults', namespaces=namespaces)
			for thing in things:
				hits = int(thing.text)
				children_start = 1000
				root_child = uuidUrl + "/children?start="
				max_child = "&max=1000"
				if hits > 1000:
					while children_start <= hits:
						childfile = os.path.join(directory, "level", xip_file[:-4] + "_" + str(children_start) + "_children.xml")
						response = requests.get(root_child + str(children_start) + max_child, headers=headers)
						preservation_utilities.filemaker(childfile, response)
						children_start = children_start + 1000
	except:
		print("problem with",row)
	
		#call on timer to see if it is time to log back in
	if timer <= time.time():
		print("time to log back in")
		headers = preservation_utilities.login(url, payload)
		timer = time.time() + 600