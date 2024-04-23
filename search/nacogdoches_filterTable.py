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

url_dict = {
    "Coahuila records, Censuses": "63234c67-2d84-4783-8010-3823f3f1c3f1",
    "Coahuila records, Elections": "d83abb22-a696-4783-b08e-fb9412711ed8",
    "Coahuila records, General Correspondence": "3c3c203a-ab6d-40bf-949d-1ac38c3a00fc",
    "Nacogdoches records, Colonial and National Government, General Correspondence": "e07ac52f-0434-48a2-8431-86a4924c8baf",
    "Nacogdoches records, Colonial and National Government, Royal and Federal Decrees": "84e132f4-20ba-451d-9c7f-519d41e2079e",
    "Nacogdoches records, Correspondence of the Captains General": "4ead81f0-2442-41e1-9aa0-21d595e9424e",
    "Nacogdoches records, Court of the Alcalde": "ca542d92-c055-4b4a-8888-0616647dc669",
    "Nacogdoches records, Department of Texas, Correspondence of Jefe": "f5899066-173e-4b06-a101-f22ffec33d14",
    "Nacogdoches records, Department of Texas, Correspondence of the Comandante": "89b9e663-48c4-4a2d-8e2e-79420640d439",
    "Nacogdoches records, Department of Texas, General Correspondence": "3b16b0f4-0fca-41cd-84c2-83b09a3c453c",
    "Nacogdoches records, Municipality, Accounts": "d26aae61-1c2a-4985-80f7-48754dd54440",
    "Nacogdoches records, Municipality, Correspondence of the Alcalde": "6fe875be-227d-4da7-8d93-a414796072f1",
    "Nacogdoches records, Municipality, Correspondence of the Comandante": "c921d31f-a3bb-45cf-a681-49f5c8a54ba8",
    "Nacogdoches records, Municipality, Correspondence of the Jefe": "a0407bbe-bfb3-4c9c-996b-a3ecd0cfe6e6",
    "Nacogdoches records, Municipality, Correspondence of the Juez": "febdf52f-bb83-42ca-9c4d-4c073e0201b8",
    "Nacogdoches records, Municipality, General Correspondence": "8d743c52-a8b0-453f-ae28-90c4b57f218c",
    "Nacogdoches records, Municipality, Oaths and Citizenships": "aff594a6-558e-4cbd-99eb-eb681e0e41fe",
    "Nacogdoches records, Municipality, Proceedings": "962281c5-94c4-4bca-a232-73f3491d89b0",
    "Nacogdoches records, Municipality, Procesos Legales": "2996c1d5-7c1e-4807-a55b-8de95ca983b5",
    "Nacogdoches records, Municipality, Subordinate": "78208102-9e2b-4c6b-a930-63c4978dd691",
    "Nacogdoches records, Province of Coahuila-Texas, Correspondence of the Governors": "88de67d8-2c82-4823-beb2-98c4b7e1d83b",
    "Nacogdoches records, Province of Coahuila-Texas, Decrees": "34bf630f-cbad-4bd8-85f3-abb9cb82a5af",
    "Nacogdoches records, Province of Coahuila-Texas, General Correspondence": "29dc0ef8-1fdd-44c7-bccc-7edebaa6a1f7",
    "Nacogdoches records, Province of Coahuila-Texas, Residencias": "cda416d5-8d9f-45a5-bebf-bc89534b4d3f"
}


def row_generator(row_data):
    sender = row_data['sender']
    recipient = row_data['recipient']
    location = row_data['Location']
    date = row_data['Date']
    series = row_data['series_path']
    microfilm_reel = row_data['Microfilm Reel Number']
    box = row_data['Box/Folder']
    while box.endswith("*"):
        box = box[:-1]
    row = f'''<tr>
        <td>{sender}</td>
        <td>{recipient}</td>
        <td>{location}</td>
        <td>{date}</td>
        <td><a href="https://tsl.access.preservica.com/uncategorized/SO_{url_dict[series]}" target="_blank">{series}</a></td>
        <td>{microfilm_reel}</td>
        <td>{box}</td>
    </tr>'''
    return row

