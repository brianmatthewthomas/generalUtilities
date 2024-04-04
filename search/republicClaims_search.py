import os
import lxml.etree as ET
import csv
import pandas as PD

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

def optionGenerator(something=set):
    something = list(something)
    print(something)
    something.sort()
    textual = ""
    for item in something:
        if item == "Unkn":
            item = "Unknown"
        stringy = f'\t<option value="{item}">{item}</option>\n'
        textual = textual + stringy
    return textual

def row_generator(row_data):
    claimant = row_data['claimant']
    names = row_data['names']
    claim_type = row_data['type']
    number = row_data['number']
    reel = row_data['reel']
    link = row_data['link']
    name_aggregate = ""
    names = list(names)
    names.sort()
    for name in names:
        name_aggregate = f"{name_aggregate}{name}; "
    while name_aggregate.endswith("; "):
        name_aggregate = name_aggregate[:-2]
    row = f'''<tr>
        <td>{claimant}</td>
        <td>{name_aggregate}</td>
        <td>{claim_type}</td>
        <td class="drop3">{number}</td>
        <td>{reel}</td>
        <td><a href="https://tsl.access.preservica.com/uncategorized/IO_{link}/" target="_blank" title="Link to {claim_type} number {number} for {claimant}">Link to claim</a></td>
    </tr>'''
    return row

empty_dict = {'claimant':'','names':"",'type':"",'number':"",'reel':"",'link':""}

metadata = "/media/sf_D_DRIVE/harvest/_claims" #input("directory to crawl for data: ")
myCSV = f"{metadata}/temp.csv"
with (open(myCSV, "w") as csvfile):
    myWriter = csv.writer(csvfile)
    myWriter.writerow(["Name of claimant", "Additional names", "Claim type", "Claim number", "Link to claim"])
    data = []
    type_set = set()
    for dirpath, dirnames, filenames in os.walk(metadata):
        for filename in filenames:
            if "metadata" in filename:
                if filename.startswith("IO"):
                    row_dict = empty_dict
                    row_dict['names'] = set()
                    filename_placeholder = filename
                    filename = os.path.join(dirpath, filename)
                    with open(filename, "r") as r:
                        filedata = r.read()
                        if "dcterms" in filedata:
                            dom = ET.parse(filename)
                            root = dom.getroot()
                            nsmap = getNamespaces(root)
                            row_dict['link'] = dom.find(".//xip:Entity", namespaces=nsmap).text
                            title = dom.find(".//dcterms:title", namespaces=nsmap).text
                            description = dom.find(".//dcterms:description.abstract", namespaces=nsmap).text
                            row_dict['claimant'] = title.split(": ")[-1]
                            names = root.xpath(".//tslac:keyword", namespaces=nsmap)
                            for name in names:
                                row_dict['names'].add(name.text)
                            myTypes = root.xpath(".//dcterms:type", namespaces=nsmap)
                            for myType in myTypes:
                                if myType.text != "Text":
                                    row_dict['type'] = myType.text
                                    type_set.add(row_dict['type'])
                            type_list = row_dict['type'].split(" ")
                            type_list.append("number")
                            type_list.append("Republic")
                            myNumber = title.split(": ")[0]
                            for item in type_list:
                                myNumber = myNumber.replace(item, "")
                            while myNumber.startswith(" "):
                                myNumber = myNumber[1:]
                            myNumber = myNumber.replace("Uned", "Unnumbered")
                            if myNumber == 'for':
                                myNumber = 'Unnumbered'
                            row_dict['number'] = myNumber
                            row_dict['reel'] = description.split(" ")[-1][:-1]
                            #myText = row_generator(row_dict)
                            #data.append(myText)
                            templist = list(row_dict['names'])
                            templist.sort()
                            temp_text = ""
                            for item in templist:
                                temp_text = f"{temp_text}{item}; "
                            while temp_text.endswith("; "):
                                temp_text = temp_text[:-2]
                            myLink = f'<a href="https://tsl.access.preservica.com/uncategorized/IO_{row_dict["link"]}/" target="_blank" title="Link to {row_dict["type"]} for {row_dict["claimant"]}">View claim</a>'
                            myWriter = csv.writer(csvfile)
                            myWriter.writerow([row_dict['claimant'], temp_text, row_dict['type'], row_dict['number'], myLink])
                            print(f"{filename} processed")
csvfile.close()

filter(None, data)
data.sort()
table_data = ""
for item in data:
    table_data = table_data + item + "\n"
df = PD.read_csv(myCSV, dtype=object)
df.sort_values(by=['Name of claimant'])
type_set = list(type_set)
type_set.sort()
counter = 0
math = len(df)/3
math = int(str(math)[:5])
var1 = 0
var2 = math

