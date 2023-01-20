import lxml.etree as ET
import os

print("only works on tslac embedded metadata with prefix dcterms or tslac")
print("will dump the results into a file called crawl_results.txt as the base of the directory structure being crawled")

directory = input("metadata directory to crawl: ")
tag_name = input("tag name including prefix: ")

nsmap = {
    'dcterms': 'http://dublincore.org/documents/dcmi-terms/',
    'tslac': 'https://www.tsl.texas.gov/'
}
logfile = os.path.join(directory, "crawl_results.txt")

metadata_set = set()
counter = 0
for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        if "metadata" in filename:
            filename = os.path.join(dirpath, filename)
            dom = ET.parse(filename)
            root = dom.getroot()
            tags = root.xpath(f".//{tag_name}", namespaces=nsmap)
            if tags is not None:
                for tag in tags:
                    if tag.text is not None:
                        metadata_set.add(tag.text)
                        counter += 1
            print(f"{counter} so far, processed {filename}")
metadata_set = list(metadata_set)
metadata_set.sort()
text_string = ""
for item in metadata_set:
    text_string += item + "\n"
with open(logfile, "w") as w:
    w.write(f"results for {tag_name}:\n{text_string}")
w.close()
