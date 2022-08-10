import sys, os
import pandas as PD
import shutil
import datetime
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from PIL import Image
import time
import pytesseract


def folder_maker(filename):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename), exist_ok=True)


def folder_name(filename):
    terrible = filename.split(".")[0]
    folder1 = terrible[2:6]
    try:
        number1 = int(terrible[6:])
        number2 = int(terrible[7:])
        number3 = int(terrible[8:])
        folder2 = ""
        folder3 = ""
        folder4 = ""
        numberlist = [0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000]
        for item in numberlist:
            if number1 > item and number1 <= item + 10000:
                var1 = str(item + 1)
                while len(var1) < 5:
                    var1 = "0" + var1
                folder2 = var1 + "-" + str(item + 10000)
        numberlist = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
        placeholder = terrible[6]
        for item in numberlist:
            if number2 > item and number2 <= item + 1000:
                var1 = str(item + 1)
                while len(var1) < 4:
                    var1 = "0" + var1
                var2 = str(item + 1000)
                if len(var2) > 4:
                    var2 = var2[:-1]
                var2 = placeholder + var2
                folder3 = placeholder + var1 + "-" + var2
        numberlist = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
        placeholder = terrible[6:8]
        for item in numberlist:
            if number3 > item and number3 <= item + 100:
                var1 = str(item + 1)
                var2 = str(item + 100)
                if len(var2) > 3:
                    var2 = str(int(placeholder + "000") + 1000)
                else:
                    var2 = placeholder + var2
                while len(var1) < 3:
                    var1 = "0" + var1
                folder4 = placeholder + var1 + "-" + var2
            elif number3 == 0:
                folder4 = str(int(placeholder) - 1) + "901-" + placeholder + "000"
        final = folder1 + "/" + folder2 + "/" + folder3 + "/" + folder4
        # print(final,"for",filename) print test to show destination folder
    except:
        # print(terrible[6:]) print test for errors
        final = "errors"
    return final


def row_converter(row, listy):
    # convert pandas row to a dictionary
    # requires a list of columns and a row as a tuple
    count = 1
    pictionary = {}
    pictionary['Index'] = row[0]
    for item in listy:
        pictionary[item] = row[count]
        count += 1
    print(pictionary)
    return pictionary


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparse = minidom.parseString(rough_string)
    return reparse.toprettyxml(indent="    ")

#toSort = input("folder to sort:")
toSort = "/media/sf_Z_DRIVE/Working/OAG/working/2022_066_20220803/2003"
#targetSort = input("where to put the sorted files: ")
targetSort = "/media/sf_Z_DRIVE/Working/OAG/working/presentation1"
for dirpath, dirnames, filenames in os.walk(toSort):
    for filename in filenames:
        sorting = folder_name(filename)
        sorting = targetSort + "/" + sorting + "/" + filename
        folder_maker(sorting)
        filename = os.path.join(dirpath, filename)
        if not os.path.isfile(sorting):
            shutil.copy2(filename, sorting)
            shutil.copystat(filename, sorting)
            print("copied", filename, "to", sorting)
        else:
            print(filename, "already copied")

#spreadsheet = input("input the spreadsheet name with filepath: ")
spreadsheet = "/media/sf_Z_DRIVE/Working/OAG/working/2022_066_20220803/Metadata for TSLAC 1997-2003/OpenRec2003.xls"
df = PD.read_excel(spreadsheet, dtype=object)
abbott_list = [304, 307, 349, 922, 2035, 2080, 304, 307, 3403, 3462, 349, 3947, 4480, 4797, 4803, 4864, 4906, 5032,
               5122, 5464, 5871, 6055, 6190, 6213, 6282, 6312, 6534, 6670]
