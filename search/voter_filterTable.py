import os
import pandas as PD
import lxml.etree as ET


# note: this assumes that the source metadata is using data harvested using the preservica entity api
# note: metadata in dcterms using _metadata-1 as the filename, record data without
# will gather the name of the link from metadata     and name of the file from record data and merge with the data
# from spreadsheet to spit out a html file. written to be self-contained

def row_converter(row=tuple, listy=list, verbose=True):
    # convert pandas row to a dictionary
    # requires a list of columns and a row as a tuple
    count = 1
    pictionary = {}
    pictionary['Index'] = row[0]
    for item in listy:
        pictionary[item] = str(row[count])
        count += 1
        if pictionary[item] == "nan":
            pictionary[item] = ""
    if verbose is True:
        print(pictionary)
    return pictionary


def month_converter(month_name):
    if month_name == "Jul":
        return "07"
    if month_name == "Aug":
        return "08"
    if month_name == "Sep":
        return "09"
    if month_name == "Jan":
        return "01"
    if month_name == "Nov":
        return "11"
    if month_name == "May":
        return "05"
    if month_name == "Oct":
        return "10"
    if month_name == "Jun":
        return "06"
    if month_name == "Feb":
        return "02"
    if month_name == "Dec":
        return "12"
    else:
        return "XX"


def rolio(roll):
    if roll == "1":
        return "3560"
    if roll == "2":
        return "3561"
    if roll == "3":
        return "3562"
    if roll == "4":
        return "3563"
    if roll == "5":
        return "3564"
    if roll == "6":
        return "3565"
    if roll == "7":
        return "3566"
    if roll == "8":
        return "3567"
    if roll == "9":
        return "3568"
    if roll == "10":
        return "3569"
    if roll == "11":
        return "3570"
    if roll == "12":
        return "3571"
    else:
        return "Unspecified"


def prefix_fixer(item):
    if item == "Mrs":
        item += "."
    if item == "Dr":
        item += "."
    if item == "Rev":
        item += "."
    if item == "Sgt":
        item += "."
    if item == "Mr":
        item += "."
    if item == "Gen":
        item += "."
    else:
        item = item
    return (item)


def initial_fixer(valuable):
    list1 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z"]
    list2 = ["A ", "B ", "C ", "D ", "E ", "F, ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O ", "P ", "Q ",
             "R ",
             "S ", "T ", "U ", "V ", "W ", "X ", "Y ", "Z "]
    list3 = [" A", " B", " C", " D", " E", " F", " G", " H", " I", " J", " K", " L", " M", " N", " O", " P", " Q", " R",
             " S", " T", " U", " V", " W", " X", " Y", " Z"]
    list4 = [". A.", ". B.", ". C.", ". D.", ". E.", ". F.", ". G.", ". H.", ". I.", ". J.", ". K.", ". L.", ". M.",
             ". N.",
             ". O.", ". P.", ". Q.", ". R.", ". S.", ". T.", ". U.", ". V.", ". W.", ". X.", ". Y.", ". Z."]
    list5 = [" A ", " B ", " C ", " D ", " E ", " F ", " G ", " H ", " I ", " J ", " K ", " L ", " M ", " N ", " O ",
             " P ", " Q ",
             " R ", " S ", " T ", " U ", " V ", " W ", " X ", " Y ", " Z "]
    for item in list1:
        if item == valuable:
            valuable = valuable + "."
    for item in list2:
        if valuable.startswith(item):
            item2 = item.replace(" ", ". ")
            valuable = valuable.replace(item, item2)
    for item in list3:
        if valuable.endswith(item):
            valuable = valuable + "."
    for item in list4:
        if valuable.endswith(item):
            item2 = item.replace(" ", "")
            valuable = valuable.replace(item, item2)
    for item in list5:
        if item in valuable:
            item2 = item.replace(" ", ".")
            valuable = valuable.replace(item, item2)
            valuable = valuable.replace("..", ".")
    return (valuable)


def name_compiler(nameDict):
    # concatenate a dictionary of elements into a name, returns compiled name
    # required elements are prefix, surname, givenName, suffix

    # generate missing keys
    if not 'surname' in nameDict:
        nameDict['surname'] = ""
    if nameDict['surname'] is None:
        nameDict['surname'] = ""
    if not 'prefix' in nameDict:
        nameDict['prefix'] = ""
    if nameDict['prefix'] is None:
        nameDict['prefix'] = ""
    if not 'givenName' in nameDict:
        nameDict['givenName'] = ""
    if nameDict['givenName'] is None:
        nameDict['givenName'] = ""
    if not 'suffix' in nameDict:
        nameDict['suffix'] = ""
    if nameDict['suffix'] is None:
        nameDict['suffix'] = ""
    # construct name
    print(nameDict['surname'], nameDict['prefix'], nameDict['givenName'], nameDict['suffix'])
    valuable = nameDict['surname'] + ", "
    valuable += nameDict['prefix'] + " "
    valuable += nameDict['givenName'] + ", "
    valuable += nameDict['suffix']
    valuable = valuable.replace("  ", " ")
    valuable = valuable.replace(", , ", ", ")
    if valuable.startswith(", "):
        valuable = valuable[2:]
    switch = 0
    while switch == 0:
        if valuable.endswith(",") or valuable.endswith(" "):
            valuable = valuable[:-1]
        else:
            switch = 1
    return valuable


