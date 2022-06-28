# meant for confederate pension applications to invert the name in the title from direct to indirect order
import lxml.etree as ET
import sys
import os


directory = "/media/sf_Z_DRIVE/Working/Ancestry/segmented/good_1677/staging/not_done/rejected" #input("directory of files to walk: ")
for dirpath, dirname, filenames in os.walk(directory):
    for filename in filenames:
        if "metadata" in filename:
            filename = os.path.join(dirpath, filename)
            metadata = ET.parse(filename)
            root = metadata.getroot()
            nsmap = root.nsmap
            nsmap['xmlns'] = nsmap[None]
            nsmap.pop(None,None)
            nsmap['dcterms'] = "http://dublincore.org/documents/dcmi-terms/"
            print(nsmap)
            titles = root.xpath(".//dcterms:title", namespaces=nsmap)
            if titles is not None:
                for title in titles:
                    titleText = title.text
                    if ", " not in titleText:
                        tempText = titleText.replace("Confederate pension application for ","")
                        templist = tempText.split(" ")[-1]
                        newText = tempText.replace(" " + templist,"")
                        newText = templist + ", " + newText
                        newTitleText = titleText.replace(tempText,newText)
                        print(newTitleText)
                        with open(filename, "r") as r:
                            filedata = r.read()
                            filedata = filedata.replace(">"+titleText+"<",">"+newTitleText+"<")
                            with open(filename, "w") as w:
                                w.write(filedata)
                            w.close()
                        print(filename,"processed")



