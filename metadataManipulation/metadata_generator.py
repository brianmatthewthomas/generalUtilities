# A basic metadata generator that assumes column names will also be the element names
# also assumes dcterms metadata schema
# also assumes | separator for multiple terms in the same column
# you can build a mapping into the process as well, although that may be a pain in the rear

# import spreadsheet processing tools
import pandas as PD
# import xml constructing tools
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement


# local repeatable code
# convert a row into a dictionary
def row_converter(row, columns):
    count = 1
    pictionary = {}
    pictionary['Index'] = row[0]
    for item in columns:
        pictionary[item] = row[count]
        count += 1
    # uncomment next line to activate the dictionary mapping function. also, modify the map based on spreadsheet needs
    # pictionary = dictionary_mapping(pictionary)
    return pictionary

# for if mapping of spreadsheet elements is needed
def dictionary_mapping(pictionary):
    # map CANNOT have the same value twice
    dict_map = {'Title': 'dcterms:title',
                'Volume': 'dcterms:volume',
                'Issue': 'dcterms:issue',
                'Publication Date': 'dcterms:date',
                'County': 'dcterms:coverage.spatial',
                'City': 'tslac:city',
                'Subjects': 'dcterms:subject',
                'Keywords': 'tslac:keyword',
                'Repository': 'dcterms:source.location',
                'Frequency': 'tslac:publication.interval',
                'Extent': 'dcterms:extent',
                'Recommended Citation': 'dcterms:identifier.bibliographicCitation',
                'Notes': 'tslac:notes',
                'Creative Commons License': 'dcterms:rights',
                'Rights Statement': 'dcterms:moreRights'}
    new_dict = {}
    for key in dict_map.keys():
        if key not in pictionary:
            continue
        new_dict[dict_map['key']] = pictionary[key]
        return new_dict


# convert xml object into a string that can be written
def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparse = minidom.parseString(rough_string)
    return reparse.toprettyxml(indent="    ")


your_spreadsheet = input("full filepath for spreadsheet: ")

dataframe = PD.read_excel(your_spreadsheet, enging="openpyxl")
columns = dataframe.columns()

for row in dataframe.itertuples():
    my_metadata = row_converter(row, columns)
    # designate how you will construct metadata export, below assumes a column called export_filename
    export_file = f"{my_metadata['export_filename']}.metadata"
    # assuming dcterms data paradigm, change as you will
    metadata = Element('dcterms:dcterms', {'xmlns': "http://dublincore.org/documents/dcmi-terms/",
                                          'xmlns:dcterms': "http://dublincore.org/documents/dcmi-terms/",
                                          'xmlns:tslac': "https://www.tsl.texas.gov/",
                                          'xsi:schemaLocation': "http://dublincore.org/documents/dcmi-terms/ qualifiedDcSchema.xsd",
                                          'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance"})
    for key in my_metadata.keys():
        if key != 'Index' and key != 'export_filename':
            # name element after column header
            element_name = key
            # get content by key in dictionary
            # convert to string just in case pandas made it a non-string type of thing
            element_text = str(my_metadata[key])
            # make an element only if there is data there
            if element_text != "":
                # use pipe| separator for multiple terms in same column, can be anything crazy
                if "|" in element_text:
                    element_text = element_text.split("|")
                    for data in element_text:
                        my_element = SubElement(metadata, key)
                        my_element.text = data
                else:
                    my_element = SubElement(metadata, key)
                    my_element.text = element_text
    with open(export_file, "w", encoding='utf-8') as w:
        w.write(prettify(metadata))
    w.close()
    print(f"{export_file} generated")
print("all done :)")