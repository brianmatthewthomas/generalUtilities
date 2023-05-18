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

preamble = '''<head>
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
	</head>
<div style="width:100%">
<div width="100%" class="container">
      <h2 class="tdaSearch_search_title" style="text-align:center; color: #a91e2f;" id="top">
        <strong>Texas Court of Criminal Appeals Indexes look-up table</strong>
      </h2>
    </div>
<p class="tdaSearch_link2" style="text-align:center">
      <a href="https://tsl.access.preservica.com/uncategorized/SO_8fcb8f0c-20cb-4ba1-b30a-c75a10d969fb/" alt="Browse the Court of Criminal Appeals indexes">Browse the Court of Criminal Appeals indexes</a>
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
					<li>The column titled <i>PDF page number</i> indicates the page number in the PDF where the information can be found. This <strong>does not</strong> correspond to the page number within the physical volume.</li>
					<li>This table is derived from an exact transcript of the index. Name spelling and syntax have <i>not</i> been standardized, so it may be necessary to check for variations in name or acronym spellings.</li>
					<li>The search results will include entries that have the words you enter. For example, searching "smith" under Appellant will show results for Smith, Smithers, and Woodsmith, among others.</li>
					<li>The filters for this table do not support wildcard options. The text entered in the filter must be an exact match to at least part of what is in the table column. For example, "o Mills" will yield results for Alamo Mills Co. but "o?Mills" and "o*Mills" will not.</li>
					<li>Abbreviations are often included in the results. For example, "Jno." for "Jonathan," "Wm." for "William," and company names may be abbreviated. If you cannot find relevant results, try searching by abbreviations and alternate spellings.</li>
					<li>Some transcriptions have notes in [brackets]. These include possible spellings, alternate versions of the text as written, and other notes that may be helpful.</li>
					<li>Direct indexes are indexed by appellant. Reverse indexes are indexed by appellee. Please search both fields if you are unsure.</li>
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
              <label for="volume_drop">Volume name</label>
              <br>
              <select id="volume_drop">
                <option value="" selected="selected">Select volume</option>
				<option value="1892-1909">General Indexes, 1892-1909</option>
				<option value="1919">General Index, Oct 1919-Sep 1947</option>
				<option value="1896">Index to Docket (Austin), 1896</option>
				<option value="1905">Index to Docket (Austin), 1905</option>
				<option value="1908">Index to Docket (Austin), 1908</option>
              </select>
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="page">Page image number</label>
              <br>
              <input id="page" placeholder="Enter a image number" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="appellant">Appellant</label>
              <br>
              <input id="appellant" placeholder="Enter the Appellant name" type="text" class="inputs">
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3 style="margin-bottom:0.5em; line-height:1em; margin-top:10px;font-size:1em">
              <label for="appellee">Appellee</label>
              <br>
              <input id="appellee" placeholder="Enter the Appellee name" type="text" class="inputs">
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
        <img title="Index page" caption="Sample index volume page" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2023/05/judiciary_criminalAppeals_indexes.jpg" class="tdaSearch_graphic" id="court_graphic">
        <p class="tdaSearch_link1" style="text-align:center">
          <a href="https://tsl.access.preservica.com/uncategorized/SO_8fcb8f0c-20cb-4ba1-b30a-c75a10d969fb/" alt="Browse the Court of Criminal Appeals indexes">Browse the Court of Criminal Appeals indexes</a>
          </p>
      </div>
    </div>
<table id="table"><tbody>
<tr style="background-color:lightgray; border-bottom:3px solid blank; padding: 0px;" class="silly">
    <td>Volume name</td>
    <td>Image name</td>
    <td>Court count</td>
    <td>Court year</td>
    <td>Appellant</td>
    <td>Appellant Alias</td>
    <td>Appellee</td>
</tr>\n'''

js = '''</tbody></table>\n<script type="text/javascript">
function master_filter() {
	var table, tr, i, td1, td2, td3, td4, td5, td6, td7;
	var volume_num = volume_drop.options [volume_drop.selectedIndex].value; 
	var page_num = page.value;
	var appellant_name = appellant.value;
	var filter_appellant = appellant_name.toUpperCase();
	var appellee_name = appellee.value;
	var filter_appellee = appellee_name.toUpperCase();
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
			if ((td1.innerHTML.toUpperCase().indexOf(volume_num) > -1) && (td2.innerHTML.toUpperCase().indexOf(page_num) > -1) && (td5.innerHTML.toUpperCase().indexOf(filter_appellant) > -1) && (td7.innerHTML.toUpperCase().indexOf(filter_appellee) > -1)) {
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
spreadsheet = "/media/sf_Y_DRIVE/Ancestry/ingested/good_2147/spreadsheets_prepared/master2.csv"
df = PD.read_csv(spreadsheet, dtype=object, na_filter=False)
listy = df.columns
basic_text = ""
for row in df.itertuples():
    valuables = row_converter(row, listy)
    exceptions = ['Cover Material', "Rear Material"]
    if valuables['Appellant'] not in exceptions:
        tester = f"{valuables['Appellant']}{valuables['Appellee']}"
        if tester != "":
            basic_text = f"{basic_text}<tr>"
            for key in valuables:
                if key != "Index":
                    basic_text = f"{basic_text}<td>{valuables[key]}</td>"
            basic_text = f"{basic_text}</tr>\n"
with open("/media/sf_Y_DRIVE/Ancestry/ingested/good_2147/spreadsheets_prepared/master2.html", "w") as w:
    w.write(basic_text)
w.close()
with open("/media/sf_Y_DRIVE/Ancestry/ingested/good_2147/spreadsheets_prepared/master2.html", "r") as r:
    filedata = r.read()
    filedata = f"{preamble}{filedata}{js}"
    with open("/media/sf_Y_DRIVE/Ancestry/ingested/good_2147/spreadsheets_prepared/master2.html", "w") as w:
        w.write(filedata)
    w.close()


