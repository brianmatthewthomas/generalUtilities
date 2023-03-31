import sys
import os
import lxml.etree as ET

text_to_replace = input("text to replace if also a problem: ")
text_replacement = input("text to replace with: ")

size = input("number of characters in the digits: ")
size = int(size)
crawler = input("directory to crawl: ")
file_list = []
for dirpath, dirnames, filenames in os.walk(f'{crawler}/level2'):
    for filename in filenames:
        if filename.startswith("SO_") and "metadata" not in filename and "children" not in filename:
            filename1 = filename
            filename = os.path.join(dirpath, filename)
            print(filename)
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
                xipRef = dom.find('.//xip:Ref', namespaces=namespaces).text
                titleist = dom.find('.//xip:Title', namespaces=namespaces)
                title = titleist.text
                # rework the title
                math = title.split("-")[-1]
                math_original = math
                math2 = math
                try:
                    math = str(int(math))
                    math2 = math
                    while len(math) < size:
                        math = "0" + math
                        print(math)
                except:
                    print("something wrong in file, adjust manually")
                    file_list.append(filename)
                title2 = title.replace(math_original, math)
                title2 = title2.replace(text_to_replace, text_replacement)
                title3 = title2.replace(math, math2)
                title_concat = title.replace("-", "")
                title_concat2 = title2.replace("-", "")
                # get other data variables
                descriptionist = dom.find('.//xip:Description', namespaces=namespaces)
                entityURL = dom.find('.//EntityResponse:Self', namespaces=namespaces).text
                if descriptionist == None:
                    description = ""
                else:
                    description = descriptionist.text
                description = description.replace(title, title2)
                securityTag = dom.find('.//xip:SecurityTag', namespaces=namespaces).text
                parent = dom.find('.//xip:Parent', namespaces=namespaces).text
                if title != title2 or title != title3:
                    titleist.text = title2
                    descriptionist.text = description
                    filedata = ET.tostring(dom)
                    with open(filename, "wb") as w:
                        w.write(filedata)
                    w.close()
                    # correct the metadata file for the folder
                    for x, y, z in os.walk(f'{crawler}/level2'):
                        for zed in z:
                            if xipRef in zed and "metadata" in zed:
                                zed = os.path.join(x, zed)
                                with open(zed, "r") as r:
                                    filedata = r.read()
                                    if f">{title}<" in filedata or f">{title3}<" in filedata:
                                        filedata = filedata.replace(f">{title}<", f">{title2}<")
                                        filedata = filedata.replace(f">{title3}<", f">{title2}<")
                                        with open(zed, "w") as w:
                                            w.write(filedata)
                                        w.close()
                    # correct the metadata file for the item
                    # find the children
                    children_list = f'{crawler}/level3/{filename1[:-4]}_children.xml'
                    print(children_list)
                    dom2 = ET.parse(children_list)
                    root = dom2.getroot()
                    children = root.xpath(".//ChildrenResponse:Child", namespaces=namespaces)
                    for child in children:
                        child_type = child.attrib['type']
                        ref = child.attrib['ref']
                        child_title = child.attrib['title']
                        child_filename = f'{crawler}/level3/{child_type}_{child_title[:10]}_{ref}.xml'
                        child_metadata = f'{child_filename[:-4]}_metadata-1.xml'
                        print(child_metadata)
                        if os.path.isfile(child_metadata):
                            with open(child_metadata, 'r') as r:
                                filedata = r.read()
                                filedata = filedata.replace(f'>{title}-', f'>{title2}-')
                                filedata = filedata.replace(f' {title}-', f' {title2}-')
                                filedata = filedata.replace(f'>{title3}-', f'>{title2}-')
                                filedata = filedata.replace(f' {title3}-', f' {title2}-')
                                with open(child_metadata, 'w') as w:
                                    w.write(filedata)
                                w.close()
for dirpath, dirnames, filenames in os.walk(f"{crawler}/level3"):
    for filename in filenames:
        if "_children" in filename:
            filename = os.path.join(dirpath, filename)
            dom = ET.parse(filename)
            root = dom.getroot()
            children = root.xpath(".//ChildrenResponse:Child", namespaces=namespaces)
            counter = 0
            for child in children:
                counter += 1
            counter = len(str(counter))
            if counter > 1:
                for child in children:
                    child_type = child.attrib['type']
                    ref = child.attrib['ref']
                    child_title = child.attrib['title']
                    child_filename = f'{crawler}/level3/{child_type}_{child_title[:10]}_{ref}.xml'
                    child_metadata = f'{child_filename[:-4]}_metadata-1.xml'
                    print(child_metadata)
                    dom2 = ET.parse(child_metadata)
                    title = dom2.find(".//dcterms:title", namespaces=namespaces).text
                    title_list = title.split("-")
                    title_order = title_list[-1]
                    if len(title_order) < counter:
                        while len(title_order) < counter:
                            title_order = "0" + title_order
                        lengthy = len(title_list)
                        lengthy = lengthy - 1
                        title2 = ""
                        for item in title_list[:lengthy]:
                            title2 = title2 + item + "-"
                        title2 = title2 + title_order
                        print(title2)
                        with open(child_metadata, "r") as r:
                            filedata = r.read()
                            filedata = filedata.replace(title, title2)
                            with open(child_metadata, "w") as w:
                                w.write(filedata)
                            w.close()
print(f"manual checking needed for {file_list}")