import lxml.etree as ET
import shutil
import hashlib
import os
import sys
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
import PyPDF2
import tarfile
import time
import PySimpleGUI as SG
import errno

my_icon = b'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'


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
        volume = str(volume_name.text).replace('[', '').replace(']', '')
        while len(volume) < 3:
            volume = f"0{volume}"
        volume = f"Vol. {volume}"
    issue = ""
    issue_name = root.find(".//metadata:citation[@qualifier = 'issue']", namespaces=nsmap)
    if issue_name is not None:
        issue = str(issue_name.text).replace('[', '').replace(']', '')
        while len(issue) < 3:
            issue = f"0{issue}"
        issue = f"No. {issue}"
    edition = ""
    edition_name = root.find(".//metadata:citation[@qualifier = 'edition']", namespaces=nsmap)
    if edition_name is not None:
        edition = str(edition_name.text).replace('[', '').replace(']', '')
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
    title = title.replace(" ,", ",").replace(',,', ',')
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


def tar_extract(source):
    dirname_list = set()
    window['-STEP-'].update("What we are doing: Tarball extraction")
    window['-OUTPUT-'].update(f"\nstarting tarball check", append=True)
    tar_list = []
    files_list = os.listdir(source)
    for item in files_list:
        if os.path.isdir(os.path.join(source, item)):
            dirname_list.add(item)
        if os.path.isfile(os.path.join(source, item)) and item.endswith(".tar"):
            tar_list.append(os.path.join(source, item))
    dirname_list = list(dirname_list)
    dirname_list.sort()
    window['-OUTPUT-'].update(f"\nlist of existing folders generated", append=True)
    window['-OUTPUT-'].update(f"\ncompiled list of tarballs", append=True)
    tar_count = len(tar_list)
    tar_processed = 0
    for item in tar_list:
        filename = item.split("\\")[-1]
        my_len = len(filename) + 1
        root_filename = filename[:-4]
        window['-OUTPUT-'].update(f"\nChecking {root_filename}", append=True)
        if root_filename not in dirname_list:
            my_tarfile = item
            tar_dir = f"{item[:-my_len]}"
            window['-OUTPUT-'].update(f"\nopening {filename} tarfile at {time.asctime()}", append=True)
            tarball = tarfile.open(my_tarfile, "r")
            window['-OUTPUT-'].update(f"\nopened {filename} tarfile, extracting at {time.asctime()}", append=True)
            tarball.extractall(path=tar_dir)
            window['-OUTPUT-'].update(f"\n{filename} extracted to {tar_dir}/{root_filename} at {time.asctime()}", append=True)
            tarball.close()
        tar_processed += 1
        window['-folder_progress-'].update_bar(tar_processed, tar_count)



def tar_check(source):
    dirname_list = set()
    window['-STEP-'].update("What we are going: checking tar extraction")
    window['-OUTPUT-'].update("\nstarting tarball check", append=True)
    tar_list = []
    files_list = os.listdir(source)
    for item in files_list:
        if os.path.isfile(os.path.join(source, item)) and item.endswith(".tar"):
            tar_list.append(os.path.join(source, item))
    dirname_list = list(dirname_list)
    dirname_list.sort()
    window['-OUTPUT-'].update("\nlist of existing folders generated", append=True)
    window['-OUTPUT-'].update("\ncompiled list of tarballs", append=True)
    tar_count = len(tar_list)
    tar_checked = 0
    for item in tar_list:
        filename = item.split("\\")[-1]
        my_len = len(filename) + 1
        root_filename = filename[:-4]
        tar_dir = item[:-my_len]
        my_tarfile = item
        tarball = tarfile.open(my_tarfile, "r")
        archive_list = tarball.getmembers()
        archive_count = len(archive_list)
        archive_processed = 0
        for thingy in archive_list:
            item_name = thingy.name
            if "." in item_name:
                if not os.path.isfile(f"{tar_dir}/{item_name}"):
                    tarball.extract(thingy, path=tar_dir)
                    window['-OUTPUT-'].update(f"\n{item_name} was missing from files, extracted again", append=True)
            archive_processed += 1
            window['-folder_progress-'].update_bar(archive_processed, archive_count)
        tarball.close()
        tar_checked += 1
        window['-overall_progress-'].update_bar(tar_checked, tar_count)


