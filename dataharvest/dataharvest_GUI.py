import os
import requests
import sys
import time
import csv
import lxml.etree as ET
import PySimpleGUI as SG

from preservation_utilities import preservation_utilities

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


def login(login_url, login_payload):
    auth = requests.post(login_url, data=login_payload).json()
    session_token = auth['token']
    login_headers = {'Preservica-Access-Token': session_token, 'Content-Type': 'application/xml',
                     'Accept-Charset': 'UTF-8'}
    return login_headers

def getNamespaces(root):
    namespaces = root.nsmap
    namespaces['xmlns'] = namespaces[None]
    namespaces.pop(None, None)
    namespaces['dcterms'] = "http://dublincore.org/documents/dcmi-terms/"
    namespaces['tslac'] = 'https://www.tsl.texas.gov/'
    namespaces['MetadataResponse'] = namespaces['xmlns']
    namespaces['EntityResponse'] = namespaces['xmlns']
    namespaces['ChildrenResponse'] = namespaces['xmlns']
    print(namespaces)
    return namespaces

def newDirpath(dirpath):
    dirpath = str(dirpath)
    if dirpath.endswith("/"):
        dirpath = dirpath[:-1]
    try:
        dirlevel2 = int(dirpath[-2:])
        dirlevel2 += 1
        return dirlevel2
    except:
        dirlevel2 = int(dirpath[-1:])
        dirlevel2 += 1
        return dirlevel2


