# to push all files in a directory to preservica as updates.
# each failed attempt will be copied to a directory called errors, which will need to be deleted after second attempt
import lxml.etree as ET
import os, shutil
import requests
import time
import getpass
from preservation_utilities import preservation_utilities

namespace_1 = {'xmlns': "http://dublincore.org/documents/dcmi-terms/",
               'tslac': "https://www.tsl.texas.gov/",
               'dcterms': "http://dublincore.org/documents/dcmi-terms/"}
metadata_files = '/media/sf_Z_DRIVE/Working/OAG/working/presentation6/2007' #input("directory with correct metadata file: ")
tag = 'dcterms:title' #input("tag content to pair on, including prefix: ")
metadata_dict = {}
for dirpath, dirnames, filenames in os.walk(metadata_files):
    for filename in filenames:
        if filename.endswith(".metadata"):
            filename = os.path.join(dirpath, filename)
            dom = ET.parse(filename)
            my_key = dom.find(tag, namespaces=namespace_1).text
            metadata_dict[my_key] = filename
            print(filename)
print(metadata_dict)

tag = 'dcterms:title'
print("For each code that is no 200 the file will be copied to an errors directory")
print("once uploads are complete, reattempt any files in ./errors and if all ok delete ./errors")

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
# user-defined parameters
seriousFilepath = '/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/newAPI/correcto_2007' #input("XIP files directory without trailing /:")

# constants
base_url = f'https://{prefix}.preservica.com/api/entity/'
failure = 0
success = 0
count = 0
log = open("log_uploadUpdates.txt", "a")
# lets make a directory to copy failed files to for retries
math = seriousFilepath.split("/")[-1]
math2 = len(math)
math = seriousFilepath[:-math2]
directory = math + "errors/placeholder.txt"
preservation_utilities.dirMaker(directory)
placeholder = open(directory, "a")
placeholder.write('this file exists only to make sure errors directory creation worked')
placeholder.close()
directory = directory[:-16]
for dirpath, dirnames, filenames in os.walk(seriousFilepath):
    # load directory to crawl
    for filename in filenames:
        # crawl the directory for files starting with the appropriate convention
        # use convention to dictate how to extract uuid
        # post file based on convention and extracted uuid
        filename2 = os.path.join(directory, filename)
        if "metadata" in filename and filename.endswith(".xml"):
            try:
                filename = os.path.join(dirpath, filename)
                print(filename)
                log.write(filename + "\n")
                dom = ET.parse(filename)
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
                nameOfSpace = namespaces['xmlns'].split("/")[-1]
                with open(filename, "r") as f:
                    filedata = f.read()
                    entityURL = dom.find('.//MetadataResponse:Self', namespaces=namespaces).text
                    xipRef = dom.find('.//xip:Ref', namespaces=namespaces).text
                    xipEntity = dom.find('.//xip:Entity', namespaces=namespaces).text
                    # remove head and tail information since that isn't permitted
                    filedata = filedata.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
                    filedata = filedata.replace("<?xml version='1.0' encoding='utf-8'?>", "")
                    top = f'<MetadataResponse xmlns="http://preservica.com/EntityAPI/{nameOfSpace}"' \
                          f' xmlns:xip="http://preservica.com/XIP/{nameOfSpace}"><xip:MetadataContainer' \
                          f' schemaUri="http://dublincore.org/documents/dcmi-terms/"><xip:Ref>' + xipRef +\
                          '</xip:Ref><xip:Entity>' + xipEntity + '</xip:Entity><xip:Content>'
                    bottom = '</xip:Content></xip:MetadataContainer><AdditionalInformation><Self>' + entityURL + \
                             '</Self></AdditionalInformation></MetadataResponse>'
                    filedata = filedata.replace(
                        f'<MetadataResponse xmlns="http://preservica.com/EntityAPI/{nameOfSpace}"'
                        f' xmlns:xip="http://preservica.com/XIP/{nameOfSpace}"><xip:MetadataContainer'
                        f' schemaUri="http://dublincore.org/documents/dcmi-terms/"><xip:Ref>' + xipRef +
                        '</xip:Ref><xip:Entity>' + xipEntity + '</xip:Entity><xip:Content>','')
                    filedata = filedata.replace(
                        '</xip:Content></xip:MetadataContainer><AdditionalInformation><Self>' + entityURL +
                        '</Self></AdditionalInformation></MetadataResponse>','')
                    filedata = filedata.replace("–", "-")
                    filedata = filedata.replace("’", "'")
                    filedata = filedata.replace('“', '"')
                    filedata = filedata.replace('”', '"')
                    with open("../tempfile.txt", "w") as f:
                        f.write(filedata)
                        f.close()
                    my_key = dom.find(f'.//{tag}', namespaces=namespaces).text
                    if my_key in metadata_dict:
                        with open(metadata_dict[my_key], "r") as f:
                            print(my_key,'found')
                            filedata = f.read()
                            filedata = filedata.replace('<?xml version="1.0" ?>','').replace("\n<dcterms:dcterms","<dcterms:dcterms")
                            filedata = top + filedata + bottom
                            with open(filename, "w") as w:
                                w.write(filedata)
                            w.close()
            except AttributeError:
                print("something wrong with", filename)
                log.write("status: 000" + filename + " may be malformed xml, check file" + "\n")
                failure = failure + 1
                shutil.copyfile(filename, filename2)
                continue
            except requests.exceptions.RequestException:
                failure = failure + 1
                print(filename, "may have failed, check Preservica")
                log.write(filename + ' may have failed, check Preservica' + "\n")
                headers = preservation_utilities.login(url, payload)
                shutil.copyfile(filename, filename2)
                continue
