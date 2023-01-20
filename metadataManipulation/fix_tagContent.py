import lxml.etree as ET
import os
from tqdm import tqdm

print("only works on tslac embedded metadata with prefix dcterms or tslac")
print("will dump the results into a file called crawl_results.txt as the base of the directory structure being crawled")

directory = input("metadata directory to crawl: ")
tag_list = []
done = "no"
while done == "no":
    tag_name = input("tag name including prefix: ")
    tag_list.append(tag_name)
    done = input('are you done? type "no" to keep adding tags to correct: ')

tag_dict = {}
done = "no"
while done == "no":
    to_replace = input("text to replace: ")
    to_insert = input("text to insert: ")
    tag_dict[to_replace] = to_insert
    done = input('are you done? type "no" to keep adding things to replace: ')

nsmap = {
    'dcterms': 'http://dublincore.org/documents/dcmi-terms/',
    'tslac': 'https://www.tsl.texas.gov/'
}
logfile = os.path.join(directory, "crawl_results.txt")
level = ""
metadata_set = set()
counter = 0
for dirpath, dirnames, filenames in os.walk(directory):
    for filename in tqdm(filenames):
        if "metadata" in filename:
            if dirpath != level:
                print(f"starting {dirpath}")
                level = dirpath
            filename = os.path.join(dirpath, filename)
            dom = ET.parse(filename)
            root = dom.getroot()
            for tag_name in tag_list:
                tags = root.xpath(f".//{tag_name}", namespaces=nsmap)
                if tags is not None:
                    for tag in tags:
                        if tag.text in tag_dict:
                            tag.text = tag_dict[tag.text]
                            filedata = ET.tostring(dom)
                            writer = open(filename, 'wb')
                            writer.write(filedata)
                            writer.close()
                            counter += 1
                            print(f"{counter} so far, processed {filename}")
print(f"{counter} files changed")