def harvest(valuables, pair_list):
    url = f"https://{valuables['prefix']}.preservica.com/api/accesstoken/login"
    payload = {'username': valuables['username'], 'password': valuables['password'], 'tenant': valuables['tenant']}
    print("logging in...")
    window['-OUTPUT-'].update("\nlogging in", append=True)
    headers = preservation_utilities.login(url, payload)
    print(headers)
    timer = time.time() + 600
    base_station = valuables['location']
    preservation_utilities.dirMaker(f"{base_station}/something.txt")
    logger = open(f"{base_station}/log_UUID-potential_fails.txt", "a")
    logger2 = open(f"{base_station}/log_UUID-MD-addedTo.txt", "a")
    level = 1
    add_counter = 0
    base_url = f"https://{valuables['prefix']}.preservica.com/api/entity/"
    so = "structural-objects/"
    dublin_core = "http://dublincore.org/documents/dcmi-terms/"
    metadata = valuables['metadata_file']
    uuid = valuables['uuid']
    jump_point = base_url + so + uuid
    response = requests.get(jump_point, headers=headers)
    dir_level = base_station + "/level" + str(level) + "/"
    filename = dir_level + "SO_" + uuid + ".xml"
    level += 1
    dir_level = dir_level + "level" + str(level) + "/"
    children_of_the_object = dir_level + "SO_" + uuid + "_children.xml"
    preservation_utilities.dirMaker(filename)
    preservation_utilities.dirMaker(children_of_the_object)
    preservation_utilities.filemaker(filename, response)
    response = requests.get(jump_point + "/children?start=0&max=1000", headers=headers)
    status = response.status_code
    if status == 401:
        print(children_of_the_object, "may have failed, logging back in")
        logger.write(children_of_the_object + "\n")
        headers = preservation_utilities.login(url, payload)
        response = requests.get(jump_point + "/children?start=0&max=1000", headers=headers)
        preservation_utilities.filemaker(children_of_the_object, response)
    else:
        preservation_utilities.filemaker(children_of_the_object, response)
    dom3 = ET.parse(children_of_the_object)
    root3 = dom3.getroot()
    namespaces = getNamespaces(root3)
    things = root3.xpath('.//ChildrenResponse:TotalResults', namespaces=namespaces)
    for thing in things:
        hits = int(thing.text)
        children_start = 1000
        root_child = jump_point + "/children?start="
        max_child = "&max=1000"
        if hits > 1000:
            while children_start <= hits:
                child_file = os.path.join(dir_level, "SO_" + uuid + "_" + str(children_start) + "_children.xml")
                response = requests.get(root_child + str(children_start) + max_child, headers=headers)
                preservation_utilities.filemaker(child_file, response)
                children_start = children_start + 1000
    dir_level2 = dir_level
    print("making recursive structure")
    while level != 21:
        level += 1
        dir_level2 = dir_level2 + "level" + str(level) + "/"
        dummy = os.path.join(dir_level2, "filename.txt")
        preservation_utilities.dirMaker(dummy)
    dom = ET.parse(filename)
    root = dom.getroot()
    namespaces = getNamespaces(root)
    version = namespaces['xmlns'].split("/")[-1]
    elements = root.xpath(f'.//EntityResponse:Fragment[not((@schema="http://preservica.com/LegacyXIP") or '
                          f'(@schema="http://preservica.com/ExtendidXIP/{version}"))]', namespaces=namespaces)
    element_counter = 0
    my_list = []
    for element in elements:
        types = element.get('schema')
        my_list.append(types)
    if dublin_core not in my_list:
        purl2 = jump_point + "/metadata"
        responsible = requests.post(purl2, headers=headers, data=open(metadata, 'rb'))
        response = requests.get(jump_point, headers=headers)
        add_counter += 1
        preservation_utilities.filemaker(filename, response)
        dom = ET.parse(filename)
        root = dom.getroot()
        namespaces = getNamespaces(root)
        elements = root.xpath(f'.//EntityResponse:Fragment[not((@schema="http://preservica.com/LegacyXIP") or '
                              f'(@schema="http://preservica.com/ExtendedXIP/{version}"))]', namespaces=namespaces)
    for element in elements:
        try:
            elemental = element.text
            element_counter += 1
            response = requests.get(elemental, headers=headers)
            preservation_utilities.filemaker(filename[:-4] + "_metadata-" + str(element_counter) + ".xml", response)
        except:
            continue
    list_of_files = []
    list_of_existing_files = []
    print("getting list of existing files")
    for dirpath, dirnames, filenames in os.walk(dir_level):
        for filename in filenames:
            filename = os.path.join(dirpath, filename)
            list_of_existing_files.append(filename)
    print("list generation complete")
    for dirpath, dirnames, filenames in os.walk(dir_level):
        for filename in filenames:
            filename = os.path.join(dirpath, filename)
            if "children" in filename:
                try:
                    dom = ET.parse(filename)
                except OSError:
                    print("trouble reading", filename, ",", add_counter, "files had dcterms added to them")
                    sys.exit()
                root = dom.getroot()
                namespaces = getNamespaces(root)
                name = dom.find(".//ChildrenResponse:Self", namespaces=namespaces).text
                name = name.split("/")[-2]
                window['-OUTPUT-'].update(f"\nworking on {name}")
                root = dom.getroot()
                elements = root.xpath(".//ChildrenResponse:Child[@type='SO']", namespaces=namespaces)
                status = len(elements)
                counter = 0
                for element in elements:
                    counter += 1
                    window['-Progress-'].update_bar(counter, status)
                    try:
                        elemental = element.text
                        types = element.get('type')
                        uuid = element.get('ref')
                        new_file = os.path.join(dirpath, types + "_" + uuid + ".xml")
                        list_of_files.append(new_file)
                        if new_file not in list_of_existing_files:
                            response = requests.get(elemental, headers=headers)
                            status = response.status_code
                            if status == 401:
                                print(new_file, "may have failed, logging back in")
                                logger.write(new_file + "\n")
                                headers = preservation_utilities.login(url, payload)
                                response = requests.get(elemental, headers=headers)
                                preservation_utilities.filemaker(new_file, response)
                            else:
                                preservation_utilities.filemaker(new_file, response)
                        dom2 = ET.parse(new_file)
                        root2 = dom2.getroot()
                        namespaces = getNamespaces(root2)
                        version = namespaces['xmlns'].split("/")[-1]
                        things = root2.xpath('.//EntityResponse:Fragment', namespaces=namespaces)
                        my_list = []
                        for thing in things:
                            dc_type = thing.get('schema')
                            my_list.append(dc_type)
                        print(my_list)
                        if dublin_core not in my_list:
                            print(uuid, "missing dcterms, adding them")
                            purl2 = elemental + "/metadata"
                            responsible = requests.post(purl2, headers=headers, data=open(metadata, 'rb'))
                            response = requests.get(elemental, headers=headers)
                            add_counter += 1
                            preservation_utilities.filemaker(new_file, response)
                            logger2.write(elemental + "\n")
                        dom2 = ET.parse(new_file)
                        root2 = dom2.getroot()
                        namespaces = getNamespaces(root2)
                        version = namespaces['xmlns'].split("/")[-1]
                        things = root2.xpath(f'.//EntityResponse:Fragment[not((@schema="http://preservica.com/'
                                             f'LegacyXIP") or (@schema="http://preservica.com/ExtendedXIP/'
                                             f'{version}"))]', namespaces=namespaces)
                        element_counter2 = 0
                        for thing in things:
                            element_counter2 += 1
                            another_new_file = new_file[:-4] + "_metadata-" + str(element_counter2) + ".xml"
                            try:
                                elementals = thing.text
                                list_of_files.append(another_new_file)
                                if another_new_file not in list_of_existing_files:
                                    response = requests.get(elementals, headers=headers)
                                    status = response.status_code
                                    if status == 401:
                                        print(f"{another_new_file} may have failed, logging back in")
                                        logger.write(another_new_file + "\n")
                                        headers = preservation_utilities.login(url, payload)
                                        response = requests.get(elementals, headers=headers)
                                        preservation_utilities.filemaker(another_new_file, response)
                                    else:
                                        preservation_utilities.filemaker(another_new_file, response)
                            except:
                                print(f"exception happened around {new_file} or {another_new_file}")
                        dir_level2 = newDirpath(dirpath)
                        child_file = os.path.join(dirpath, "level" + str(dir_level2), types + "_" +
                                                  uuid + "_children.xml")
                        list_of_files.append(child_file)
                        if child_file not in list_of_existing_files:
                            preservation_utilities.dirMaker(child_file)
                            response = requests.get(elemental + "/children?start=0&max=1000", headers=headers)
                            status = response.status_code
                            if status == 401:
                                print(f"{child_file} may have failed, logging back in")
                                logger.write(child_file + "\n")
                                headers = preservation_utilities.login(url, payload)
                                response = requests.get(elemental + "/children?start=0&max+1000", headers=headers)
                                preservation_utilities.filemaker(child_file, response)
                            else:
                                preservation_utilities.filemaker(child_file, response)
                        dom3 = ET.parse(child_file)
                        root3 = dom3.getroot()
                        namespaces = getNamespaces(root3)
                        version = namespaces['xmlns'].split("/")[-1]
                        things = root3.xpath('.//ChildrenResponse:TotalResults', namespaces=namespaces)
                        for thing in things:
                            hits = int(thing.text)
                            children_start = 1000
                            root_child = elemental + "/children?start="
                            max_child = "&max=1000"
                            if hits > 1000:
                                while children_start <= hits:
                                    child_file = os.path.join(dirpath, "level" + str(dir_level2), types + "_" + uuid +
                                                              "_" + str(children_start) + "children.xml")
                                    response = requests.get(root_child + str(children_start) + max_child,
                                                            headers=headers)
                                    status = response.status_code
                                    if status == 401:
                                        print(f"{child_file} may have failed, logging back in")
                                        logger.write(child_file + "\n")
                                        headers = preservation_utilities.login(url, payload)
                                        response = requests.get(root_child + str(children_start) + max_child,
                                                                headers=headers)
                                        preservation_utilities.filemaker(child_file, response)
                                    else:
                                        preservation_utilities.filemaker(child_file, response)
                                        children_start += 1000
                    except:
                        print(f"exception happened near {filename}")
                elements = root.xpath(".//ChildrenResponse:Child[@type='IO']", namespaces=namespaces)
                status = len(elements)
                counter = 0
                for element in elements:
                    counter += 1
                    window['-Progress-'].update_bar(counter, status)
                    try:
                        elemental = element.text
                        types = element.get('type')
                        uuid = element.get('ref')
                        titleist = element.get('title')
                        titleist = titleist.replace(" ", "_").replace("&", "and").replace(":", "_").replace("/", "_")
                        titleist = titleist.replace('"', '_').replace('?', '_').replace("*", "_")
                        titleist = titleist[:10]
                        new_file = os.path.join(dirpath, types + "_" + titleist + "_" + uuid + ".xml")
                        list_of_files.append(new_file)
                        if new_file not in list_of_existing_files:
                            response = requests.get(elemental, headers=headers)
                            status = response.status_code
                            if status == 401:
                                print(f"{new_file} may have failed, logging back in")
                                logger.write(new_file + "\n")
                                headers = preservation_utilities.login(url, payload)
                                response = requests.get(elemental, headers=headers)
                                preservation_utilities.filemaker(new_file, response)
                            else:
                                preservation_utilities.filemaker(new_file, response)
                        dom2 = ET.parse(new_file)
                        root2 = dom2.getroot()
                        namespaces = getNamespaces(root2)
                        version = namespaces['xmlns'].split("/")[-1]
                        things = root2.xpath('.//EntityResponse:Fragment', namespaces=namespaces)
                        my_list = []
                        for thing in things:
                            dc_type = thing.get('schema')
                            my_list.append(dc_type)
                        print(my_list)
                        if dublin_core not in my_list:
                            print(f"{uuid} missing dcterms, adding them")
                            purl2 = elemental + "/metadata"
                            metadata2 = metadata
                            if len(pair_list) > 0:
                                my_title = element.get("title")
                                for xyz in pair_list:
                                    metadata_file_name = xyz.split("/")[-1][:-9]
                                    if "." in metadata_file_name:
                                        ext_index = metadata_file_name.rfind(".")
                                        metadata_file_name = metadata_file_name[:ext_index]
                                    if my_title == metadata_file_name:
                                        metadata2 = xyz
                            responsible = requests.post(purl2, headers=headers, data=open(metadata2, 'rb'))
                            response = requests.get(elemental, headers=headers)
                            add_counter += 1
                            preservation_utilities.filemaker(new_file, response)
                            logger2.write(elemental + "\n")
                        dom2 = ET.parse(new_file)
                        root2 = dom2.getroot()
                        namespaces = getNamespaces(root2)
                        version = namespaces['xmlns'].split("/")[-1]
                        things = root2.xpath(f'.//EntityResponse:Fragment[not((@schema="http://preservica.com/'
                                             f'LegacyXIP") or (@schema="http://preservica.com/ExtendedXIP/'
                                             f'{version}"))]', namespaces=namespaces)
                        element_counter2 = 0
                        for thing in things:
                            try:
                                elementals = thing.text
                                element_counter2 += 1
                                another_new_file = new_file[:-4] + "_metadata-" + str(element_counter2) + ".xml"
                                list_of_files.append(another_new_file)
                                if another_new_file not in list_of_existing_files:
                                    response = requests.get(elementals, headers=headers)
                                    status = response.status_code
                                    if status == 401:
                                        print(f"{another_new_file} may have failed, logging back in")
                                        logger.write(another_new_file + "\n")
                                        headers = preservation_utilities.login(url, payload)
                                        response = requests.get(elementals, headers=headers)
                                        preservation_utilities.filemaker(another_new_file, response)
                                    else:
                                        preservation_utilities.filemaker(another_new_file, response)
                            except:
                                print(f"exception happened for some weird reason around {new_file} ")
                        if timer <= time.time():
                            print("time to log back in")
                            headers = preservation_utilities.login(url, payload)
                            timer = time.time() + 600
                    except:
                        print(f"exception happened for some weird reason")
    logger.close()
    logger2.close()


