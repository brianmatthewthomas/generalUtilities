import errno
import lxml.etree as ET
import shutil
import hashlib
import os
import sys
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
import PyPDF2

def create_directory(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

def create_sha256(filename):
    sha256 = hashlib.sha256()
    blocksize = 65536
    with open(filename, 'rb') as f:
        buffer = f.read(blocksize)
        while len(buffer) > 0:
            sha256.update(buffer)
            buffer = f.read(blocksize)
    fixity = sha256.hexdigest()
    return fixity

def prettyify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparse = minidom.parseString(rough_string)
    return reparse.toprettyxml(indent="    ")

def transform_metadata(filename):
    keyword_exceptions = ['newspapers', 'Newspapers']
    subject_exceptions = ['newspapers', 'Newspapers']
    nsmap = {'metadata': ""}
    dom = ET.parse(filename)
    root = dom.getroot()
    # find the singular details
    serial = ""
    serial_name = root.find(".//metadata:title[@qualifier = 'serialtitle']", namespaces=nsmap)
    if serial_name is not None:
        serial = f"{serial_name.text}"
    creator = ""
    creator_name = root.find(".//metadata:creator[@qualifier = 'edt']/metadata:name", namespaces=nsmap)
    if creator_name is not None:
        creator = creator_name.text
    proprietor = ""
    proprietor_name = root.find(".//metadata:contributor[@qualifier = 'ptr']/metadata:name", namespaces=nsmap)
    if proprietor_name is not None:
        proprietor = proprietor_name.text
    publisher = ""
    publisher_name = root.find(".//metadata:publisher/metadata:name", namespaces=nsmap)
    if publisher_name is not None:
        publisher = publisher_name.text
    publisher_location = ""
    publisher_location_name = root.find(".//metadata:publisher/metadata:location", namespaces=nsmap)
    if publisher_location_name is not None:
        publisher_location = f"({publisher_location_name.text})"
    date = ""
    date_name = root.find(".//metadata:date[@qualifier = 'creation']", namespaces=nsmap)
    if date_name is not None:
        date = date_name.text
    dateAvailable = ""
    if date != "":
        dateAvailable = str(int(date.split('-')[0]) + 95)
    language = ""
    language_name = root.find(".//metadata:language", namespaces=nsmap)
    if language_name is not None:
        language = language_name.text
    main_description = ""
    main_description_name = root.find(".//metadata:description[@qualifier = 'content']", namespaces=nsmap)
    if main_description_name is not None:
        main_description = main_description_name.text
    phys_details = ""
    phys_details_name = root.find(".//metadata:description[@qualifier = 'physical']", namespaces=nsmap)
    if phys_details_name is not None:
        phys_details = phys_details_name.text
    volume = ""
    volume_name = root.find(".//metadata:citation[@qualifier = 'volume']", namespaces=nsmap)
    if volume_name is not None:
        volume = volume_name.text
        while len(volume) < 3:
            volume = f"0{volume}"
        volume = f"Vol. {volume}"
    issue = ""
    issue_name = root.find(".//metadata:citation[@qualifier = 'issue']", namespaces=nsmap)
    if issue_name is not None:
        issue = issue_name.text
        while len(issue) < 3:
            issue = f"0{issue}"
        issue = f"No. {issue}"
    edition = ""
    edition_name = root.find(".//metadata:citation[@qualifier = 'edition']", namespaces=nsmap)
    if edition_name is not None:
        edition = edition_name.text
        edition = f"Ed. {edition}"
    # find the multiple details
    keywords = set()
    keywords_name = root.findall(".//metadata:subject[@qualifier = 'UNTL-BS']", namespaces=nsmap)
    if keywords_name is not None:
        for keyword in keywords_name:
            if keyword not in keyword_exceptions:
                keyword = keyword.text
                keyword = keyword.split(" - ")
                for item in keyword:
                    keywords.add(item)
    keywords = list(keywords)
    keywords.sort()
    geographic = set()
    geographic_name = root.findall(".//metadata:coverage[@qualifier = 'placeName']", namespaces=nsmap)
    states = ['Texas']
    abbreviation = ""
    if geographic_name is not None:
        for geography in geographic_name:
            geography = geography.text
            geography = geography.split(" - ")
            geographic.add(geography[0])
            if len(geography) > 1:
                if geography[1] in states:
                    abbreviation = f" ({geography[1][:3]}.)"
                geographic.add(geography[1])
                for item in geography[2:]:
                    geographic.add(f"{item}{abbreviation}")
    geographic = list(geographic)
    geographic.sort()
    subjects = set()
    subjects_name = root.findall(".//metadata:subject[@qualifier = 'LCSH']", namespaces=nsmap)
    if subjects_name is not None:
        for subject in subjects_name:
            subject = subject.text
            subject = subject.split(" -- ")
            for item in subject:
                if item not in geographic and item not in subject_exceptions:
                    while item.endswith("."):
                        item = item[:-1]
                    subjects.add(item)
    extra_text = set()
    extra_text_name = root.findall(".//metadata:note[@qualifier = 'display']", namespaces=nsmap)
    if extra_text_name is not None:
        for extra in extra_text_name:
            extra = extra.text
            extra_text.add(f" {extra}")
    extra_text = list(extra_text)
    dcterms = Element('dcterms:dcterms', {'xmlns': "http://dublincore.org/documents/dcmi-terms/",
                                          'xmlns:dcterms': "http://dublincore.org/documents/dcmi-terms/",
                                          'xmlns:tslac': "https://www.tsl.texas.gov/",
                                          'xsi:schemaLocation': "http://dublincore.org/documents/dcmi-terms/ qualifiedDcSchema.xsd",
                                          'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance"})
    title = f"{serial} {publisher_location}, {volume}, {issue}, {edition}, {date}"
    title = title.replace(" ,", ",")
    while title.endswith(",") or title.endswith(" "):
        title = title[:-1]
    title_xml = SubElement(dcterms, 'dcterms:title')
    title_xml.text = title
    relation_xml = SubElement(dcterms, "dcterms:relation.isPartOf")
    relation_xml.text = "Texas State Library and Archives Newspaper collection"
    citation_xml = SubElement(dcterms, "dcterms:identifier.bibliographicCitation")
    citation_xml.text = f"{title}, {relation_xml.text}. Archives and Information Services. Texas State Library and Archives Commission."
    description = f"{main_description}"
    for item in extra_text:
        description = f"{description} {item}"
    if serial != "":
        serial_xml = SubElement(dcterms, "dcterms:relation.isVersionOf")
        serial_xml.text = serial
        description = f"{description} {serial}"
    if creator != "":
        creator_xml = SubElement(dcterms, "dcterms:creator")
        creator_xml.text = creator
        description = f"{description}, editor {creator}"
    if not description.endswith("."):
        description = f"{description}."
    if publisher != "":
        publisher_xml = SubElement(dcterms, "dcterms:publisher")
        publisher_xml.text = publisher
    if date != "":
        date_xml = SubElement(dcterms, "dcterms:date.created")
        date_xml.text = date
    if dateAvailable != "":
        dateAvailable_xml = SubElement(dcterms, "dcterms:date.available")
        dateAvailable_xml.text = dateAvailable
    language_dict = {'eng': 'English', 'spa': "Spanish"}
    if language != "" and language in language_dict.keys():
        language_xml = SubElement(dcterms, "dcterms:language")
        language_xml.text = language_dict[language]
    description_xml = SubElement(dcterms, "dcterms:description.abstract")
    description_xml.text = description
    if volume != "":
        volume_xml = SubElement(dcterms, "dcterms:source.volume")
        volume_xml.text = str(int(volume.split(" ")[-1]))
    if issue != "":
        issue_xml = SubElement(dcterms, "dcterms:source.issue")
        issue_xml.text = str(int(issue.split(" ")[-1]))
    if edition != "":
        edition_xml = SubElement(dcterms, "dcterms:source.edition")
        edition_xml.text = edition.split(" ")[-1]
    for item in subjects:
        subject_xml = SubElement(dcterms, "dcterms:subject")
        subject_xml.text = item
    for item in geographic:
        geographic_xml = SubElement(dcterms, "dcterms:coverage.spatial")
        geographic_xml.text = item
    for item in keywords:
        keyword_xml = SubElement(dcterms, "tslac:keyword")
        keyword_xml.text = item
    types = ['Text', 'Newspapers']
    for item in types:
        type_xml = SubElement(dcterms, "dcterms:type")
        type_xml.text = item
    if phys_details != "":
        phys_details_xml = SubElement(dcterms, "tslac:note")
        phys_details_xml.text = phys_details
    if proprietor != "":
        proprietor_xml = SubElement(dcterms, "tslac:note")
        proprietor_xml.text = f"{proprietor}, proprietor."
    rights = SubElement(dcterms, 'dcterms:rights')
    rights.text = "If this newspaper issue was published 95 years ago or longer, it is in the Public Domain under the laws of the United States. If this issue was published less than 95 years ago, it is still within copyright under the laws of the United States. Unless expressly stated otherwise, the Texas State Library and Archives Commission makes no warranties about the Item and cannot guarantee the accuracy of this Rights Statement. You are responsible for your own use. Please contact the Texas State Library and Archives Commission for more information. You may need to obtain other permissions for your intended use. For example, other rights such as publicity, privacy or moral rights may limit how you may use the material."
    return prettyify(dcterms)


source = "/media/sf_X_DRIVE/DigitizationTransferFolder/tslac-newspapers-2023-08-08/sn86088196" #input("source folder: ")
target = "/media/sf_X_DRIVE/DigitizationTransferFolder/tslac-newspapers-2023-08-08/temp/Terry_County_Voice" #input("target location of sorted files: ")

source_tiffs = set()
source_pdfs = set()
for dirpath, dirnames, filenames in os.walk(source):
    for filename in filenames:
        if dirpath.endswith("01_tif"):
            source_tiffs.add(dirpath)
        if dirpath.endswith("02_pdf"):
            source_pdfs.add(dirpath)
source_tiffs = list(source_tiffs)
source_tiffs.sort()
source_pdfs = list(source_pdfs)
source_pdfs.sort()
for directory in source_tiffs:
    year = directory.split("/")[-2][:4]
    identifier = directory.split("/")[-2].split("-")[0]
    source_metadata = f"{directory.replace('01_tif', '')}metadata.untl.xml"
    target_directory = f"{target}/{year}/{identifier}/preservation1"
    target_metadata = f"{target_directory}/{identifier}.metadata"
    if os.path.isfile(source_metadata):
        create_directory(target_metadata)
        metadata = open(target_metadata, 'w', encoding='utf-8')
        metadata.write(transform_metadata(source_metadata))
        metadata.close()
    files = [q for q in os.listdir(directory) if os.path.isfile(f"{directory}/{q}")]
    for file in files:
        filename1 = os.path.join(directory, file)
        filename2 = os.path.join(target_directory, file)
        if not os.path.isfile(filename2):
            create_directory(filename2)
            shutil.copy2(filename1, filename2)
            shutil.copystat(filename1, filename2)
        source_checksum = create_sha256(filename1)
        target_checksum = create_sha256(filename2)
        if source_checksum != target_checksum:
            print(f"something went wrong copying {filename1}, exiting")
            sys.exit()
        print(f"{filename2} verified")
for directory in source_pdfs:
    year = directory.split("/")[-2][:4]
    identifier = directory.split("/")[-2].split("-")[0]
    source_metadata = f"{directory.replace('02_pdf', '')}metadata.untl.xml"
    target_directory = f"{target}/{year}/{identifier}/presentation2"
    target_metadata = f"{target_directory}/{identifier}.metadata"
    presentation3_metadata = f"{target}/{year}/{identifier}/presentation3/{identifier}.metadata"
    pdf_target = f"{target}/{year}/{identifier}/presentation3/{identifier}.pdf"
    pdf_target_metadata = f"{pdf_target}.metadata"
    if os.path.isfile(source_metadata):
        create_directory(target_metadata)
        target_metadata = open(target_metadata, 'wt', encoding='utf-8')
        target_metadata.write(transform_metadata(source_metadata))
        target_metadata.close()
        create_directory(presentation3_metadata)
        presentation3_metadata = open(presentation3_metadata, 'wt', encoding='utf-8')
        presentation3_metadata.write(transform_metadata(source_metadata))
        presentation3_metadata.close()
        create_directory(pdf_target_metadata)
        pdf_target_metadata = open(pdf_target_metadata, 'wt', encoding='utf-8')
        pdf_target_metadata.write(transform_metadata(source_metadata))
        pdf_target_metadata.close()
    merger = PyPDF2.PdfFileMerger()
    files = [q for q in os.listdir(directory) if os.path.isfile(f"{directory}/{q}")]
    files.sort()
    for file in files:
        filename1 = os.path.join(directory, file)
        filename2 = os.path.join(target_directory, file)
        if not os.path.isfile(filename2):
            create_directory(filename2)
            shutil.copy2(filename1, filename2)
            shutil.copystat(filename1, filename2)
        source_checksum = create_sha256(filename1)
        target_checksum = create_sha256(filename2)
        if source_checksum != target_checksum:
            print(f"something went wrong copying {filename1}, exiting")
            sys.exit()
        print(f"{filename2} verified")
        merger.append(fileobj=open(filename2, 'rb'))
    merger.write(pdf_target)
    merger.close()
    print(f"{pdf_target} aggregated, moving on")
print("all done!")