df = PD.read_excel("/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/search/nacogdoches/Nacogdoches Archives_Working Copy.xlsx", sheet_name="Browse Tool Info", dtype=object)
print(df)
listy = df.columns
start = "1"
locations1 = set()
series1 = set()
locations2 = set()
series2 = set()
table_html1 = ""
table_html2 = ""
for row in df.itertuples():
    my_dict = row_converter(row, listy)
    if my_dict['Classification'] == "Correspondence":
        my_dict['sender'] = my_dict['Sender Name']
        my_dict['recipient'] = my_dict['Recipient Name']
        locations1.add(my_dict['Location'])
        series_name = f"{my_dict['Record Group']}, {my_dict['Series']}, {my_dict['SubSeries']}"
        while series_name.endswith(", "):
            series_name = series_name[:-2]
        series1.add(series_name)
        my_dict['series_path'] = series_name
        my_row = row_generator(my_dict)
        table_html1 += my_row
    else:
        my_dict['sender'] = my_dict['Sender Name']
        if my_dict['Title'] != "":
            my_dict['recipient'] = my_dict['Title']
        elif my_dict['Description'] != "":
            my_dict['recipient'] = my_dict['Description']
        else:
            my_dict['recipient'] = "Untitled document"
        if len(my_dict['recipient']) > 50:
            my_dict['recipient'] = f"{my_dict['recipient'][:50]}..."
        locations2.add(my_dict['Location'])
        series_name = f"{my_dict['Record Group']}, {my_dict['Series']}, {my_dict['SubSeries']}"
        while series_name.endswith(", "):
            series_name = series_name[:-2]
        series2.add(series_name)
        my_dict['series_path'] = series_name
        my_row = row_generator(my_dict)
        table_html2 += my_row


locations1 = optionGenerator(locations1)
series1 = optionGenerator(series1)
locations2 = optionGenerator(locations2)
series2 = optionGenerator(series2)

table_head = "<table id='table'>\n<tbody>\n"
table_head = f"{table_head}<tr style='background-color:lightgray; border-bottom:3px solid blank; padding: 0px;' class='silly'><td>Sender Name</td><td>Recipient Name</td><td>Location</td>" \
             f"<td>Date</td><td>Records Series</td><td>Microfilm Reel</td><td>Box.Folder</td></tr>"
table_head2 = table_head.replace("Sender Name", "Creator").replace("Recipient Name", "Title/Description")
aboutme = "The Nacogdoches Archives Record Group includes a variety of records maintained by national, regional, and local officials--both political and military--of the Mexican government from the mid-eighteenth into the early nineteenth century. The records include Spanish colonial and Mexican national government correspondence, decrees, and reports; the correspondence and reports of military and political officials stationed in the Provincias Internas (1776-1824) and, later, the State of Coahuila y Texas; records of the Department of Nacogdoches (northeastern area of Texas), 1830-1836; and municipal records of Nacogdoches and vicinity. Until the 1830s, the records are written in Spanish. The records of the Municipality of Nacogdoches (not to be confused with the Department of Nacogoches) are a mixture of both English- and Spanish-language documents after 1830."
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
html_top1 = f'''
<div style="width:100%">
<div width="100%" class="container">
      <h2 class="tdaSearch_search_title" style="text-align:center; color: #a91e2f;" id="top">
        <strong>Nacogdoches Archive Correspondence filter table</strong>
      </h2>
    </div>
<p class="tdaSearch_link2" style="text-align:center">
      <a href="https://tsl.access.preservica.com/uncategorized/SO_858938f7-c553-43c5-bda8-58fb3cd6ad5d/" alt="Browse the Nacogdoches Archive">Browse the Nacogdoches Archive</a>
    </p>
    <p><a href="#about">About the Nacogdoches Archive</a></p>
<div align="center" class="tdaSearch_search_container">
      <div align="left" class="tdaSearch_search_warning">
        <p>Use the options below to filter correspondence and other material listed in the <a href="#table">results table</a>. For more information how to use this search tool click <a href="#tdaSearchHelp" title="Link to description of how this tool works">here</a>. Search tips for senders and recipients
		<img class="tooltip_image" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2020/06/200px-Icon-round-Question_mark.svg_.png" max-width="5px" style="cursor:help" title="Click for search tips" id="tooltip_number">
              </p><div class="tooltip-test" id="tooltip_number_1" style="display:none;">
                <div class="modal-content">
                    <span class="closeify" id="closeify_tooltip_number">x</span>
					<h2 style="color:#a91d2f; text-align:center">Sender and Recipient Search tips</h2>
					<p>Sender and recipient names may be incomplete. Include last names only in your preliminary search, in addition to full names.</p>
					<p>Names are also likely to have variations in spelling. For example, “Ybarbo” “Ibarbo” “Ybarvo” and “Ibarvo” might be interchangeable.</p>
					<p>Some sender and recipient names are titles, such as “Governor” or “Alcalde” rather than individual names. Be sure to reference the <a href"https://www.tsl.texas.gov/ref/abouttx/prerepub.html" title="Link to list of Pre-Republic era Governors of Texas">"Pre-Republic Governors of Texas”</a> list and/or the <a href="https://www.tshaonline.org/handbook" title="Link to Texas State Historical Association's Handbook of Texas online">Handbook of Texas</a> to determine identities and search by the individual’s title when available, in addition to their full name and last name only.</p>
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
                {locations1}
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
                {series1}
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
html_top2 = f'''
<div style="width:100%">
<div width="100%" class="container">
      <h2 class="tdaSearch_search_title" style="text-align:center; color: #a91e2f;" id="top">
        <strong>Nacogdoches Archive Documents filter table</strong>
      </h2>
    </div>