SG.theme("DarkGreen5")
layout = [
    [
      SG.Checkbox("harvest data?", key="-HARVEST-", tooltip="Check to harvest data based on a UUID")
    ],
    [
      SG.Checkbox("rerun harvest when completed?", key="-RERUN-",
                  tooltip="check this box to automatically run the data harvest for a second pass")
    ],
    [
      SG.Checkbox("check for errors?", key="-ERROR_CATCHER-", tooltip="check output for bad harvest files")
    ],
    [
      SG.Checkbox("patch harvest as well?", key="-PATCH-",
                  tooltip="patch the harvested data, must be run against an errors csv file")
    ],
    [
        SG.Push(),
        SG.Text("Harvested files location", visible=True, key="-LOCATION_Text-"),
        SG.In("", size=(50, 1), visible=True, key="-LOCATION-",
              tooltip="yes, this includes where to put harvested files. absolute filepath must end in a /"),
        SG.FolderBrowse()
    ],
    [
        SG.Push(),
        SG.Text("Metadata file", visible=True, key="-METADATA_Text-"),
        SG.In("", size=(50, 1), visible=True, key="-METADATA-",
              tooltip="absolute filepath for metadata file to insert if no DCMI metadata is present"),
        SG.FileBrowse()
    ],
    [
        SG.Push(),
        SG.Text("Error file location", visible=True, key="-ERRORS_Text-"),
        SG.In("", size=(50, 1), visible=True, key="-ERRORS-",
              tooltip="specific file must be a csv"),
        SG.FileBrowse()
    ],
    [
        SG.Push(),
        SG.Text("UUID for top-level folder", visible=True, key="-UUID_Text-"),
        SG.Input("", size=(50, 1), visible=True, key='-UUID-')
    ],
    [
      SG.Checkbox("pair with item-level metadata?", key="-PAIR-",
                  tooltip="check to insert existing item-level unique metadata to items")
    ],
    [
        SG.Push(),
        SG.Text("Root metadata files location", visible=True, key="-PAIR_Text-"),
        SG.In("", size=(50, 1), visible=True, key="-PAIR_FILES-",
              tooltip="root folder for pairing metadata, files must end in .metadata"),
        SG.FolderBrowse()
    ],
    [
        SG.Text("Login variables", text_color="orchid1", font=("Calibri", "12", "underline"))
    ],
    [
        SG.Push(),
        SG.Text("Username:", key="-USERNAME_TEXT-"),
        SG.Input("", size=(50, 1), key="-USERNAME-")
    ],
    [
        SG.Push(),
        SG.Text("Password:", key="-PASSWORD_TEXT-"),
        SG.Input("", size=(50, 1), password_char="#", key="-PASSWORD-")
    ],
    [
        SG.Push(),
        SG.Text("Domain Prefix:", key="-PREFIX_TEXT-"),
        SG.Input("", size=(50, 1), key="-PREFIX-")
    ],
    [
        SG.Push(),
        SG.Text("Tenancy abbreviation:", key="-TENANT_TEXT-"),
        SG.Input("", size=(50, 1), key="-TENANT-")
    ],
    [
        SG.Text("Select execute to start processing")
    ],
    [
        SG.Push(),
        SG.Button("Execute", tooltip="This will start the program running."),
        SG.Push()
    ],
    [
        SG.Text("Select Close to close the window.")
    ],
    [
        SG.Button("Close",
                  tooltip="Close this window. Other processes you started must be finished before this button "
                          "will do anything.",
                  bind_return_key=True)],
    [
        SG.ProgressBar(1, orientation="h", size=(50, 20), bar_color="dark green", key="-Progress-", border_width=5,
                       relief="RELIEF_SUNKEN")
    ],
    [
        SG.Text("", key="-STATUS-")
    ],
    [
        SG.Multiline(default_text="Click execute to show progress\n------------------------------", size=(70, 5),
                     auto_refresh=True, reroute_stdout=False, key="-OUTPUT-", autoscroll=True, border_width=5),
    ],
]


