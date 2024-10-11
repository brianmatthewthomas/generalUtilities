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
import tarfile
import time
from tqdm import tqdm
import PySimpleGUI as SG
import errno

my_icon = b'iVBORw0KGgoAAAANSUhEUgAAAHgAAABsCAQAAAALKr7UAAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAALEsAACxLAaU9lqkAAAAHdElNRQ' \
          b'fmAhQHBBtCNNv6AAANwUlEQVR42u2ca3hV5ZXHf0lObgRz4WK4WmpAEFFHFBTkMQWUoTyoiIpDrajcpGOFWsaOtCqgraIdO8pDp7VF' \
          b'awtVKlSpoigXUZDLYBlCRCAkJCEhIUDIhYSEJOec/3zYSdg7yd7nJDlJSJ78z6ez93r3Xuustde7bvtAJzrRiU50ohOd6EQnOtGJTv' \
          b'iBoA4kSyRdCKKc8x1f4K6M4naGcznBFJLCVrZxquPaaCIbKEWmTxX7mEd0R9RwBPN4mngq+YZdpFFFP0YyghjcrGcRaR1Lu+EsoRyR' \
          b'zEP0qD0axVjeowKxg6s7krjBLKAMsZ6r6p2L4kkKEVvp13EE/lfOID6kt83PMZdziN8T3jHE7c0exD4G2lK4eB43JUzuGOa8GA+FTH' \
          b'Kk6sFXiI/ocqmw7SK0iSuHkYVY4XP9DCop5jbzLdsO/fglPcgigwyyyaOAMjx+rQxhFv3J5LdU+aD8jMNcx93sQG0t8PX8svbp8nCe' \
          b'AvLIIp1jZJJDPueosF17FfchVnHE511Os5HrGE938ttS4HCm8wwJMUyilBxOhRRFl0VrALcAcIFiznCCDNJJJ4s8Cimr0RAA99OXE7' \
          b'xjOdYwxFbmk8DgthT4OyxiBpFDWMy9QClnya1W7nFyORtRElEVzzAA3JRylhwySSONTHI5SxzTCOJ9Uvy622FySeAadraNwMFMZCk3' \
          b'hTKFxVwDQBxx1XuLKKeIU5wgnXQyyOaUqzi2LJYEbgO8nOcsOVQwmAqO0IcCyn3e8SyZJDC4bWLpHszncbr15j+Yw2U+iKsoIZ8cMk' \
          b'ir1n0h52usWJzjDNmkksJRMkmnzDa5WMWDrOJhPx6AAGMUm/AEaay2q7Fwq1jHtEN/0bN6QCPVT10u5kYVnOKPRNnedyXibwS3rkl3' \
          b'ZSZP0S+Wx3iS+EYvDyGaaK5kDOChhEKyOUoKR8kgK6z4csYRY5P4BxEKuFt3WxrGM0wl9AYWM5mQZlwolQ0cwMMQJjEbqKKYl/gNnL' \
          b'Wtc4QQAxS3nkFH8DApKFKzdEzNgUfv6KpaQ47XMpVLkuYL8TFhtra1E7G4tcRNYCVlaJD+VM1e07FRPYS6Klgh6iEUruXyyq37hXjL' \
          b'1v324xhiZmsIG8q9JKFQTVOymosS3SE0XH9WvFz6je4RSlC6ypUoxK9subiVEspIbI3wYjnnUH8tV4maj32KU5jWqEQ3CL2iJPVUsN' \
          b'aoQNcI8bgtH08iUi+WAYJbSLf38D5PhFw2iXU8QdcAXPI0pURzLVEMBvbRj/54yaWIQvBw0mZZJBOAr8lrSYG/w6v8meF9eInVjAzY' \
          b'vhZKOacIYjjwLakUATHkUwLlFwWql6LcjJuNuFvKkMO4j30oRN/XLgUSebpWaJoK9JWi1FUT5VJ3JWm9XCKXQTaB7OuIQ/RtKXEH8Q' \
          b'YlqI9eVoECC69ek0vBmqhfKb56a5qnKr0uxDemmqUZ/0IOXpa0TAAdycN8i1y6U7t9sn9BVU3w0wsUUbsPB+suZUtaKMRmIhpMQt9G' \
          b'pNlov5m4ltWUowF6XUU+GD+h5zRB92udKhspcpn+qskapP5yyaW3pZpd+E8N6nA6pbhZGHj9xvA4aShcD2i/T6YLdHe1jqL1dhNM+4' \
          b'JylKLxQmNVqBKNkk0cdR1HEJvpHlhhg7iVj6hEg7VSpX4wvFahtWZ5i09rsMPf1UUuLVOWrhReHq7H12C2I04wOrDi9mIJJ1FXzdJh' \
          b'P9O8maam13eV3USBy/SIUE89rThRxrg6fN3ILkQRjwTSnMOYwi68aITWqcJPRrNN4T9KbEYMlq4RQi4FiZMWtxTBAxxBFDCvWYlZHQ' \
          b'xlJSXGb5wtqUzfKEnnfLK5zmTQ6HmTB35fS/WHRml8r25WkBCnuZeehBNBLyazhlJEFtMDF1R1Yz6pKFST9IU8kg5rqnqquyZqn48E' \
          b'b45J3BjtrD5erDkKFwrSKB1qhMgZGmNcq5RkNrGZQ5QjPGxhTOCi5IlswY0G6bfVLqek1u+i7+msA4M5GmIS+FYVVx9/16T3mY3YrK' \
          b'o02Ysoprz2qiV8xTwnz9y4iscQ5jOd2Bims4Ah1Qe3samWYC8HzX2NOthLuunb7bUt+v2mBsKHzOVmP9kpqDwKYfw3uxhGPJBLEgco' \
          b'Coxu43iCoyhE4/SJSQtlmmLSWqQ+dzDoeSbKy7Sj9sx/mccV9JjfUdj/poYVU8n3WyLdm8hmqtBAvVbHaLco2sTs9Tppy95JDTVRjj' \
          b'LtwQfVz3QmXv/np0W/9hkXOMXQwIeNf6AIxeixei6lQg+aWA3WKw78fahwE+0zFt3/xKLjBXL7I3DBlI8Q+4gLbGjxNBnIpfEWQ67B' \
          b'LnUzMXqVMhyynR+bKLvqC8vZ/eplOttXB/0JYk4M3Y14N3C7bRf+jT140dVa0aD3rdJcE5tBek5eH/lszWdknfTRrR9ZdPwzeXwKnH' \
          b'+6by7iF4HqAY1mLWWopxYqzeaWVr1coSMO7H1sSu3Q0/UdkHqYzg9Qik+Bk9xxbiq5KxDidmcZp1CEpmqH7W/t0U8tWlnooBWvFpgo' \
          b'o7S1HkWlHvXbWgy8oxCRe7FN1pzndg3eYI3UO475z2FdYWKxl5IcaE/rehPtjQ0+IDsUZ6IZ6LNsv1CIHYGoEH6PC8Gar1wfJZfnjE' \
          b'jWr93zU0WaaJ9qUHsV+oFFxy863v+8xgqxvLH5UEMBdhrHRR+b8acaHOddU7umG484BG1ik6mR24U7GuQyjFmm8UiximyH+58gBTzs' \
          b'bWzPqCGBc9khNlLquPA9jpm+TWK4UwjINktufoMN3WjuMH1LYa3DNZM5DQUcaLw3rg8vn1KVzCGHZbmsxlv7LZpHbXtZRqxsnk4Yax' \
          b'vbRzDL1Ob18hfb+jrsxg2pZAZCYNhDZiFbHJatt/wc4xnlQCs2m9rzkTYGbSCRsaZvB/nQhq6EvUY2UhoYgU+yHT6jxGZRGR+YBqqi' \
          b'mEmkwy0K+dxSur7RMdaZYxqb87DdZEdmHOMwVLGz8V3fhgX28DGVSSTbLLpQMwMEwMDqaSM7HOCwZQvo4aMEGmGxDrtEsxDy2N+UiM' \
          b'ruEUk7x6e2yVOExamvsdGDgc2m5nwEExz3keP8nAJLdT+4ARezkRV4IZkTgSy/Lkc32dQvKnWvJcbqqQ22+2WhbjZRDlOew956zpJ7' \
          b'IZf+WI+mWC8ZQWg+DwU2KZzA+Uh9YsPaBsVaWBtiG2d9qa4muscdAsYqLZXLctWp9TpURzTNoPmaCYGeT4ljD5pnEx+7tUxhFubGKa' \
          b'dBymdMNOH6h2NsHG254nAdrXPPfxgZVwVv892W6Bc9iwbquA17pZptCS2DNKuByLvIaIVUf4Y6hKu7NcAibp86xaICLTZi7ZP8xGEm' \
          b'q1m4kfwQvWnLYq5ut7AYqhfrVSp2WLQ2zzafytRoy7WitNJi/Em6S8FC7K7XZQggIliPJqnMVuQDutrCZqzW1KFYYjobpvdtrlNcx1' \
          b'mF6GemXkaFVmuQEOW8wRUtO5jyEFVxjt3ej9XTwuoAC3VxTaFcCA22ecqrtKSOs7rH5KxytEBRQhxnboNd4ICiL4fskrmaJHGFJfFD' \
          b't5jqWrsUYzozu0GD9jo4K6+2GT+Zl81+F6ubuRu/jAYry7Ff+6TxdNV+flDbInvB8oSvtSkjJNg4q2L92ighFbGMy2kljCA/RG84F9' \
          b'NMrRajGL+pugWTaDo6yKZRttzGWR3QVMPQk5namlPd4axFiT4a10c13ML2G9VlOXNw8qhNrXlZA86qTG8aer/AqgbeOmthTKE8Uut9' \
          b'1Je+UF+ThjdLkl60GPQam5XbTT+LEVmlaqZR4czkRy214zqnL1+iqT5HQ1dVl1lDNFulkkqNmlP1J8E2gKnUq+qtYEVqsjJUqfd0nR' \
          b'BuPuIm2gizqYrRNp/DvVv07/qhfqdCSdLXlp7EDIfmiUdJWqNNOqfj+rEReeexKLANlMYhnn3oh36NNVzcwF42BZ4u/dWPlR8YnsDL' \
          b'5yS29XvN8/F001eN6M1X6E7L8EqGD/pMPWHsxmd4vvW2IKcAJBk95PfoilSu8SaBH3SsWVdoXY1uv+T2FprvbTQW4I71+RybDXRprb' \
          b'gRWudAmap5uszQ7QtNePujxdCLfeg+h0Sifvt7uqIUpG76uc7bTlut0jAhPGxj/KWi2xrMpbKLbb7T8DDoVq3WHtshlYOaYcThJ3mW' \
          b'nlxyiGMbSnSc0vEf5/R7I+Vz8wljLtX/mribUpdWBEDcvbrHKBBlsbAt91tfiORdNFipzRI2Xy8bIywVrHOsyV8SGEEuWtCE4e6aMt' \
          b'wWjVeIECnMCci7Hy2MYF7A2606OWgssvSUuhuDgm+1nz8U6cs/0VjlN1LYcq2pSSH/ybT29c8a91Eaohf9mLK5iGTNMF5/zecV+tPO' \
          b'EM6bqJffkXWhXtOVxga0iXGBnGBuPQziWzReZ/x4H/QLTTQKNRn8lG60W0ynNFi/8OGts7XIKOKWsZrradcIYwXeWH3gUMtcqxGGk0' \
          b'riQcd+eTtBP3aia2xm7w5pllG5OMurDKCDIJGT6P7aqfaLUfLvjBc5PGzljvbppOyK9AuocGmpqVrl1S7dbYzzZ/OfPmYb2iGieAvF' \
          b'1qb3eVqq3kY1eW3bVRxbFv3ZiQZpv6q0QWOMst23zGyLanJrYTTHUaIeM9pmxfxPy7zLeSlhRvV/SnrZxZ1N/kOwdoRQFlFIHs/7mE' \
          b'btQHBxGzd1qH+57UQ7xv8DgC8wraZy+5gAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjItMDItMjBUMDc6MDQ6MjcrMDA6MDBxXqaVAAAA' \
          b'JXRFWHRkYXRlOm1vZGlmeQAyMDIyLTAyLTIwVDA3OjA0OjI3KzAwOjAwAAMeKQAAACZ0RVh0aWNjOmNvcHlyaWdodABObyBjb3B5cm' \
          b'lnaHQsIHVzZSBmcmVlbHmnmvCCAAAAIXRFWHRpY2M6ZGVzY3JpcHRpb24Ac1JHQiBJRUM2MTk2Ni0yLjFXrdpHAAAAInRFWHRpY2M6' \
          b'bWFudWZhY3R1cmVyAHNSR0IgSUVDNjE5NjYtMi4xa5wU+QAAABt0RVh0aWNjOm1vZGVsAHNSR0IgSUVDNjE5NjYtMi4xhWT+PAAAAA' \
          b'BJRU5ErkJggg=='


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
    print("starting tarball check")
    tar_list = []
    files_list = os.listdir(source)
    for item in tqdm(files_list):
        if os.path.isdir(os.path.join(source, item)):
            dirname_list.add(item)
        if os.path.isfile(os.path.join(source, item)) and item.endswith(".tar"):
            tar_list.append(os.path.join(source, item))
    dirname_list = list(dirname_list)
    dirname_list.sort()
    print("list of existing folders generated")
    print("compiled list of tarballs")
    for item in tqdm(tar_list):
        filename = item.split("/")[-1]
        my_len = len(filename) + 1
        root_filename = filename[:-4]
        if root_filename not in dirname_list:
            my_tarfile = item
            tar_dir = f"{item[:-my_len]}"
            print(f"opening {filename} tarfile at {time.asctime()}")
            tarball = tarfile.open(my_tarfile, "r")
            print(f"opened {filename} tarfile, extracting at {time.asctime()}")
            tarball.extractall(path=tar_dir)
            print(f"{filename} extracted to {tar_dir}/{root_filename} at {time.asctime()}")
            tarball.close()


