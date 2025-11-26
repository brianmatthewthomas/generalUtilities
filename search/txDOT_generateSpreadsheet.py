import pandas as PD
import os
'''
main_frame = PD.DataFrame()

the_file = "/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/newAPI/correcto/IO_000120375_dcfb0832-e02a-45b2-97dd-9c658cd50ff6_metadata-1.xml"

df = PD.read_xml(the_file, xpath=".//dcterms:dcterms",
                 elems_only=True,
                 namespaces={"dcterms": "http://dublincore.org/documents/dcmi-terms/", "tslac": "https://www.tsl.texas.gov/"})
df['link'] = f"https://tsl.access.preservica.com/uncategorized/IO_{the_file.split('_')[-2]}/"
print(df)
print(main_frame)
main_frame = main_frame.append(df)
print(main_frame)
writer = main_frame.to_excel("H:/harvest/agencies/txDOT/RoW/level2/AMA.xlsx", index=False)
'''
# start crawl
your_frame = PD.DataFrame()
to_crawl = "H:/harvest/agencies/txDOT/RoW/level2/YKM"
for dirpath, dirnames, filenames in os.walk(to_crawl):
    for filename in filenames:
        if filename.endswith("_metadata-1.xml") and filename.startswith("IO_"):
            print(filename)
            try:
                filename = os.path.join(dirpath, filename)
                df = PD.read_xml(filename, xpath=".//dcterms:dcterms", elems_only=True,
                                 namespaces={"dcterms": "http://dublincore.org/documents/dcmi-terms/", "tslac": "https://www.tsl.texas.gov/"})
                df['link'] = f"https://tsl.access.preservica.com/uncategorized/IO_{filename.split('_')[-2]}/"
                #print(df)
                your_frame = PD.concat([your_frame, df], ignore_index=True)
            except:
                continue
        if filename.endswith("_metadata-2.xml") and filename.startswith("IO_"):
            print(filename)
            try:
                filename = os.path.join(dirpath, filename)
                df = PD.read_xml(filename, xpath=".//dcterms:dcterms", elems_only=True,
                                 namespaces={"dcterms": "http://dublincore.org/documents/dcmi-terms/", "tslac": "https://www.tsl.texas.gov/"})
                df['link'] = f"https://tsl.access.preservica.com/uncategorized/IO_{filename.split('_')[-2]}/"
                #print(df)
                your_frame = PD.concat([your_frame, df], ignore_index=True)
            except:
                continue

writer = your_frame.to_excel("H:/harvest/agencies/txDOT/RoW/level2/YKM_data.xlsx",index=False)