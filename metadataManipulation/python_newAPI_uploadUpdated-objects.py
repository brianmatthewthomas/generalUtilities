# to push all files in a directory to preservica as updates.
# each failed attempt will be copied to a directory called errors, which will need to be deleted after second attempt
import lxml.etree as ET
import os, shutil
import requests
import time
import getpass
from preservation_utilities import preservation_utilities

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
seriousFilepath = "/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/newAPI/correcto" #input("XIP files directory without trailing /:")

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
        if filename.startswith("SO_") and filename.endswith(".xml") and "metadata" not in filename and "children" not in filename:
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
                namespaces['EntityResponse'] = namespaces['xmlns']
                namespaces['xip'] = namespaces['xmlns'].replace("EntityAPI", "XIP")
                nameOfSpace = namespaces['xmlns'].split("/")[-1]
                with open(filename, "r") as f:
                    filedata = f.read()
                    xipRef = dom.find('.//xip:Ref', namespaces=namespaces).text
                    title = dom.find('.//xip:Title', namespaces=namespaces).text
                    description = dom.find('.//xip:Description', namespaces=namespaces).text
                    securityTag = dom.find('.//xip:SecurityTag', namespaces=namespaces).text
                    parent = dom.find('.//xip:Parent', namespaces=namespaces).text
                    filedata = f'<xip:StructuralObject xmlns:xip="{namespaces["xip"]}"><xip:Ref>{xipRef}</xip:Ref>' \
                                f'<xip:Title>{title}</xip:Title><xip:Description>{description}</xip:Description>' \
                                f'<xip:SecurityTag>{securityTag}</xip:SecurityTag><xip:Parent>{parent}</xip:Parent>' \
                                f'</xip:StructuralObject>'
                    print(filedata)
                    with open(f"{math}errors/tempfile.txt", "w") as f:
                        f.write(filedata)
                    f.close()
            except:
                sys.exit()
                '''
                response = requests.put(entityURL, headers=headers, data=filedata.encode('utf-8'))
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
        if timer <= time.time():
            print("time to log back in")
            headers = preservation_utilities.login(url, payload)
            timer = time.time() + 600'''
print("potential errors:", failure)
print("success count:", count)
log.close()