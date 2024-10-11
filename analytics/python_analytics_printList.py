# program will take user input to iterate over many files,
# locate a specific term and apply a transform as a result
# all inapplicable files are left alone
# to know what files were affected look at the last modified date

# may in the future need to improve iteration over directories
import os, sys, csv
import lxml.etree as ET
from openpyxl import Workbook
import time
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

def getNamespaces(root):
    namespaces = root.nsmap
    namespaces['xmlns'] = namespaces[None]
    namespaces.pop(None, None)
    namespaces['dcterms'] = "http://dublincore.org/documents/dcmi-terms/"
    namespaces['tslac'] = 'https://www.tsl.texas.gov/'
    namespaces['MetadataResponse'] = namespaces['xmlns']
    namespaces['EntityResponse'] = namespaces['xmlns']
    namespaces['ChildrenResponse'] = namespaces['xmlns']
    return namespaces

#remind user what they need to do before proceeding

SG.theme("LightGreen5")
layout = [
	[
		SG.Push(),
		SG.Text("Path to harvested files", visible=True, key="-PATH_TEXT-"),
		SG.In(default_text="", size=(50, 1), visible=True, key="-PATH-"),
		SG.FolderBrowse()
	],
	[
		SG.Push(),
		SG.Text("excel filename", visible=True, key="-EXCEL_TEXT-"),
		SG.In(default_text="", size=(50, 1), visible=True, key="-EXCEL-", tooltip="will save to root folder of the harvested files")
	],
	[
		SG.Text(text="Sheet name, choose Sheet1 for analytics stuff")
	],
	[
		SG.Radio(text="Sheet1", group_id="sheet_name", key="-excel_sheet1-")
	],
	[
		SG.Radio(text="Other", group_id="sheet_name", key="-excel_other-"),
		SG.In(default_text="", size=(25, 1), visible=True, key="-excel_other_text-")
	],
	[
		SG.Push(),
		SG.Text(text="Collection name", visible=True, key="-COLLECTION_TEXT-"),
		SG.In(default_text="", size=(50, 1), visible=True, key="-COLLECTION-")
	],
	[
		SG.Text("Is this LSTA-funded?"),
		SG.Radio(text="Yes", group_id="LSTA", key="-LSTA_YES-"),
		SG.Radio(text="No", group_id="LSTA", key="-LSTA_NO-", default=True)
	],
	[
		SG.Text("Select execute to start, select close to close window")
	],
	[
		SG.Button(button_text="Execute", bind_return_key=True),
		SG.Push(),
		SG.Button(button_text="Close")
	],
	[
		SG.Push(),
		SG.Text("Overall Progress"),
		SG.Push()
	],
	[
		SG.Push(),
		SG.ProgressBar(max_value=1, orientation="h", size=(50, 2), key="-Overall_Progress-", border_width=5, relief="RELIEF_SUNKEN"),
		SG.Push()
	],
	[
		SG.Push(),
		SG.Text("Folder progress"),
		SG.Push()
	],
	[
		SG.Push(),
		SG.ProgressBar(max_value=1, orientation="h", size=(50, 2), key="-Folder_Progress-", border_width=5, relief="RELIEF_SUNKEN"),
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
    "Collection Spreadsheet Maker",
    layout,
    icon=my_icon,
    button_color="light green",
)

event, values = window.read()
while True:
	event, values = window.read()
	seriousFilepath = values["-PATH-"]
	workbookfilename = values["-EXCEL-"]
	worksheetName = "Sheet1"
	if values["-excel_other-"] is True:
		worksheetName = values["-excel_other_text-"]
	collectionName = values['-COLLECTION-']
	type1 = "Born-digital"
	if values['-LSTA_YES-'] is True:
		type1 = "LSTA"
	if event == "Execute":
		workbookfilename = f"{seriousFilepath}/{workbookfilename}"
		wb = Workbook(workbookfilename)
		ws = wb.create_sheet(worksheetName)
		window['-OUTPUT-'].update("\nGathering progress bar info", append=True)
		count = 0
		dirname_list = set()
		for dirpath, dirnames, filenames in os.walk(seriousFilepath):
			for filename in filenames:
				if filename.endswith("xml") and "metadata" not in filename and "_children" not in filename:
					count += 1
					dirname_list.add(dirpath)
		window['-OUTPUT-'].update("\nProgress bar info gathered, starting the compilation", append=True)
		ws.append(['UUIDs', 'filename'])
		ws.append([collectionName, type1])
		dir = ""
		current = 0
		dirname_list = list(dirname_list)
		dirname_list.sort()
		for dirname in dirname_list:
			window["-OUTPUT-"].update(f"\nstarting {dirname} at {time.asctime()}", append=True)
			listing = os.listdir(dirname)
			files_list = []
			for item in listing:
				if item.endswith(".xml") and "metadata" not in item and "_children" not in item:
					item = os.path.join(dirname, item)
					if os.path.isfile(item):
						files_list.append(item)
			folder_length = len(files_list)
			folder_count = 0
			for item in files_list:
				with open(item, "r") as f:
					filedata = f.read()
					if "<xip:Title>" in filedata:
						dom = ET.parse(item)
						root = dom.getroot()
						namespaces = getNamespaces(root)
						try:
							tree = ET.parse(item)
							root = tree.getroot()
							title = root.find(".//xip:Title", namespaces=namespaces).text
							uuid = root.find(".//xip:Ref", namespaces=namespaces).text
							ws.append([uuid, title])
							folder_count += 1
							current += 1
							window['-Overall_Progress-'].update_bar(current, count)
							window['-Folder_Progress-'].update_bar(folder_count, folder_length)
						except:
							window['-OUTPUT-'].update(f"\nsomething is wrong with {item.split('/')[-1]}", append=True)
		wb.save(workbookfilename)
		wb.close()
		window['-OUTPUT-'].update("\nAll done", append=True)
	if event == "Close" or event == SG.WIN_CLOSED:
		break
window.close()
# to document the tag being searched