def name_compiler2(nameDict):
    # concatenate a dictionary of elements into a name, returns compiled name
    # required elements are prefix, surname, givenName, suffix

    # generate missing keys
    if not 'surname' in nameDict:
        nameDict['surname'] = ""
    if nameDict['surname'] is None:
        nameDict['surname'] = ""
    if not 'prefix' in nameDict:
        nameDict['prefix'] = ""
    if nameDict['prefix'] is None:
        nameDict['prefix'] = ""
    if not 'givenName' in nameDict:
        nameDict['givenName'] = ""
    if nameDict['givenName'] is None:
        nameDict['givenName'] = ""
    if not 'suffix' in nameDict:
        nameDict['suffix'] = ""
    if nameDict['suffix'] is None:
        nameDict['suffix'] = ""
    # construct name
    valuable = nameDict['prefix'] + " " + nameDict['givenName'] + " " + nameDict['surname'] + ", " + nameDict['suffix']
    if valuable.endswith(", "):
        valuable = valuable[:-2]
    while valuable.startswith(" "):
        valuable = valuable[1:]
    while "  " in valuable:
        valuable = valuable.replace("  ", " ")
    return valuable


page_head = '''<html>
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
<div style="width:100%">
<div width="100%" class="container">
      <h2 class="tdaSearch_search_title" style="text-align:center; color: #a91e2f;" id="top">
        <strong>Voter Registration list</strong>
      </h2>
    </div>
<p class="tdaSearch_link2" style="text-align:center">
      <a href="https://tsl.access.preservica.com/uncategorized/SO_858938f7-c553-43c5-bda8-58fb3cd6ad5d/" alt="Browse the registration lists">Browse the registration lists</a>
    </p>
<div align="center" class="tdaSearch_search_container">
      <div align="left" class="tdaSearch_search_warning">
        <p>Use the options below to filter cases listed in the <a href="#table">results table</a>. Search tips:
		<img class="tooltip_image" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2020/06/200px-Icon-round-Question_mark.svg_.png" max-width="5px" style="cursor:help" title="Click for search tips" id="tooltip_case_number">
              </p><div class="tooltip-test" id="tooltip_case_number_1" style="display:none;">
                <div class="modal-content">
                    <span class="closeify" id="closeify_tooltip_case_number">x</span>
					<h2 style="color:#a91d2f; text-align:center">Search tips</h2>
					<p>The following additional information is intended to assist you in using this tool.</p>
					<ul>
					<li>This table is derived from transcriptions provided by Ancestry.com and has not been checked for accuracy.</li>
					<li>Due to the extensive number is registered voters, the information has been broken into filter tables by the microfilm reel they were scanned off of. There are 12 microfilm reels. Reels were filmed roughly by county.</li>
					<li>If you do not find a name you are searching for in this table, try a different table.</li>
					<li>Residence Location is very rarely noted in the record but is provided in this table for cases where it is known and could be useful.</li>
					<li>Text entered into the filters is not case sensitive, but it is spelling sensitive. For example, a partial match on "Dal" would include Dallas and Dalam, but a partial match on "Dala" would be strictly Dalam.</li>

					<li>The <a href="https://txarchives.org/tslac/finding_aids/50082.xml" target="_blank">finding aid</a> has more information about these indexes and how to request the case files identified using this search.</li>
					</ul>
                </div>
              </div>
                <script>
                  var tooltip_case_number_1 = document.getElementById("tooltip_case_number_1");
                  var tooltip_case_number = document.getElementById("tooltip_case_number");
                  var span = document.getElementById("closeify_tooltip_case_number");
                  tooltip_case_number.onclick = function() {
                    tooltip_case_number_1.style.display = "block";
                  }
                  span.onclick = function() {
                    tooltip_case_number_1.style.display = "none";
					}
                    window.onclick = function(event) {
                    if (event.target == tooltip_case_number_1) {
                      tooltip_case_number_1.style.display = "none";
                    }
                  }              
                </script><p></p>
      </div>

      <div class="tdaSearch_search_form_left" style="padding-left:10px">
        <form id="form" onchange="master_filter()" onkeyup="master_filter()">
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="page">Page image number</label>
              <br>
              <input id="page" placeholder="Enter a image number" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="given">Given name</label>
              <br>
              <input id="given" placeholder="Enter the given name first" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="surname">Surname</label>
              <br>
              <input id="surname" placeholder="Enter the surname last" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="birthplace">Birthplace</label>
              <br>
              <input id="birthplace" placeholder="Enter the location of origin" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="date">Date of registration</label>
              <br>
              <input id="date" placeholder="Enter the date name put in registry" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="locations">Residence Location</label>
              <br>
              <input id="locations" placeholder="Enter the known location (note this is not given for most individuals)" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="county">County</label>
              <br>
              <input id="county" placeholder="Enter the County registered in" type="text" class="inputs">
            </h3>
          </div>
          <div id="NullResultsMessage" style="display:none;border:5px outset #a91d2f;background-color:lightgrey;text-align:center;border-radius:10px;">
            <p><span class="message" style="font-weight:bold;color:#a91d2f;font-size:2em;">Warning:</span><br><br>No matching results. Update your selections from the options above or click on reset to start over.</p>
          </div>
          <br>
          <div class="tdaSearch_thing5">
            <input onclick="location.reload()" style="height:2.75em;" type="reset" value="Reset options">
          </div>
        </form>
      </div>
      <div class="tdaSearch_search_form_right">
        <img title="Voter registration page" caption="Sample voter registration page" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2022/06/appealsIndex_thumb2.jpg" class="tdaSearch_graphic" id="court_graphic">
        <p class="tdaSearch_link1" style="text-align:center">
          <a href="https://tsl.access.preservica.com/uncategorized/SO_8858938f7-c553-43c5-bda8-58fb3cd6ad5d/" alt="Browse the voter registration lists">Browse the voter registration lists</a>
        </p>
      </div>
    </div>
'''