for my_type in type_set:
    df2 = df.loc[df['Claim type'] == my_type]
    table_data = df2.to_html(index=False)
    dom = ET.fromstring(table_data)
    root = dom.xpath(".//tr")
    for item in root:
        others = item.xpath("./td")
        if others is not None:
            if len(others) > 0:
                other = others[-1]
                other.attrib['class'] = "tommy"
                other1 = others[-2]
                other1.attrib['class'] = "drop5"
                other2 = others[-3]
                other2.attrib['class'] = 'drop4'
    writable = ET.tostring(dom)
    table_data = writable
    form_text = f'''<form id="form" onchange="master_filter()" onkeyup="master_filter()">

            <div class="tdaSearch_thing1">
                <h3>
                  <label for="claimant">Claimant name</label>
                    <strong id="claimant_note" style="color:purple; display:none;"> *Active filter</strong>
                    <div>
                        <input id="claimant" placeholder="Enter a claimant name starting with last name" class="inputs" type="text"/>
                    </div>
                </h3>
            </div>  
            <div class="tdaSearch_thing1">
                <h3>
                    <label for="more_names" >Additional names </label>
                    <strong id="more_names_note" style="color:purple; display:none;"> *Active filter</strong>
                                                                                                       <div>
                        <input id="more_names" placeholder="Enter additional names to filter by" type="text" class="inputs"/>
                    </div>
                </h3>
            </div>
            <div class="tdaSearch_thing1">
                <h3>
                    <label for="type_drop">Claim type  </label>
                    <strong id="type_note" style="color:purple; display:none;"> *Active filter</strong>
                    <div>
                        <select id="type_drop" class="inputs">
                            <option value="">Select claim type</option>
                            <option>Audited claim</option>
                            <option>Pension claim</option>
                            <option>Public Debt claim</option>
                            <option>Unpaid claim</option>
                        </select>
                    </div>
                </h3>
            </div>
            <div class="tdaSearch_thing1">
                <h3>
                    <label for="claim_number" >Claim number </label>
                    <strong id="claim_number_note" style="color:purple; display:none;"> *Active filter</strong>
                    <div>
                        <input id="claim_number" placeholder="Enter claim number" type="text" class="inputs"/>
                    </div>
                </h3>
            </div>

            <div id="NullResultsMessage" style="display:none;border:5px outset #a91d2f;background-color:lightgrey;text-align:center;border-radius:10px;">
                <p>No matching results. Update your selections from the options above or click on reset to start over.</p>
            </div>
            <br/>
            <div class="tdaSearch_thing5">
                <input onClick="location.reload()" style="height:2.75em;" type="reset" value="Reset options"/>
            </div>
        </form>
    '''
    preamble = '''<html>
<head>
<style>
	.tdaSearch_search_container{display:table; border: 1px outset; border-radius: 10px}
.tdaSearch_search_warning{border-bottom: 2px solid rgb(147,35,29); padding: 1%; display:block;}
.tdaSearch_search_title:before{left:0;margin-right:15px;width:75px;content:"";position:absolute;height:20px;background:#a91e2f;top:10px;box-sizing:border-box;} 
.tdaSearch_search_title{display:inline-block;position:relative;padding-left:100px;padding-right:15px; font-size:1.8em;font-weight:500;line-height:1.2;box-sizing:border-box} 
.tdaSearch_search_title:after{box-sizing:border-box;left:100%;margin-left:15px;width:225px;content:"";position:absolute;height:20px;background:#a91e2f;top:10px}
.tdaSearch_search_box{display:flex;padding-left:10px;padding-right:10px;}
.tdaSearch_search_form_left{display:table-cell; float:left; width:50%;text-align:left;}
.tdaSearch_search_form_right{display:table-cell; float:right; width:45%;align-self:center;padding-left:10px;text-align:center;margin-top:10%}
div#tdaSearch_search_form_left_senate{width:65%}
div#tdaSearch_search_form_right_senate{width:35%}
select{width:100%;word-break:break-word;overflow:hidden;text-overflow:ellipsis;word-wrap:break-word;overflow-wrap:break-word;overflow-x:hidden;}
option{word-break:break-word;overflow:hidden;text-overflow:ellipsis;word-wrap:break-word;overflow-wrap:break-word;overflow-x:hidden;}
.tdaSearch_thing1{width:100%;overflow:hidden;}
.tdaSearch_thing5{text-align:center;padding-bottom:15px;}
.tdaSearch_thing5>input{border-radius:5px;}
.tdaSearch_link2{display:none}
.tdaSearch_graphic{box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);}
#senate_graphic{box-shadow:none; align:center;}
td{border-bottom: 1px solid darkgray; border-right: 1px solid darkgray; padding: 3px; min-width:5em;}
tr:hover{background-color: lightgray;}
.form-button{font-weight:bold; font-size:1.25em; border:2px outset darkgrey; border-radius:5px; background-color:lightgrey; font-weight:bold; color:#005297; font-family:Georgia}
.form-button1{padding:1px; font-size:1.25em; font-weight:bold; border:2px outset darkgrey; border-radius:5px; background-color:lightgrey; text-decoration:none;color:#005297;font-family:Georgia}
.form-button:hover, .form-button1:hover {border:2px inset darkgrey;}
.image{padding-left:20px;vertical-align:center;max-width=400}
.form{max-width:710px;}
.inputs{width:700px;}
table#senate, table#table{border: 3px outset black; padding: 0px; horizontal-align: center; border-radius:10px;}
.tdaSearch_search_form_top>form>.tdaSearch_thing1, .tdaSearch_search_form_bottom>form>.tdaSearch_thing1{
	max-width: 700px;
	padding-left: 10px;
	padding-right: 10px;
}
.tdaSearch_search_form_bottom{
	border-top: 3px outset #a91d2f;
	margin-top: 5px;
	display: block;
}
.tdaSearch_search_form_top{
	display:block;width:100%;
}
label{display: inline-block; padding-bottom: 5px;}
/* responsiveness */
@media(max-width:1230px){.image{max-width:200px}}
@media(max-width: 1150px){
	.tdaSearch_search_title:before{width:0px}
	.tdaSearch_search_title{text-align:center;padding-left:0px;display:block}
	.tdaSearch_search_title:after{width:0px}
}
@media(max-width:1130px){.image{display:none}.form{margin:auto}.drop4{display:none}}
@media(max-width:980px){
	.inputs{width:100%}
	.drop1{display:none}
}
@media (max-width:840px){
	.form-button1, .form-button{font-size:1em;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;}.drop5{display:none;}
}
@media(max-width:760px){
	.tdaSearch_search_container{display:block;border:0px;border-radius:0px;background-color:transparent;}
	.tdaSearch_search_form_left{display:inline-table;width:100%;border-bottom:3px solid #a91e2f;}
	.tdaSearch_search_form_right{display:inline-table;width:100%;text-align:center;float:none;padding-top:5px;}
	div#tdaSearch_search_form_left_senate{width:100%}
	div#tdaSearch_search_form_right_senate{display:none}
	img#court_graphic{display:none}
	.tdaSearch_search_box{display:block;}
	.tdaSearch_link2{display:block;}
	.tdaSearch_link1{display:none;}
	input#recording_num, input#search_all{border:1px solid lightgrey; padding-left:5px;}
	.inputs{width:100%;}
	.tdaSearch_search_form_top>form>.tdaSearch_thing1, .tdaSearch_search_form_bottom>form>.tdaSearch_thing1{
	max-width: 100%;
	padding-left: 10px;
	padding-right: 10px;
	}
	.form{max-width:100%;}
	select{max-width:100%}
}
@media(max-width:650px){
	.drop2{display:none}
}
@media (max-width:555px){
	.drop3{display:none;}
}
/* tooltips */
.tooltip_image{
	max-height:1em;
	max-width:1em;
}
.drop0{
	display: none;
}
.tommy{
    text-align: center;
    padding: 10px;
}
.tommy > a{
    border-radius: 5px;
    border: 2px outset darkgray;
    font-weight: bold;
    background-color: darkgray;
    padding: 5px;
}
.tommy > a:hover{
    border: 2px inset darkgray;
}
</style>
<style>
			/* lifted directly from answer 2 on https://stackoverflow.com/questions/7853130/how-to-change-the-style-of-alert-box */
		#modalContainer {
			background-color:rgba(0, 0, 0, 0.3);
			position:absolute;
			/* width:100%;
			height:100%; */
			top:0px;
			left:0px;
			z-index:10000;
			background-image:url(tp.png); /* required by MSIE to prevent actions on lower z-index elements */
		}

		#alertBox {
			position:relative;
			width:300px;
			/* min-height:100px;*/
			margin-top:50px;
			border:1px solid #666;
			background-color:#fff;
			background-repeat:no-repeat;
			background-position:20px 30px;
		}

		#modalContainer > #alertBox {
			position:fixed;
		}

		#alertBox h1 {
			margin:0;
			font:bold 1em verdana,arial;
			background-color:#a91d2f;
			color:#FFF;
			border-bottom:1px solid #000;
			padding:2px 0 2px 5px;
		}

		#alertBox p {
			font:0.7em verdana,arial;
			/* height:150px;*/
			padding-left:5px;
			margin-left:auto;
			margin-right:auto;
		}

		#alertBox #closeBtn {
			display:block;
			position:relative;
			margin:5px auto;
			padding:7px;
			border:0 none;
			width:70px;
			font:0.7em verdana,arial;
			text-transform:uppercase;
			text-align:center;
			color:#FFF;
			background-color:#357EBD;
			border-radius: 3px;
			text-decoration:none;
		}

		/* unrelated styles */

		#mContainer {
			position:relative;
			width:600px;
			margin:auto;
			padding:5px;
			border-top:2px solid #000;
			border-bottom:2px solid #000;
			font:0.7em verdana,arial;
		}

		h1,h2 {
			margin:0;
			padding:4px;
			font:bold 1.5em verdana;
			#border-bottom:1px solid #000;
		}

		code {
			font-size:1.2em;
			color:#069;
		}

		#credits {
			position:relative;
			margin:25px auto 0px auto;
			width:350px; 
			font:0.7em verdana;
			border-top:1px solid #000;
			border-bottom:1px solid #000;
			height:150px;
			padding-top:4px;
		}

		#credits img {
			float:left;
			margin:5px 10px 5px 0px;
			border:1px solid #000000;
			width:80px;
			height:100px;
		}

		.important {
			background-color:#F5FCC8;
			padding:2px;
		}

		code span {
			color:green;
		}	
	</style>
	</head>
<div style="width:100%">
<div width="100%" class="container">
    <h2 class="tdaSearch_search_title" style="text-align:center; color: #a91e2f;" id="top">
        <strong>Republic Claims custom search</strong>
    </h2>
</div>
<p class="tdaSearch_link2" style="text-align:center">
    <a href="https://tsl.access.preservica.com/uncategorized/SO_fd1da040-38cc-4ca6-8299-237ddc19d983/">Browse the Republic claims</a>
</p>
<div align="center" class="tdaSearch_search_container" style="width:100%">
    <div align="left" class="tdaSearch_search_warning">
        <p>Use the options below to filter claims list in the <a href="#scotx">results table</a>
        </p>
    </div>
    <div class="tdaSearch_search_form_left" style="padding-left: 10px;">
'''
    table_text = f'''{table_data}'''
    script = '''<script>
	function master_filter() {
		var table, tr, i, td1, td2, td3, td4
		var claimants = claimant.value;
		var filter_claimant = claimants.toUpperCase();
		var others = more_names.value;
		var filter_others = others.toUpperCase();
		var typology = type_drop.options[type_drop.selectedIndex].value;
		var claims = claim_number.value;
		var filter_claims = claims.toUpperCase();
		table = document.getElementById("scotx");
		tr = table.getElementsByTagName("tr");
		for (i = 1; i < tr.length; i++) {
			td1 = tr[i].getElementsByTagName("td")[0];
			td2 = tr[i].getElementsByTagName("td")[1];
			td3 = tr[i].getElementsByTagName("td")[2];
			td4 = tr[i].getElementsByTagName("td")[3];
			if (td1, td2, td3, td4) {
				if ((td1.innerHTML.toUpperCase().indexOf(filter_claimant) > -1) && (td2.innerHTML.toUpperCase().indexOf(filter_others) > -1) && (td3.innerHTML.indexOf(typology) > -1) && (td4.innerHTML.toUpperCase().indexOf(filter_claims) > -1)) {
					tr[i].style.display = "";
				} else {
					tr[i].style.display = "none";
				}
			}
		}
	}
</script>'''
    html = f'''{preamble}{form_text}
    </div>
    <div class="tdaSearch_search_form_right">
        <img title="Index page" caption="Sample index volume page" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2023/05/judiciary_criminalAppeals_indexes.jpg" class="tdaSearch_graphic" id="court_graphic">
        <p class="tdaSearch_link1" style="text-align:center">
            <a href="https://tsl.access.preservica.com/uncategorized/SO_fd1da040-38cc-4ca6-8299-237ddc19d983/" alt="Browse the Republic caims">Browse the Republic claims</a>
        </p>
    </div>
</div>
    {table_data}
    {script}
</div>
</html>
'''
    # write the html file
    output = f"{metadata}/output{str(counter)}.html"
    with open(output, "w") as w:
        w.write(html)
    w.close()
    # adjust the html output to get the overall desired results
    with (open(output, "r") as r):
        filedata = r.read()
        filedata = filedata.replace('<table border="1" class="dataframe">', '<table style="border: 3px solid black;padding: 0px" id="scotx">')
        filedata = filedata.replace('<tr style="text-align: right;">', '<tr style="background-color:lightgray;border-bottom:3px solid black;padding: 0px" class="silly">')
        filedata = filedata.replace('<th>Additional names</th>', '<th style="width:30%;max-width:500px;">Additional names</th>')
        filedata = filedata.replace('&lt;', '<').replace('&gt;', '>').replace("NaN", 'n/a')
        filedata = filedata.replace("\\n", "\n").replace("b'<table", "<table").replace("</table>'", "</table>")
        while "  " in filedata:
            filedata = filedata.replace("  ", " ")
        with open(output, "w") as w:
            w.write(filedata)
        w.close()
    counter += 1
    var1 = var2
    var2 = var2 + math