def process(source, target):
    counter = 0
    source_tiffs = set()
    source_pdfs = set()
    window['-STEP-'].update("What we are doing: Processing tiff folders")
    window['-OUTPUT-'].update("\nstarting tiff copy-over", append=True)
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
    pdf_count = len(source_pdfs)
    for directory in source_tiffs:
        year = directory.split("\\")[-3][:4]
        identifier = directory.split("\\")[-3].split("-")[0]
        source_metadata = f"{directory.replace('01_tif', '')}metadata.untl.xml"
        target_directory = f"{target}\\{year}\\{identifier}\\preservation1"
        target_metadata = f"{target_directory}\\{identifier}.metadata"
        if os.path.isfile(source_metadata):
            create_directory(target_metadata)
            metadata = open(target_metadata, 'w', encoding='utf-8')
            metadata.write(transform_metadata(source_metadata))
            metadata.close()
        files = [q for q in os.listdir(directory) if os.path.isfile(f"{directory}/{q}")]
        window['-OUTPUT-'].update(f"\nprocessing {directory}", append=True)
        tiff_counter = 0
        tiff_number = len(files)
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
                    window['-OUTPUT-'].update(f"\nsomething went wrong copying {filename1}, exiting, {time.asctime()}", append=True)
                    sys.exit()
            tiff_counter += 1
            window['-folder_progress-'].update_bar(tiff_counter, tiff_number)
        counter += 1
        window['-overall_progress-'].update_bar(counter, pdf_count)
    counter = 0
    window['-STEP-'].update("What we are doing: PDF processing")
    for directory in source_pdfs:
        year = directory.split("\\")[-3][:4]
        identifier = directory.split("\\")[-3].split("-")[0]
        source_metadata = f"{directory.replace('02_pdf', '')}metadata.untl.xml"
        target_directory = f"{target}\\{year}\\{identifier}\\presentation2"
        target_metadata = f"{target_directory}\\{identifier}.metadata"
        presentation3_metadata = f"{target}\\{year}\\{identifier}\\presentation3\\{identifier}.metadata"
        pdf_target = f"{target}\\{year}\\{identifier}\\presentation3\\{identifier}.pdf"
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
        merger = PyPDF2.PdfMerger()
        files = [q for q in os.listdir(directory) if os.path.isfile(f"{directory}/{q}")]
        files.sort()
        files_list = []
        pdf_counter = 0
        pdf_number = len(files)
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
                    window['-OUTPUT-'].update(f"\nsomething went wrong copying {filename1}, exiting", append=True)
                    sys.exit()
                window['-OUTPUT-'].update(f"\n{filename2} verified, {time.asctime()}", append=True)
                files_list.append(filename2)
            pdf_counter += 1
            window['-folder_progress-'].update_bar(pdf_counter, pdf_number)
        files_list.sort()
        counter += 1
        if not os.path.isfile(pdf_target):
            for my_file in files_list:
                merger.append(fileobj=open(my_file, 'rb'))
            merger.write(pdf_target)
            merger.close()
            window['-OUTPUT-'].update(f"\n{pdf_target} aggregated, moving on", append=True)
        window['-overall_progress-'].update_bar(counter, pdf_count)

SG.theme("DarkGreen4")
layout = [
    [
        SG.Push(),
        SG.Text(text="Path to newspaper files"),
        SG.In(default_text="", size=(50, 1), visible=True, key="-source-"),
        SG.FolderBrowse()
    ],
    [
        SG.Push(),
        SG.Text(text="Path to output processed newspaper files"),
        SG.In(default_text="", size=(50, 1), visible=True, key="-target-"),
        SG.FolderBrowse()
    ],
    [
        SG.Text(text="Did this come as tarfiles?"),
        SG.Push(),
        SG.Radio(text="Yes", group_id="tarball", key="-tarball_true-"),
        SG.Push(),
        SG.Radio(text="No", default=True, group_id="tarball", key="-tarball_false-")
    ],
    [
        SG.Text(text="Select execute to start, select close to close window")
    ],
    [
        SG.Button(button_text="Execute", bind_return_key=True),
        SG.Push(),
        SG.Button(button_text="Close")
    ],
    [
        SG.Push(),
        SG.Text("What we are doing", key="-STEP-"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text("Total Progress"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.ProgressBar(max_value=1, orientation="h", size=(50, 5), key="-overall_progress-", border_width=5, relief="RELIEF_SUNKEN"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text(text="Current Progress"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.ProgressBar(max_value=1, orientation="h", size=(50, 5), key="-folder_progress-", border_width=5, relief="RELIEF_SUNKEN"),
        SG.Push()
    ],
    [
        SG.Text("What is happening")
    ],
    [
        SG.Image(my_icon),
        SG.Multiline(default_text="Click execute to start, this box will show progress\n-----------------------------------",
                     size=(70, 5), autoscroll=True, border_width=5, auto_refresh=True, reroute_stdout=False, key="-OUTPUT-"),
        SG.Image(my_icon)
    ],
]

window = SG.Window(
    "Newspaper processor",
    layout,
    icon=my_icon,
    button_color="dark green"
)

event, values = window.read()
while True:
    event, values = window.read()
    source = values["-source-"]
    target = values['-target-']
    is_tarfile = False
    if values['-tarball_true-'] is True:
        is_tarfile = True
    if event == "Execute":
        if is_tarfile is True:
            window['-OUTPUT-'].update(f"\nMaking pass on already extracted tarballs just in case something got missed", append=True)
            process(source, target)
            window['-OUTPUT-'].update(f"\nStarting extraction routine", append=True)
            tar_extract(source)
            window['-OUTPUT-'].update(f"\nRechecking extracted tarballs for missing files", append=True)
            tar_check(source)
            window['-OUTPUT-'].update(f"\nTar extractions verified, moving on to processing", append=True)
            process(source, target)
            window['-OUTPUT-'].update(f"\nAll Done", append=True)
        if is_tarfile is False:
            window['-OUTPUT-'].update(f"\nMaking first pass on processing newspaper", append=True)
            process(source, target)
            window['-OUTPUT-'].update(f"\nMaking second pass on processing newspaper just in case", append=True)
            process(source, target)
            window['-OUTPUT-'].update(f"\nAll Done", append=True)
    if event == "Close" or event == SG.WIN_CLOSED:
        break
window.close()