def tar_check(source):
    dirname_list = set()
    print("starting tarball check")
    tar_list = []
    files_list = os.listdir(source)
    for item in tqdm(files_list):
        if os.path.isfile(os.path.join(source, item)) and item.endswith(".tar"):
            tar_list.append(os.path.join(source, item))
    dirname_list = list(dirname_list)
    dirname_list.sort()
    print("list of existing folders generated")
    print("compiled list of tarballs")
    for item in tqdm(tar_list):
        filename = item.split("/")[-1]
        my_len = len(filename) + 1
        root_filename = filename[:-4]
        tar_dir = item[:-my_len]
        my_tarfile = item
        tarball = tarfile.open(my_tarfile, "r")
        archive_list = tarball.getmembers()
        for thingy in archive_list:
            item_name = thingy.name
            if "." in item_name:
                if not os.path.isfile(f"{tar_dir}/{item_name}"):
                    tarball.extract(thingy, path=tar_dir)
                    print(f"{item_name} was missing from files, extracted again")
        tarball.close()


def process(source, target):
    counter = 0
    source_tiffs = set()
    source_pdfs = set()
    print("starting tiff copy-over")
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
    for directory in tqdm(source_tiffs):
        year = directory.split("/")[-3][:4]
        identifier = directory.split("/")[-3].split("-")[0]
        source_metadata = f"{directory.replace('01_tif', '')}metadata.untl.xml"
        target_directory = f"{target}/{year}/{identifier}/preservation1"
        target_metadata = f"{target_directory}/{identifier}.metadata"
        if os.path.isfile(source_metadata):
            create_directory(target_metadata)
            metadata = open(target_metadata, 'w', encoding='utf-8')
            metadata.write(transform_metadata(source_metadata))
            metadata.close()
        files = [q for q in os.listdir(directory) if os.path.isfile(f"{directory}/{q}")]
        print(f"processing {directory}")
        for file in tqdm(files):
            filename1 = os.path.join(directory, file)
            filename2 = os.path.join(target_directory, file)
            if not os.path.isfile(filename2):
                create_directory(filename2)
                shutil.copy2(filename1, filename2)
                shutil.copystat(filename1, filename2)
                source_checksum = create_sha256(filename1)
                target_checksum = create_sha256(filename2)
                if source_checksum != target_checksum:
                    print(f"something went wrong copying {filename1}, exiting, {time.asctime()}")
                    sys.exit()
    for directory in tqdm(source_pdfs):
        year = directory.split("/")[-3][:4]
        identifier = directory.split("/")[-3].split("-")[0]
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
        files_list = []
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
                print(f"{filename2} verified, {time.asctime()}")
                files_list.append(filename2)
        files_list.sort()
        counter += 1
        if not os.path.isfile(pdf_target):
            for my_file in files_list:
                merger.append(fileobj=open(my_file, 'rb'))
            merger.write(pdf_target)
            merger.close()
            print(f"{pdf_target} aggregated, moving on")

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
        sg.Push(),
        SG.Radio(text="Yes", group_id="tarball", key="-tarball_true-"),
        SG.Push(),
        SG.Radio(text="No", default=True, group_id="tarball", key="-tarball_false-")
    ],
    [
        SG.Text(text="Select execute to start, select close to close window")
    ],
    [
        SG.Button(button_text="Execute", blind_return_key=True),
        SG.Push(),
        SG.Button(button_text="Close")
    ],
    [
        SG.Push(),
        SG.Text("Total Volumes Progress"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.ProgressBar(max_value=1, orientation="h", size=(50, 5), key="-folder_progress-", border_width=5, relief="RELIEF_SUNKEN"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text(text="Current Volume Progress"),
        SG.Push()
    ],
    [
        SG.Text("What is happening")
    ],
    [
        SG.Push(),
        SG.Multiline(default_text="Click execute to start, this box will show progress\n-----------------------------------",
                     size=(70, 5), autoscroll=True, border_width=5, auto_refresh=True, reroute_stdout=False, key="-OUTPUT-"),
        SG.Push()
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
    if event == "Close" or event == SG.WIN_CLOSED:
        break

source = "/media/sf_Z_DRIVE/Working/Newspaper/incomplete/sn84022278"  # input("source folder: ")
target = "/media/sf_Z_DRIVE/Working/Newspaper/incomplete/processed/sn84022278_DallasHerald"  # input("target location of sorted files: ")
is_tarfile = input("was this received as tarballs? yes/no: ")
tarfile_opts = ['yes', 'no']
while is_tarfile not in tarfile_opts:
    print("wrong answer, type yes or no")
    is_tarfile = input("was this received as tarballs? yes/no: ")
if is_tarfile == "yes":
    print("making pass on already extracted tarballs just in case")
    process(source, target)
    print("starting extraction routine")
    tar_extract(source)
    print("rechecking extracted tarballs for missing files")
    tar_check(source)
    print(f"tar extractions verified, moving on to processing")
    process(source, target)
    print("making second pass on processing newspapers just in case")
if is_tarfile == "no":
    print("making first pass on processing newspaper")
    process(source, target)
    print("making second pass on processing newspaper just in case")
print("all done!")
