# meant for confederate pension applications to invert the name in the title from direct to indirect order
import lxml.etree as ET
import sys
import os


directory = input("directory to manipulate data in: ")
output = input("target location of copies of files processed: ")
logger = f"{directory}/logger.txt"
log = open(logger, "a")
for dirpath, dirname, filenames in os.walk(directory):
    for filename in filenames:
        if "metadata" in filename and "IO" in filename:
            filename = os.path.join(dirpath, filename)
            print(filename)
            with open(filename, "r") as r:
                filedata = r.read()
                if "militaryDept.soldier>" not in filedata:
                    metadata = ET.parse(filename)
                    root = metadata.getroot()
                    nsmap = root.nsmap
                    nsmap['xmlns'] = nsmap[None]
                    nsmap.pop(None,None)
                    nsmap['dcterms'] = "http://dublincore.org/documents/dcmi-terms/"
                    nsmap['tslac'] = "https://www.tsl.texas.gov/"
                    print(nsmap)
                    soldiers = root.xpath(".//tslac:keyword", namespaces=nsmap)
                    rights = root.find(".//dcterms:identifier.bibliographicCitation", namespaces=nsmap)
                    for soldier in soldiers:
                        soldier_name = soldier.text
                        print(soldier_name)
                        if soldier_name is not None and "Mrs." not in soldier_name:
                            subelement = ET.Element('militaryDept.soldier')
                            subelement.text = soldier_name
                            subelement = rights.addnext(subelement)
                            #subelement.text = soldier_name
                            filedata = ET.tostring(metadata)
                            writer = open(filename, 'wb')
                            writer.write(filedata)
                            writer.close()
                            with open(filename, "r") as r:
                                filedata = r.read()
                                filedata = filedata.replace("militaryDept.soldier>", "tslac:militaryDept.soldier>")
                                with open(filename, "w") as w:
                                    w.write(filedata)
                                w.close()
                                filename2 = filename.split("/")[-1]
                                filename2 = os.path.join(output, filename2)
                                with open(filename2, "w") as w:
                                    w.write(filedata)
                                w.close()
                            log.write(soldier_name + "\n")
log.close()