listy = df.columns
for row in df.itertuples():
    valuables = row_converter(row, listy)
    my_dict = {}
    my_dict['creator'] = 'Texas Attorney General Open Records Division'
    dcterms = Element('dcterms:dcterms')
    dcterms.set('xsi:schemaLocation', "http://dublincore.org/documents/dcmi-terms/ qualifiedDcSchema.xsd")
    dcterms.set('xmlns', "http://dublincore.org/documents/dcmi-terms/")
    dcterms.set('xmlns:tslac', "https://www.tsl.texas.gov/")
    dcterms.set('xmlns:dcterms', "http://dublincore.org/documents/dcmi-terms/")
    dcterms.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
    creator = SubElement(dcterms, 'dcterms:creator')
    creator.text = 'Texas Attorney General Open Records Division'
    relation = SubElement(dcterms, 'dcterms:relation.isPartOf')
    relation.text = 'Texas Attorney General Open Records Letter Rulings'
    ocrNote = SubElement(dcterms, 'tslac:note')
    ocrNote.text = 'Optical character recognition of these files was completed using automated tools and have not been reviewed for accuracy.'
    valuables['status_date'] = str(valuables['status_date'])
    valuables['received_date'] = str(valuables['received_date'])
    date = valuables['status_date'].split(" ")[0]
    if "/" in date:
        date = date.split("/")
        year = int(date[2])
        day = date[0]
        if len(day) < 2:
            day = "0" + day
        month = date[1]
        if len(month) < 2:
            month = "0" + month
        date = date[2] + "-" + month + "-" + day
    year = int(date[:4])
    created = SubElement(dcterms, 'dcterms:date.created')
    created.text = date
    identifier1 = valuables['issued_as'][-2:]
    if int(identifier1) < 50:
        identifier1 = "20" + identifier1
    else:
        identifier1 = "19" + identifier1
    identifier2 = str(valuables['issued_as_num'])
    identifier3 = int(valuables['issued_as_num'])
    while len(identifier2) < 5:
        identifier2 = "0" + identifier2
    # identifier = SubElement(dcterms,'dcterms:identifier')
    identifierText = identifier1 + "-" + identifier2
    subject1 = "Texas. Attorney-General's Office"
    attyGen = ""
    if year >= 2015:
        attyGen = "Attorney General Ken Paxton"
        attyGen_subject = "Paxton, Ken, 1962-"
    if year > 2002 and year < 2015:
        attyGen = "Attorney General Greg Abbott"
        attyGen_subject = "Abbott, Greg, 1957-"
    if year == 2002:
        if identifier3 in abbott_list:
            attyGen = "Attorney General Greg Abbott"
            attyGen_subject = "Abbott, Greg, 1957-"
        if identifier3 >= 6816:
            if identifier3 < 6816:
                attyGen = "Attorney General John Cornyn"
                attyGen_subject = "Cornyn, John, 1952-"
    if year >= 1999 and year < 2002:
        attyGen = "Attorney General John Cornyn"
        attyGen_subject = "Cornyn, John, 1952-"
    if year >= 1991 and year < 1999:
        attyGen = "Attorney General Dan Morales"
        attyGen_subject = "Morales, Dan"
    if year >= 1989 and year < 1991:
        attyGen = "Attorney General Jim Mattox"
        attyGen_subject = "Mattox, Jim"
    title = SubElement(dcterms, 'dcterms:title')
    title.text = f'Open Records Letter Ruling {identifierText}'
    citation = SubElement(dcterms, 'dcterms:identifier.bibliographicCitation')
    citation.text = f"{title.text}, Texas Attorney General Open Records Letter Rulings, Texas Attorney General's records. Archives and Information Services Division, Texas State Library and Archives Commission."
    valuables['Last Name'] = str(valuables['Last Name'])
    valuables['First Name'] = str(valuables['First Name'])
    valuables['GB_Name'] = str(valuables['GB_Name'])
    valuables['gb_entity'] = str(valuables['gb_entity'])
    requestor1 = valuables['Last Name'] + ", " + valuables['First Name']
    requestor1_direct = valuables['First Name'] + " " + valuables['Last Name']
    #set default valuable to deal with blank entity fields
    requestor2 = "Unspecified government entity"
    if valuables['gb_entity'] != "":
        requestor2 = str(valuables['gb_entity']).title()
    requestor3 = valuables['GB_Name']
    if "&" not in requestor2 and ", " in requestor2:
        if "City" in requestor2:
            geo = requestor2.split(", ")[0] + " (Tex.)"
            geoTag = SubElement(dcterms, 'dcterms:coverage.spatial')
            geoTag.text = geo
            requestor2 = requestor2.split(", ")[1] + " " + requestor2.split(", ")[0]
        elif "County" in requestor2:
            geo = requestor2.split(", ")[0] + " County (Tex.)"
            geoTag = SubElement(dcterms, 'dcterms:coverage.spatial')
            geoTag.text = geo
            requestor2 = requestor2.split(", ")[0] + " County"
        elif ", " in requestor2 and len(requestor2.split(", ")) == 2:
            templist = requestor2.split(", ")
            requestor2 = templist[1] + " " + templist[0]
    keywords = [requestor1, requestor3, requestor2, attyGen]
    for item in keywords:
        keyword = SubElement(dcterms, 'tslac:keyword')
        keyword.text = item
    subject = SubElement(dcterms, "dcterms:subject")
    subject.text = subject1
    if requestor1_direct != requestor3:
        representation = f' of {requestor3}'
    else:
        representation = ""
    description = SubElement(dcterms, 'dcterms:description.abstract')
    description.text = f"{title.text} dated {created.text}, responding to a decision request from {requestor1_direct}{representation} on behalf of {requestor2}."
    oagID = SubElement(dcterms, 'tslac:attyGeneral.orlIdentifier')
    oagID.text = identifierText
    oagID2 = SubElement(dcterms, 'tslac:attyGeneral.requestIdentifier')
    while valuables['request_id'].endswith(" "):
        valuables['request_id'] = valuables['request_id'][:-1]
    oagID2.text = valuables['request_id']
    attyGeneral = SubElement(dcterms, 'tslac:attyGeneral.attyGeneralName')
    attyGeneral.text = attyGen
    oagRequestor = SubElement(dcterms, 'tslac:attyGeneral.requestorPerson')
    oagRequestor.text = valuables['Last Name'] + ", " + valuables['First Name']
    oagRequestorGov = SubElement(dcterms, "tslac:attyGeneral.requestorEntity")
    oagRequestorGov.text = str(valuables['gb_entity']).title()
    if valuables['gb_entity'] != valuables['GB_Name']:
        oagEntity = SubElement(dcterms, 'tslac:attyGeneral.requestorEntityRep')
        oagEntity.text = valuables['GB_Name'].title()
    dateReceived = SubElement(dcterms, 'tslac:attyGeneral.dateReceived')
    dateReceived.text = valuables['received_date'][:10]
    dateIssued = SubElement(dcterms, 'tslac:attyGeneral.dateIssued')
    dateIssued.text = valuables['status_date'][:10]
    toSave = "or" + identifier1 + identifier2 + ".pdf.xml"
    print(toSave)
    sorting = folder_name(toSave)
    sorting = targetSort + "/" + sorting + "/" + toSave

    metadatafile = "./2007/" + valuables['issued_as'] + identifier2 + ".pdf.xml"
    metadata = open(sorting, "wt", encoding="utf-8")
    metadata.write(prettify(dcterms))
    metadata.close()

print("all done")