import sys, os, json, requests
import datetime
import time
import getpass
import lxml.etree as ET


def login(url, payload):
    auth = requests.post(url, data=payload).json()
    sessionToken = auth["token"]
    headers = {'Preservica-Access-Token': sessionToken}
    headers['Content-Type'] = 'application/xml'
    headers['Accept-Charset'] = 'UTF-8'
    return headers


def legacyXIP(dom, headers, namespaces):
    temp2 = dom.find('.//EntityResponse:Fragment[@schema="http://preservica.com/LegacyXIP"]',
                     namespaces=namespaces).text
    response = requests.get(temp2, headers=headers)
    status = response.status_code
    if status == 401:
        print("get for", filename, " legacyXIP metadata may have failed, retrying")
        logger.write(filename + "login error" + "\n")
        login(url, payload)
        headers = login(url, payload)
        response = requests.get(temp2, headers=headers)
        with open(tempfile2, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()
    if status == 502:
        print("get for", filename, " legacyXIP metadata may have failed, retrying")
        logger.write(filename + "login error" + "\n")
        login(url, payload)
        headers = login(url, payload)
        response = requests.get(temp2, headers=headers)
        with open(tempfile2, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()
    else:
        with open(tempfile2, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()
    dom2 = ET.parse(tempfile2)
    dateOfCreation = dom2.find(".//LegacyXIP:LastModifiedDate", namespaces=namespaces).text
    return dateOfCreation


def txCTS(dom, headers, namespaces):
    temp2 = dom.find('.//EntityResponse:Fragment[@schema="https://texas.gov/"]', namespaces=namespaces).text
    response = requests.get(temp2, headers=headers)
    status = response.status_code
    if status == 401:
        print(status, "get for", filename, " txCTS metadata may have failed, retrying")
        logger.write(filename + "login error" + "\n")
        login(url, payload)
        headers = login(url, payload)
        response = requests.get(temp2, headers=headers)
        with open(tempfile2, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()
    if status == 502:
        print(status, "get for", filename, " txCTS metadata may have failed, retrying")
        logger.write(filename + "login error" + "\n")
        login(url, payload)
        headers = login(url, payload)
        response = requests.get(temp2, headers=headers)
        with open(tempfile2, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()
    else:
        with open(tempfile2, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()
    dom2 = ET.parse(tempfile2)
    try:
        dateOfCreation = dom2.find(".//txCTS:date.correspondenceEntered[1]", namespaces=namespaces).text
    except:
        dateOfCreation = "None"
    if dateOfCreation == "None" or dateOfCreation == None:
        try:
            tempting = dom2.find(".//txCTS:imagePath[1]", namespaces=namespaces).text
            tempting = tempting[-13:]
            dateOfCreation = tempting[:4] + "-" + tempting[5:7] + "-" + tempting[-3:-1]
        except:
            dateOfCreation = "None"
    return dateOfCreation


def mail(dom, headers, namespaces):
    temp2 = dom.find('.//EntityResponse:Fragment[@schema="http://www.tessella.com/mailbox/v1"]',
                     namespaces=namespaces).text
    response = requests.get(temp2, headers=headers)
    status = response.status_code
    if status == 401:
        print(status, "get for", filename, " email metadata may have failed, retrying")
        logger.write(filename + "login error" + "\n")
        login(url, payload)
        headers = login(url, payload)
        response = requests.get(temp2, headers=headers)
        with open(tempfile2, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()
    if status == 502:
        print(status, "get for", filename, " email metadata may have failed, retrying")
        logger.write(filename + "login error" + "\n")
        login(url, payload)
        headers = login(url, payload)
        response = requests.get(temp2, headers=headers)
        with open(tempfile2, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()
    else:
        with open(tempfile2, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()
    dom2 = ET.parse(tempfile2)
    try:
        dateOfCreation = dom2.find(".//email:date", namespaces=namespaces).text
    except:
        dateOfCreation = "None"
    return dateOfCreation


def mail2(tempfile2, headers, namespaces):
    dom2 = ET.parse(tempfile2)
    try:
        dateOfCreation = dom2.find(".//email:appointmentStartTime", namespaces=namespaces).text
        note = "Date of creation based upon date of appointment start date."
    except:
        dateOfCreation = "None"
    return dateOfCreation


def getDcterms(dom, headers, namespaces):
    temp1 = dom.find('.//EntityResponse:Fragment[@schema="http://dublincore.org/documents/dcmi-terms/"]',
                     namespaces=namespaces).text
    response = requests.get(temp1, headers=headers)
    status = response.status_code
    if status == 401:
        print(status, "get for", filename, "dcterms metadata may have failed, retrying")
        logger.write(filename + "login error" + "\n")
        login(url, payload)
        headers = login(url, payload)
        response = requests.get(temp1, headers=headers)
        with open(tempfile1, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()
    if status == 502:
        print(status, "get for", filename, "dcterms metadata may have failed, retrying")
        logger.write(filename + "login error" + "\n")
        login(url, payload)
        headers = login(url, payload)
        response = requests.get(temp1, headers=headers)
        with open(tempfile1, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()
    else:
        with open(tempfile1, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()


if __name__ == '__main__':
    url = "https://tsl.preservica.com/api/accesstoken/login"
    u = input("Enter your username: ")
    p = getpass.getpass("Enter password: ")
    t = input("Enter your tenancy name: ")
    payload = {'username': u, 'password': p, 'tenant': t}
    print("Logging in...")
    headers = login(url, payload)
    print(headers)

namespaces = {'xip': 'http://preservica.com/XIP/v6.3',
              'EntityResponse': 'http://preservica.com/EntityAPI/v6.3',
              'ChildrenResponse': 'http://preservica.com/EntityAPI/v6.3',
              'MetadataResponse': 'http://preservica.com/EntityAPI/v6.3',
              'dcterms': 'http://dublincore.org/documents/dcmi-terms',
              'email': 'http://www.tessella.com/mailbox/v1',
              'LegacyXIP': 'http://preservica.com/LegacyXIP',
              'txCTS': 'https://texas.gov/',
              'tslac': 'https://www.tsl.texas.gov/'
              }
# create a basic timer for logging back in rather than waiting for a time-out
timer = time.time() + 600
# create initial date of creation and general notes just in case the first file doesn't have any metadata to work with
dateOfCreation = ""
note = ""
# helper files
tempfile1 = "tempfile1.xml"
tempfile2 = "tempfile2.xml"
# open the tempfile2 to make sure it exists in case the first file is a dud
tatoo = open(tempfile2, "w")
tatoo.close()
# create spreadsheet to list out what needs to be reharvested after this is all done
# the local variables for this process
print("Designed to pick up a harvest where it left off. Change helper.txt to where it failed and continue")
realfilepath = input("Directory to crawl: ")
logger = open(realfilepath + "/log_dateLooper.txt", "a")
tracker = 0
# create binary switch for if an update should be applied
NA = 0
dir = ""
# start crawl
helpme = "helper.txt"
status = input("new or resume date addition? Enter 'new' or 'resume': ")
while status != 'new' and status != 'resume':
    status = input("new or resume date addition? Enter 'new' or 'resume': ")
if status == 'new':
    helper = open(helpme, "a")
    # create list of files to work with
    for dirpath, dirnames, filenames in os.walk(realfilepath):
        for filename in filenames:
            if filename.startswith(("IO_")) and filename.endswith((".xml")):
                if "children" not in filename:
                    if "metadata" not in filename:
                        filename = os.path.join(dirpath, filename)
                        helper.write(filename + "\n")
    helper.close()
with open(helpme, "r") as db:
    for line in db:
        filename = line[:-1]
        dom = ET.parse(filename)
        root = dom.getroot()
        list = []
        elements = root.xpath(".//EntityResponse:Fragment", namespaces=namespaces)
        for element in elements:
            type = element.get('schema')
            list.append(type)
        if "http://dublincore.org/documents/dcmi-terms/" not in list:
            print(filename, "is missing dcterms, run metadata adder and then rerun this script")
            sys.exit()
        getDcterms(dom, headers, namespaces)
        response = ""
        if "http://www.tessella.com/mailbox/v1" in list:
            dateOfCreation = mail(dom, headers, namespaces)
            note = "Date of creation based upon date message/appointment was received"
            if dateOfCreation == "None":
                dateOfCreation = mail2(tempfile2, headers, namespaces)
                note = "Date of creation based upon date of appointment start date."
                if dateOfCreation == "None":
                    if "http://preservica.com/LegacyXIP" in list:
                        dateOfCreation = legacyXIP(dom, headers, namespaces)
                        note = "Date of creation information extrapolated from date the file was last modified, which may not perfectly correspond to the exact date file was created."
                    else:
                        NA = 1
            response = ""
        elif "https://texas.gov/" in list:
            dateOfCreation = txCTS(dom, headers, namespaces)
            note = "Date of creation based upon date correspondence received by the Governor's Office, as documented in the Correspondence Tracking System database. Governor's Office data entry errors may  exist."
            if dateOfCreation == "None":
                if "http://preservica.com/LegacyXIP" in list:
                    dateOfCreation = legacyXIP(dom, headers, namespaces)
                    note = "Date of creation information extrapolated from date the file was last modified, which may not perfectly correspond to the exact date file was created."
                else:
                    NA = 1
            response = ""
        elif "http://preservica.com/LegacyXIP" not in list:
            print(filename, "has nothing actionable")
            logger.write(filename + "has no actionable info, date added may be wrong")
            with open(tempfile2, "w") as fd:
                fd.write("nothing goes here")
            fd.close()
            # set switch to skip posting non-existent data
            NA = 1
        else:
            dateOfCreation = legacyXIP(dom, headers, namespaces)
            note = "Date of creation information extrapolated from date the file was last modified, which may not perfectly correspond to the exact date file was created."
            response = ""
        # remove superfluous data from temp dcterms file
        # if switch says dcterms was applicable
        if NA == 0:
            with open(tempfile1, "r") as f:
                filedata = f.read()
                if "date.created>" in filedata:
                    print("date of creation already assigned for", filename)
                    filedata = ""
                # check if date.created already exists and exit if sort
                else:
                    try:
                        dom = ET.parse(tempfile1)
                        entityURL = dom.find(".//MetadataResponse:Self", namespaces=namespaces).text
                        xipRef = dom.find(".//xip:Ref", namespaces=namespaces).text
                        xipEntity = dom.find(".//xip:Entity", namespaces=namespaces).text
                        filedata = filedata.replace(
                            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><MetadataResponse xmlns="http://preservica.com/EntityAPI/v6.3" xmlns:xip="http://preservica.com/XIP/v6.3"><xip:MetadataContainer schemaUri="http://dublincore.org/documents/dcmi-terms/"><xip:Ref>' + xipRef + '</xip:Ref><xip:Entity>' + xipEntity + '</xip:Entity><xip:Content>',
                            '')
                        filedata = filedata.replace(
                            '</xip:Content></xip:MetadataContainer><AdditionalInformation><Self>' + entityURL + '</Self></AdditionalInformation></MetadataResponse>',
                            '')
                        # fix a weird behavior that converts a utf8 character to windows single quote character during an earlier part of the loop
                        filedata = filedata.replace("’", "'")
                        filedata = filedata.replace("‘", "'")
                        dateOfCreation = str(dateOfCreation)
                        dateOfCreation = dateOfCreation[:10]
                        try:
                            tester = int(dateOfCreation[:4])
                        except:
                            print("date format for", filename, "is wrong, check into that")
                            logger.write(filename + " has bad date information, check manually" + "\n")
                        # insert text based on whether prefix was included in the metadata
                        if "</dcterms:identifier.bibliographicCitation>" in filedata:
                            filedata = filedata.replace("</dcterms:identifier.bibliographicCitation>",
                                                        "</dcterms:identifier.bibliographicCitation><dcterms:date.created>" + dateOfCreation + "</dcterms:date.created><tslac:note>" + note + "</tslac:note>")
                        elif "</identifier.bibliographicCitation>" in filedata:
                            filedata = filedata.replace("</identifier.bibliographicCitation>",
                                                        "</identifier.bibliographicCitation><date.created>" + dateOfCreation + "</date.created><tslac:note>" + note + "</tslac:note>")
                        if ' xmlns:tslac="https://www.tsl.texas.gov/"' not in filedata:
                            filedata = filedata.replace('xmlns:dcterms',
                                                        'xmlns:tslac="https://www.tsl.texas.gov/" xmlns:dcterms')
                        if 'xmlns="http://www.tessella.com/XIP/v4"' in filedata:
                            filedata = filedata.replace('xmlns="http://www.tessella.com/XIP/v4"',
                                                        'xmlns="http://dublincore.org/documents/dcmi-terms/"')
                        # re-save file with changes
                        with open(tempfile1, "w") as f:
                            f.write(filedata)
                            f.close()
                        response = requests.put(entityURL, headers=headers, data=filedata)
                        status = response.status_code
                        current = time.asctime()
                        if status == 400:
                            status = str(status)
                            logger.write(filename + ' may have failed, check Preservica' + "\n")
                            print(filename, "may have failed, logging back in")
                            login(url, payload)
                            headers = login(url, payload)
                            response = requests.put(entityURL, headers=headers, data=filedata)
                        if status == 401:
                            status = str(status)
                            logger.write(filename + ' may have failed, check Preservica' + "\n")
                            print(filename, "may have failed, logging back in")
                            login(url, payload)
                            headers = login(url, payload)
                            response = requests.put(entityURL, headers=headers, data=filedata)
                        if status == 404:
                            status = str(status)
                            logger.write(filename + ' may have failed, check Preservica' + "\n")
                            print(filename, "may have failed, logging back in")
                            login(url, payload)
                            header = login(url, payload)
                            response = requests.put(entityURL, headers=headers, data=filedata)
                        if status == 422:
                            status = str(status)
                            logger.write(filename + ' may have failed, check Preservica' + "\n")
                            print(filename, "may have failed, logging back in")
                            login(url, payload)
                            headers = login(url, payload)
                            response = requests.put(entityURL, headers=headers, data=filedata)
                        if status == 500:
                            status = str(status)
                            logger.write(filename + ' may have failed, check Preservica' + "\n")
                            print(filename, "may have failed, logging back in")
                            login(url, payload)
                            headers = login(url, payload)
                            response = requests.put(entityURL, headers=headers, data=filedata)
                        if status == 502:
                            status = str(status)
                            logger.write(filename + ' may have failed, check Preservica' + "\n")
                            print(filename, "may have failed, logging back in")
                            login(url, payload)
                            headers = login(url, payload)
                            response = requests.put(entityURL, headers=headers, data=filedata)
                        if status == 504:
                            status = str(status)
                            logger.write(filename + ' may have failed, check Preservica' + "\n")
                            print(filename, "may have failed, logging back in")
                            login(url, payload)
                            headers = login(url, payload)
                            response = requests.put(entityURL, headers=headers, data=filedata)
                        print('status: ', str(status), "at", current, "for", filename)
                        logger.write('status: ' + str(status) + ' at ' + current + ' for ' + filename + "\n")
                        patchlog = open(realfilepath + "/patchlog.csv", "a")
                        tracker = tracker + 1
                        uuid = filename[-40:-4]
                        patchlog.write(
                            "https://tsl.preservica.com/api/entity/information-objects/" + uuid + "," + filename + "\n")
                        patchlog.close()
                    except AttributeError:
                        print("something wrong with", filename, "metadata")
                        logger.write("status: 000 " + filename + "may be malformed xml, check file" + "\n")
                        continue
                    except requests.exceptions.RequestException:
                        print(filename, "may have failed, check preservica")
                        logger.write(filename + ' may have failed, check Preservica' + "\n")
                        headers = login(url, payload)
                        continue
        # clear all existing variables so they don't accidentally get recycled and delete-ish temp files
        tempSwitch = 0
        while tempSwitch == 0:
            try:
                os.rename(tempfile2, "junk.xml")
                tempSwitch = 1
            except:
                print("trouble with temp file, retrying")
        filedata = ""
        NA = 0
        note = ""
        dateOfCreation = ""
        temp1 = ""
        temp2 = ""
        root = ""
        root2 = ""
        dom = ""
        dom2 = ""
        entityURL = ""
        xipRef = ""
        xipEntity = ""
        list = ""
        tempSwitch = 0
        while tempSwitch == 0:
            try:
                os.rename(tempfile1, "junk1.xml")
                tempSwitch = 1
            except:
                print("trouble with temp file, retrying")
        # call on timer to see if it is time to log back in
        if timer <= time.time():
            print("time to log back in")
            headers = login(url, payload)
            timer = time.time() + 600
logger.close()
os.remove(helpme)
os.remove("junk.xml")
os.remove("junk1.xml")
print(tracker, "files updated, list of files removed")