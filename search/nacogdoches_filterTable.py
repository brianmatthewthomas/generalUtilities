import sys
import os
import pandas as PD

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
    sender = row_data['sender']
    recipient = row_data['recipient']
    location = row_data['Location']
    date = row_data['Date']
    series = row_data['series_path']
    microfilm_reel = row_data['Microfilm Reel Number']
    box = row_data['Box/Folder']
    row = f'''<tr>
        <td>{sender}</td>
        <td>{recipient}</td>
        <td>{location}</td>
        <td>{date}</td>
        <td>{series}</td>
        <td>{microfilm_reel}</td>
        <td>{box}</td>
    </tr>'''
    return row

df = PD.read_excel("/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/search/nacogdoches/Nacogdoches Archives_Working Copy.xlsx", sheet_name="Browse Tool Info", dtype=object)
print(df)
listy = df.columns
start = "1"
locations = set()
series = set()
table_html = ""
for row in df.itertuples():
    my_dict = row_converter(row, listy)
    my_dict['sender'] = my_dict['Sender Name']
    my_dict['recipient'] = my_dict['Recipient Name']
    locations.add(my_dict['Location'])
    series_name = f"{my_dict['Record Group']}, {my_dict['Series']}, {my_dict['SubSeries']}"
    while series_name.endswith(", "):
        series_name = series_name[:-2]
    series.add(series_name)
    my_dict['series_path'] = series_name
    my_row = row_generator(my_dict)
    table_html += my_row

locations = optionGenerator(locations)
series = optionGenerator(series)

table_head = "<table id='table'>\n<tbody>\n"
table_head = f"{table_head}<tr style='background-color:lightgray; border-bottom:3px solid blank; padding: 0px;' class='silly'><td>Sender Name</td><td>Recipient Name</td><td>Location</td>" \
             f"<td>Date</td><td>Records Series</td><td>Microfilm Reel</td><td>Box</td></tr>"

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
	'''
html_top = f'''
<div style="width:100%">
<div width="100%" class="container">
      <h2 class="tdaSearch_search_title" style="text-align:center; color: #a91e2f;" id="top">
        <strong>Nacogdoches Archive filter table</strong>
      </h2>
    </div>
<p class="tdaSearch_link2" style="text-align:center">
      <a href="https://tsl.access.preservica.com/uncategorized/SO_858938f7-c553-43c5-bda8-58fb3cd6ad5d/" alt="Browse the Nacogdoches Archive">Browse the Nacogdoches Archive</a>
    </p>
<div align="center" class="tdaSearch_search_container">
      <div align="left" class="tdaSearch_search_warning">
        <p>Use the options below to filter correspondence and other material listed in the <a href="#table">results table</a>. Search tips:
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
      </div>

      <div class="tdaSearch_search_form_left" style="padding-left:10px">
        <form id="form" onchange="master_filter()" onkeyup="master_filter()">
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="sender">Sender</label>
              <br>
              <input id="sender" placeholder="Enter Sender name" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="recipient">Recipient name</label>
              <br>
              <input id="recipient" placeholder="Enter Recipient name" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="location_drop">Location mentioned in record</label>
              <br>
              <select id="location_drop">
                <option value="">Selection a location referenced in the correspondence</option>
                {locations}
              </select>
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="date">Date on record</label>
              <br>
              <input id="date" placeholder="YYYY-MM-DD" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="record_group">Found in Record Group</label>
              <br>
              <select id="record_group">
                <option value="">Select an applicable record group</option>
                {series}
              </select>
            </h3>
          </div>
          <div id="NullResultsMessage" style="display:none;border:5px outset #a91d2f;background-color:lightgrey;text-align:center;border-radius:10px;">
            <p>No matching results. Update your selections from the options above or click on reset to start over.</p>
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
          <a href="https://tsl.access.preservica.com/uncategorized/SO_8858938f7-c553-43c5-bda8-58fb3cd6ad5d/" alt="Browse the Nacogdoches Archive">Browse the Nacogdoches Archive</a>
        </p>
      </div>
    </div>
'''

page_booty = '''<script type="text/javascript">
function master_filter() {
	var table, tr, i, td1, td2, td3, td4, td5, td6, td7;
	var filter_sender = sender.value.toUpperCase();
	var filter_recipient = recipient.value.toUpperCase();
	var filter_location = location_drop.options[location_drop.selectedIndex].value;
	var filter_date = date.value;
	var filter_series = record_group.options[record_group.selectedIndex].value;
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
		if (td1, td2, td3, td4, td5, td6, td7) {
			if ((td1.innerHTML.toUpperCase().indexOf(filter_sender) > -1) && (td2.innerHTML.toUpperCase().indexOf(filter_recipient) > -1) && (td3.innerHTML.indexOf(filter_location) > -1) && (td4.innerHTML.toUpperCase().indexOf(filter_date) > -1) && (td5.innerHTML.indexOf(filter_series) > -1)) {
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

my_html = f"{page_head}{html_top}{table_head}{table_html}</table>{page_booty}</html>"

with open("/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/search/nacogdoches/output.html", "w") as w:
    w.write(my_html)
w.close()
print("all done")