page_booty = '''<script type="text/javascript">
function master_filter() {
	var table, tr, i, td1, td2, td3, td4, td5, td6, td7, td8, td9, td10, td11;
	var page_num = page.value;
	var given_name = given.value;
	var filter_given_name = given_name.toUpperCase();
	var sur_name = surname.value;
	var filter_surname = sur_name.toUpperCase();
	var birth_place = birthplace.value;
	var filter_birthplace = birth_place.toUpperCase();
	var datify = date.value;
	var residence = locations.value;
	var filter_residence = residence.toUpperCase();
	var counties = county.value;
	var filter_county = counties.toUpperCase();
	table = document.getElementById("table");
	tr = table.getElementsByTagName("tr");
	for (i = 1; i < tr.length; i++) {
		td1 = tr[i].getElementsByTagName("td")[0];
		td2 = tr[i].getElementsByTagName("td")[1];
		td3 = tr[i].getElementsByTagName("td")[2];
		td4 = tr[i].getElementsByTagName("td")[3];
		td5 = tr[i].getElementsByTagName("td")[4];
		td6 = tr[i].getElementsByTagName("td")[5];
		td7 = tr[i].getElementsByTagName("td")[6];
		td8 = tr[i].getElementsByTagName("td")[7];
		td9 = tr[i].getElementsByTagName("td")[8];
		td10 = tr[i].getElementsByTagName("td")[9];
		td11 = tr[i].getElementsByTagName("td")[10];
		if (td1, td2, td3, td4, td5, td6, td7, td8, td9, td10, td11) {
			if ((td3.innerHTML.toUpperCase().indexOf(page_num) > -1) && (td5.innerHTML.toUpperCase().indexOf(filter_given_name) > -1) && (td6.innerHTML.toUpperCase().indexOf(filter_surname) > -1) && (td8.innerHTML.toUpperCase().indexOf(filter_birthplace) > -1) && (td9.innerHTML.toUpperCase().indexOf(datify) > -1) && (td10.innerHTML.toUpperCase().indexOf(filter_residence) > -1) && (td11.innerHTML.toUpperCase().indexOf(filter_county) > -1)) {
				tr[i].style.display = "";
			} else {
				tr[i].style.display = "none";
			}
		}
	}
	var tabula = 0;
	for (i = 1; i < tr.length; i++){
		if (tr[i].style.display != "none"){
			tabula = tabula + 1
		} else {
			tabula = tabula
		}
	}
	var NullResultsMessage;
	if (tabula < 1){
		NullResultsMessage = document.getElementById("NullResultsMessage").style.display="";
	} else {
		NullResultsMessage = document.getElementById("NullResultsMessage").style.display="none";
	}
}
</script>'''

source_spreadsheet = "/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/special_projects/ancestry/2274/reference table/reference_table.xlsx"  # input("curated spreadsheet to source data from: ")
source_metadata = "/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/newAPI/voter/level4"  # input("folder with metadata to crawl: ")
output = "/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/special_projects/ancestry/2274/voter"  # input("file to spit out, including filepath: ")

metadata_dict = {}