<p class="tdaSearch_link2" style="text-align:center">
      <a href="https://tsl.access.preservica.com/uncategorized/SO_858938f7-c553-43c5-bda8-58fb3cd6ad5d/" alt="Browse the Nacogdoches Archive">Browse the Nacogdoches Archive</a>
    </p>
    <p><a href="#about">About the Nacogdoches Archive</a></p>
<div align="center" class="tdaSearch_search_container">
      <div align="left" class="tdaSearch_search_warning">
        <p>Use the options below to filter correspondence and other material listed in the <a href="#table">results table</a>. For more information how to use this search tool click <a href="#tdaSearchHelp" title="Link to description of how this tool works">here</a>.</p>
      </div>

      <div class="tdaSearch_search_form_left" style="padding-left:10px">
        <form id="form" onchange="master_filter()" onkeyup="master_filter()">
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="creator">Creator</label>
              <br>
              <input id="creator" placeholder="Enter creator name" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="description">Title/Description</label>
              <br>
              <input id="description" placeholder="Enter possible description" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="location_drop">Location mentioned in record</label>
              <br>
              <select id="location_drop">
                <option value="">Selection a location referenced in the correspondence</option>
                {locations2}
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
                {series2}
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
bottom_text = f'''
    <div class="tdaSearch_bottom_text">
    <p><a href="#top">Back to top</a></p>
    <h2 id="tdaSearchHelp">How to use the Nacogdoches Archive Browse Tool</h2>
    <p>The Nacogdoches Archives Browse Tool was developed to assist researchers in filtering the collected data to narrow down results. Filtering options include sender name, recipient name, sender’s location, date (YYYY-MM-DD), image and document location (microfilm reel and box/folder) and associated record group, series and subseries if applicable.</p>
    <p>It is not a search engine and will not return exact or perfect results, as the data itself is not perfect and remains a working, ongoing project. Not every entry has every field available to reference. Some entries may not include a location, date, sender or recipient name, etc.</p>
    <p>Alternatively, there is a spreadsheet to download that researchers can manipulate and explore freely, containing the entire data set.</p>
    <p>Please note, some records have been digitized from their original microfilm reel but have not been included in the dataset. There are images available for the <em>Brazos Archives record group</em> and <em>Additional Correspondence and Printed Material series</em> under the <em>Nacogdoches record group</em>, but these images do not have corresponding data points in the spreadsheet and will require individual review.</p>
    <h2 id="about">About the Nacogdoches Archive</h2>
     <p>{aboutme}</p>
    </div>
'''

page_booty1 = '''<script type="text/javascript">
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
tooltip1_script = '''<script>
	var tooltip_number_1 = document.getElementById("tooltip_number_1");
	var tooltip_number = document.getElementById("tooltip_number");
	var span = document.getElementById("closeify_tooltip_number");
	tooltip_number.onclick = function() {
		tooltip_number_1.style.display = "block";
	}
	span.onclick = function() {
		tooltip_number_1.style.display = "none";
	}
	window.onclick = function(event) {
		if (event.target == tooltip_number_1) {
			tooltip_number_1.style.display = "none";
		}
	}
</script>'''

page_booty2 = '''<script type="text/javascript">
function master_filter() {
	var table, tr, i, td1, td2, td3, td4, td5, td6, td7;
	var filter_creator = creator.value.toUpperCase();
	var filter_description = description.value.toUpperCase();
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
			if ((td1.innerHTML.toUpperCase().indexOf(filter_creator) > -1) && (td2.innerHTML.toUpperCase().indexOf(filter_description) > -1) && (td3.innerHTML.indexOf(filter_location) > -1) && (td4.innerHTML.toUpperCase().indexOf(filter_date) > -1) && (td5.innerHTML.indexOf(filter_series) > -1)) {
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

my_correspondence_html = f"{page_head}{html_top1}{table_head}{table_html1}</table>{bottom_text}{page_booty1}{tooltip1_script}</html>"
my_other_html = f"{page_head}{html_top2}{table_head2}{table_html2}</table>{bottom_text}{page_booty2}</html>"

with open("/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/search/nacogdoches/output_correspondence.html", "w") as w:
    w.write(my_correspondence_html)
w.close()
print("all done")
with open("/media/sf_F_DRIVE/Archives/Electronic_records/Texas_Digital_Archive/working_materials/search/nacogdoches/output_other.html", "w") as w:
    w.write(my_other_html)
w.close()
print("all done")

