import lxml.etree as ET
import os
import shutil

print("only works on tslac embedded metadata with prefix dcterms or tslac")
print("will dump the results into a file called crawl_results.txt as the base of the directory structure being crawled")

directory = "/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/newAPI/cpa/level3/numbered/level2" #input("metadata directory to crawl: ")
tag_name = input("tag name including prefix: ")

nsmap = {
    'dcterms': 'http://dublincore.org/documents/dcmi-terms/',
    'tslac': 'https://www.tsl.texas.gov/'
}
logfile = os.path.join(directory, "crawl_results.txt")
title_log = os.path.join(directory, "title_list.txt")
metadata_set = set()
counter = 0
titlelist = []
titleset = set()
title_dump = "/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/newAPI/errors"
for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        if "metadata" in filename and "IO_" in filename:
            filename2 = filename
            filename = os.path.join(dirpath, filename)
            dom = ET.parse(filename)
            root = dom.getroot()
            tags = root.xpath(f".//{tag_name}", namespaces=nsmap)
            if tags is not None:
                for tag in tags:
                    if tag.text is not None:
                        metadata_set.add(tag.text)
                        counter += 1
            title = root.find(".//dcterms:title", namespaces=nsmap)
            if title is not None:
                title = title.text
                if title in titlelist:
                    titleset.add(title)
                    print(title)
                    filename2 = os.path.join(title_dump, filename2)
                    shutil.copy2(filename, filename2)
                    shutil.copystat(filename, filename2)
                titlelist.append(title)
            print(f"{counter} so far, processed {filename}")
metadata_set = list(metadata_set)
metadata_set.sort()
text_string = ""
for item in metadata_set:
    text_string += item + "\n"
with open(logfile, "w") as w:
    w.write(f"results for {tag_name}:\n{text_string}")
w.close()
titleset = list(titleset)
titleset.sort()
text_string = ""
for item in titleset:
    text_string += item + "\n"
with open(title_log, "w") as w:
    w.write(text_string)
w.close()