for dirpath, dirnames, filenames in os.walk(source_metadata):
    for filename in filenames:
        if filename.endswith("_metadata-1.xml") and filename.startswith("IO_"):
            print(filename)
            filename1 = os.path.join(dirpath, filename)
            filename2 = filename1.replace("_metadata-1.xml", ".xml")
            dom1 = ET.parse(filename1)
            root = dom1.getroot()
            namespaces = root.nsmap
            namespaces['xmlns'] = namespaces[None]
            namespaces.pop(None, None)
            namespaces['dcterms'] = "http://dublincore.org/documents/dcmi-terms/"
            namespaces['tslac'] = 'https://www.tsl.texas.gov/'
            namespaces['MetadataResponse'] = namespaces['xmlns']
            namespaces['EntityResponse'] = namespaces['xmlns']
            namespaces['ChildrenResponse'] = namespaces['xmlns']
            nameOfSpace = namespaces['xmlns'].split("/")[-1]
            dom2 = ET.parse(filename2)
            title = dom2.find("//xip:Title", namespaces=namespaces).text
            ref = dom2.find("//xip:Ref", namespaces=namespaces).text
            url = f"https://tsl.access.preservica.com/uncategorized/IO_{ref}/"
            title_text = dom1.find("//dcterms:title", namespaces=namespaces).text
            title_text = title_text.split("county, ")[-1]
            metadata_dict[title] = [url, title_text]
print(metadata_dict)
print("preservica data aggregated and printed to screen above")
# proceed = input("press enter to proceed or ctrl+c to abort")

# now constructing the html
table_head = "<table id='table'>\n<tbody>\n"
table_head = f"{table_head}<tr style='background-color:lightgray; border-bottom:3px solid blank; padding: 0px;' class='silly'><td>Image link</td><td>Microfilm reel</td><td>Image on reel</td>" \
             f"<td>Prefix</td><td>Given Name</td><td>Surname</td><td>Suffix</td><td>Birthplace</td><td>Date</td>" \
             f"<td>Residence Location</td><td>County</td></tr>"
df = PD.read_excel(source_spreadsheet, dtype=object)
listy = df.columns
start = "1"
html_text = ""
for row in df.itertuples():
    valuables = row_converter(row, listy)
    tester = f"{valuables['NamePrefix']}{valuables['GivenName']}{valuables['Surname']}{valuables['NameSuffix']}"
    if valuables['ImageFileName'] in metadata_dict.keys() and tester != "":
        if valuables['SourceArchiveRoll'] != start:
            html_text = f"{table_head}\n{html_text}</tbody>\n</table>\n"
            html_text = page_head + html_text + page_booty
            with open(f"{output}{start}.html", "w") as w:
                w.write(html_text)
            w.close()
            start = valuables['SourceArchiveRoll']
            html_text = ""
        month = month_converter(valuables['ResidenceMonth'])
        year = valuables['ResidenceYear']
        if year == "":
            year = "XXXX"
        day = valuables['ResidenceDay']
        date_str = ""
        if year != "Unspecified":
            date_str = f"{year}"
            if month != "XX":
                date_str = f"{date_str}-{month}"
                if day != "Unspecified":
                    date_str = f"{date_str}-{day}"
                else:
                    continue
            else:
                continue
        else:
            date_str = "Unspecified"
        temp_text = "\n<tr>"
        temp_text = f"{temp_text}\n\t<td><a href='{metadata_dict[valuables['ImageFileName']][0]}'>Link to image</a></td>"
        temp_text = f"{temp_text}\n\t<td>{rolio(valuables['SourceArchiveRoll'])}</td>"
        temp_text = f"{temp_text}\n\t<td>{valuables['ImageFileName'].split('-')[-1]}</td>"
        temp_text = f"{temp_text}\n\t<td>{prefix_fixer(valuables['NamePrefix'])}</td>"
        temp_text = f"{temp_text}\n\t<td>{initial_fixer(valuables['GivenName'])}</td>"
        temp_text = f"{temp_text}\n\t<td>{valuables['Surname']}</td>"
        temp_text = f"{temp_text}\n\t<td>{valuables['NameSuffix']}</td>"
        temp_text = f"{temp_text}\n\t<td>{valuables['BirthPlace']}</td>"
        temp_text = f"{temp_text}\n\t<td>{date_str}</td>"
        temp_text = f"{temp_text}\n\t<td>{valuables['ResidencePlace']}</td>"
        temp_text = f"{temp_text}\n\t<td>{valuables['ResidenceCounty']}</td>"
        temp_text = f"{temp_text}\n</tr>"
        html_text = f"{html_text}{temp_text}"
html_text = f"{table_head}\n{html_text}</tbody>\n</table>"
html_text = page_head + html_text + page_booty
with open(output, "w") as w:
    w.write(html_text)
w.close()