'''
                response = requests.put(entityURL, headers=headers, data=filedata)
                status = response.status_code
                current = time.asctime()
                # handle specific http error codes
                if status == 400:
                    failure = failure + 1
                    status = str(status)
                    log.write(filename + ' may have failed, check Preservica ' + "\n")
                    response = requests.put(entityURL, headers=headers, data=filedata)
                    shutil.copyfile(filename, filename2)
                if status == 401:
                    failure = failure + 1
                    print(filename, "may have failed, logging back in")
                    status = str(status)
                    log.write(filename + ' may have failed, check Preservica ' + "\n")
                    headers = preservation_utilities.login(url, payload)
                    response = requests.put(entityURL, headers=headers, data=filedata)
                    shutil.copyfile(filename, filename2)
                if status == 404:
                    failure = failure + 1
                    status = str(status)
                    print(filename, "may have failed")
                    shutil.copyfile(filename, filename2)
                if status == 422:
                    failure = failure + 1
                    status = str(status)
                    log.write(filename + ' may have failed, check Preservica ' + "\n")
                    response = requests.put(entityURL, headers=headers, data=filedata)
                    shutil.copyfile(filename, filename2)
                if status == 500:
                    failure = failure + 1
                    status = str(status)
                    print(filename, "may have failed")
                    shutil.copyfile(filename, filename2)
                if status == 502:
                    failure = failure + 1
                    status = str(status)
                    log.write(filename + ' may have failed, check Preservica ' + "\n")
                    shutil.copyfile(filename, filename2)
                if status == 504:
                    failure = failure + 1
                    status = str(status)
                    print(filename, "may have failed")
                    shutil.copyfile(filename, filename2)
                status = str(status)
                print("status:", status, "at", current, "for", filename)
                log.write('status: ' + status + ' at ' + current + ' for ' + filename + "\n")
                count = count + 1
        if timer <= time.time():
            print("time to log back in")
            headers = preservation_utilities.login(url, payload)
            timer = time.time() + 600
print("potential errors:", failure)
print("success count:", count)
log.close()'''