window = SG.Window(
    "Opex Compiler Graphical interface",
    layout,
    icon=my_icon,
    button_color="dark green",
)

event, values = window.read()
while True:
    event, values = window.read()
    username = values['-USERNAME-']
    password = values['-PASSWORD-']
    prefix = values['-PREFIX-']
    tenant = values['-TENANT-']
    metadata = values['-METADATA-']
    metadata_files = values['-PAIR_FILES-']
    location = values['-LOCATION-']
    error_log = values['-ERRORS-']
    uuid = values['-UUID-']
    valuables = {'username': username,
                 'password': password,
                 'tenant': tenant,
                 'prefix': prefix,
                 'location': location,
                 'metadata_file': metadata,
                 'uuid': uuid}
    url = f"https://{prefix}.preservica.com/api/accesstoken/login"
    payload = {'username': username, 'password': password, 'tenant': tenant}
    pair_list = []
    if event == "Execute":
        if values['-PAIR-'] is True:
            window['-OUTPUT-'].update("\nGathering list of metadata files for pairing", append=True)
            if metadata_files != "":
                for dirpath, dirnames, filenames in os.walk(metadata_files):
                    for filename in filenames:
                        if filename.endswith(".metadata"):
                            filename = os.path.join(dirpath, filename)
                            pair_list.append(filename)
                window['-OUTPUT-'].update("\nlist of metadata files generated", append=True)
            else:
                window['-OUTPUT-'].update("\nyou need to add the metadata files folder, exiting", append=True)
                print("you need to add the metadata files folder, exiting")
                sys.exit()
        if values['-HARVEST-'] is True:
            window['-OUTPUT-'].update("\ncheckbox works", append=True)
            window['-OUTPUT-'].update("\nstarting original harvest of files", append=True)
            harvest(valuables, pair_list=pair_list)
            window['-OUTPUT-'].update("\noriginal harvest of files finished, moving on to any other selected option",
                                      append=True)
        if values['-RERUN-'] is True:
            window['-OUTPUT-'].update("\nstarting second pass at harvesting files to catch missing items", append=True)
            harvest(valuables, pair_list=pair_list)
            window['-OUTPUT-'].update("\nsecond pass completed", append=True)
        if values['-ERROR_CATCHER-'] is True:
            window['-OUTPUT-'].update("\n starting error catching routine", append=True)
            log = open(error_log, "a")
            crawler = location
            dir = ""
            for dirpath, dirnames, filenames in os.walk(crawler):
                counter = 0
                status = len(filenames)
                for filename in filenames:
                    counter += 1
                    window['-Progress-'].update_bar(counter, status)
                    if filename.endswith(".xml"):
                        filename = os.path.join(dirpath, filename)
                        if dir != dirpath:
                            current = time.asctime()
                            print(f"checking {dirpath} starting at {current}")
                            dir = dirpath
                        with open(filename, "r") as f:
                            filedata = f.read()
                            if "xip" not in filedata:
                                print(f"error in {filename}")
                                if "IO_" in filename:
                                    my_type = "IO"
                                    core = "information-objects/"
                                    finder = filename.find("IO_")
                                    finder2 = finder - 1
                                    directory = filename[:finder2]
                                    xip_file = filename[finder:]
                                if "SO_" in filename:
                                    my_type = "SO"
                                    core = "structural-objects/"
                                    finder = filename.find("SO_")
                                    finder2 = finder - 1
                                    directory = filename[:finder2]
                                    xip_file = filename[finder:]
                                if "metadata" in filename:
                                    uuid = filename[-51:-15]
                                else:
                                    uuid = filename[-40:-4]
                                log.write(f"https://{prefix}.preservica.com/api/entity/{core}{uuid},{directory},"
                                          f"{xip_file},{type}\n")
            print("all done with error checking")
            print("don't forget to modify errors.csv to be in the format needed for patch harvesting")
            log.close()
            window['-OUTPUT-'].update("\nerror catcher routine complete", append=True)
        if values['-PATCH-'] is True:
            print("patch option was selected")
            window['-OUTPUT-'].update("\nRunning patch harvest for anything missing", append=True)
            headers = preservation_utilities.login(url, payload)
            timer = time.time() + 600
            logger = open(f"{location}/log_potential_fails_patch.txt", "a")
            base_url = f"https://{prefix}.preservica.com/api/entity/"
            file = open(error_log, "r", encoding='utf-8')
            csv_in = csv.reader(file)
            for row in csv_in:
                try:
                    uuid_url = row[0]
                    directory = row[1]
                    xip_file = row[2]
                    if "_metadata" in xip_file:
                        temp = "_" + xip_file.split("_")[-1]
                        xip_file = xip_file.replace(temp, ".xml")
                    new_file = f"{directory}/{xip_file}"
                    print(new_file)
                    preservation_utilities.dirMaker(new_file)
                    response = requests.get(uuid_url, headers=headers)
                    status = response.status_code
                    if status == 401:
                        print(f"{new_file} may have failed, logging back in")
                        logger.write(new_file + "\n")
                except:
                    continue
            window['-OUTPUT-'].update("\npatch harvest completed", append=True)
    if event == "Close" or event == SG.WIN_CLOSED:
        break
window.close()
