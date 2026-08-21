import lxml.etree as ET
import os

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

path_to_files = input("Enter the folderpath: ")

search_page = os.path.join(path_to_files, 'search.html')

table = '''<table id="senate">
    <tbody>
        <tr style="background-color:lightgray;border-bottom:3px solid green;padding: 0px" class="silly">
            <td class="drop0"> </td>
            <td>Recording No.</td>
            <td>Title</td>
            <td class="drop2">Legislature</td>
            <td class="drop3">Committee</td>
            <td>Date(s)</td>
            <td width="25%" class="drop1">Keyword(s)</td>
        </tr>\n'''

with open(search_page, 'w', encoding='utf-8') as file:
    file.write(table)
file.close()

date_set = set()
legislature_set = set()
committee_set = set()

for dirpath, dirnames, filenames in os.walk(f"{path_to_files}/level4"):
    for filename in filenames:
        if filename.endswith(".xml") and "metadata" in filename:
            filename = os.path.join(dirpath, filename)
            with open(filename, "r") as r:
                filedata = r.read()
                if "dcterms" in filedata and ": transcription" not in filedata:
                    dom = ET.parse(filename)
                    root = dom.getroot()
                    namespaces = getNamespaces(root)
                    xip = ""
                    xip = root.find(".//xip:Entity", namespaces=namespaces).text
                    recording_id = root.find(".//dcterms:identifier.filename", namespaces=namespaces).text
                    title = ""
                    title = root.find(".//dcterms:title", namespaces=namespaces).text
                    legislature = ""
                    legislature = root.find(".//tslac:legislatureSession", namespaces=namespaces).text
                    legislature_set.add(legislature)
                    committee = ""
                    committee = root.find(".//tslac:senateCommittee", namespaces=namespaces).text
                    committee_set.add(committee)
                    dates_text = ""
                    dates = root.xpath(".//dcterms:date.created", namespaces=namespaces)
                    for date in dates:
                        date_set.add(date.text)
                        dates_text = f"{dates_text}{date.text}; "
                    while dates_text.endswith("; "):
                        dates_text = dates_text[:-2]
                    keywords_text = ""
                    if "keyword" in filedata:
                        keywords = root.xpath(".//tslac:keyword", namespaces=namespaces)
                        for keyword in keywords:
                            keywords_text = f"{keywords_text}{keyword.text}; "
                        while keywords_text.endswith("; "):
                            keywords_text = keywords_text[:-2]
                    text = f"\t\t<tr>\n"
                    text = f"""{text}\t\t\t<td class="drop0">{recording_id}</td>\n"""
                    text = f"""{text}\t\t\t<td><a target="_blank" href="https://tsl.access.preservica.com/uncategorized/IO_{xip}" title="Link to recording number {recording_id}">{recording_id}</a></td>\n"""
                    text = f"""{text}\t\t\t<td>{title}</td>\n"""
                    text = f"""{text}\t\t\t<td class="drop2">{legislature}</td>\n"""
                    text = f"""{text}\t\t\t<td class="drop3">{committee}</td>\n"""
                    text = f"""{text}\t\t\t<td>{dates_text}</td>\n"""
                    text = f"""{text}\t\t\t<td class="drop1">{keywords_text}</td>\n\t\t</tr>\n"""
                    with open(search_page, 'a', encoding='utf-8') as file:
                        file.write(text)
                    file.close()
with open(search_page, 'a', encoding='utf-8') as file:
    file.write("\t</tbody>\n</table>\n")
file.close()

for dirpath, dirnames, filenames in os.walk(f"{path_to_files}/level1"):
    for filename in filenames:
        if filename.endswith(".xml") and "metadata" in filename:
            leg_number = filename.split("_")[1]

date_set = list(date_set)
date_set.sort()
date_set_text = ""
for item in date_set:
    date_set_text = f'{date_set_text}\n\t\t\t\t\t<option value="{item}">{item}</option>'

legislature_set = list(legislature_set)
legislature_set.sort()
legislature_text = ""
for item in legislature_set:
    legislature_text = f'{legislature_text}\n\t\t\t\t\t<option value="{item}">{item}</option>'

committee_set = list(committee_set)
committee_set.sort()
committee_text = ""
for item in committee_set:
    committee_text = f'{committee_text}\n\t\t\t\t\t<option value="{item}">{item}</option>'

some_javascript = '''function master_filter() {
                var table, tr, i, td1, td2, td3, td4, td5, td6, td7;
                var recording_number = recording_num.value;
                var filter_recording_number = recording_number.toUpperCase();
                var dately = date_drop.options [date_drop.selectedIndex].value;
                var legislature = legislature_drop.options [legislature_drop.selectedIndex].value;
                var committee = committee_drop.options [committee_drop.selectedIndex].value;
                table = document.getElementById("senate");
                tr = table.getElementsByTagName("tr");
                for (i = 1; i < tr.length; i++) {
                    td1 = tr[i].getElementsByTagName("td")[0];
                    td2 = tr[i].getElementsByTagName("td")[1];
                    td3 = tr[i].getElementsByTagName("td")[2];
                    td4 = tr[i].getElementsByTagName("td")[3];
                    td5 = tr[i].getElementsByTagName("td")[4];
                    td6 = tr[i].getElementsByTagName("td")[5];
                    td7 = tr[i].getElementsByTagName("td")[6];
                    if (td1, td3, td4, td5, td6) {
                        if ((td1.innerHTML.toUpperCase().indexOf(filter_recording_number) > -1) && (td3.innerHTML.indexOf(legislature) > -1) && (td4.innerHTML.indexOf(committee) > -1) && (td5.innerHTML.indexOf(dately) > -1)) {
                            tr[i].style.display = "";
                        } else {
                            tr[i].style.display = "none";
                        }
                    }
                }
                var recording_num1, recording_num2, case_num_note;
                if (recording_number != "") {
                    recording_num1 = "dcterms.dcterms_filename_freetext/" + recording_number + "*|";
                    recording_num2 = "dcterms.dcterms_filename_freetext/" + recording_number + "*|";
                    recording_num_note = document.getElementById("recording_num_note").style.display="inline";
                } else {
                    recording_num1 = "";
                    recording_num2 = "";
                    recording_num_note = document.getElementById("recording_num_note").style.display="none";
                }
                var legislature_num1, legislature_num2, legislature_note;
                if (legislature != "") {
                    legislature_num1 = "dcterms.leg_session/" + legislature + "*|";
                    legislature_num2 = "dcterms.leg_session/" + legislature + "*|";
                    legislature_note = document.getElementById("legislature_note").style.display="inline";
                } else {
                    legislature_num1 = "";
                    legislature_num2 = "";
                    legislature_note = document.getElementById("legislature_note").style.display="none";
                }
                var committee1, committee2, committee_note;
                if (committee != "") {
                    committee1 = "dcterms.senate_committee/" + committee + "*|";
                    committee2 = "dcterms.senate_committee/" + committee + "*|";
                    committee_note = document.getElementById("committee_note").style.display="inline";
                } else {
                    committee1 = "";
                    committee2 = "";
                    committee_note = document.getElementById("committee_note").style.display="none";
                }
                var date1, date2, date_note;
                if (dately != "") {
                    date1 = "dcterms.dcterms_date/" + dately + "|";
                    date2 = "dcterms.dcterms_date/" + dately + "|";
                    date_note = document.getElementById("date_note").style.display="inline";
                } else {
                    date1 = "";
                    date2 = "";
                    date_note = document.getElementById("date_note").style.display="none";
                }
                var a = document.getElementById("linkavich");
                a.href = "https://tsl.access.preservica.com/?s="
            + search_all.value 
            + "&parenthierarchy=so_goes_here" 
            + "&hh_cmis_filter=" 
            + recording_num1 
            + legislature_num1 
            + committee1 
            + date1 
            + "&saved_filters=" 
            + recording_num2 
            + legislature_num2 
            + committee2 
            + date2;
            }'''

some_javascript2 = '''<script>
function flip() {
	var tooltip, tooltip_image;
	if (document.getElementById("tooltip").style.display="none"){
		tooltip = document.getElementById("tooltip").style.display="block";
		tooltip_image = document.getElementById("tooltip_image").style.display="none";
	}
}
function fliper() {
	var tooltip, tooltip_image;
	if (document.getElementById("tooltip").style.display="block"){
		tooltip = document.getElementById("tooltip").style.display="none";
		tooltip_image = document.getElementById("tooltip_image").style.display="block";
	}
}'''

some_style = """td{border-bottom: 1px solid green; border-right: 1px solid green; padding: 0px;}
			tr:hover{background-color: lightgray;}
			.form-button{font-weight:bold; font-size:1.5em; border:2px outset darkgrey; border-radius:5px; background-color:lightgrey; font-weight:bold; color:#005297; font-family:Georgia}
			.form-button1{padding:1px; font-size:1.5em; font-weight:bold; border:2px outset darkgrey; border-radius:5px; background-color:lightgrey; text-decoration:none;color:#005297;font-family:Georgia}
			.form-button:hover, .form-button1:hover {border:2px inset darkgrey;}
			.image{padding-left:20px;vertical-align:center;max-width=400}.form{max-width:710px;}
			.container{display:flex; border: 3px solid rgb(147,35,29); border-radius: 10px; background-color: whitesmoke;}
			.inputs{width:700px;}
			@media(max-width:1230px){.image{max-width:200px}}
			@media(max-width:1130px){.image{display:none}.form{margin:auto}}
			@media(max-width:900px){.container{margin:0px;}.inputs{width:95%}.keyword{display:none}}"""

some_javascript = some_javascript.replace("so_goes_here", leg_number)

some_text = path_to_files.split("/")[-1].split("\\")[-1]

with open(search_page, "r") as r:
    filedata = r.read()
    new_text = f"""<html>
    <body>
                <div class="container">
                    <h2 class="tdaSearch_search_title">
                        <strong>Texas Senate Recordings\n{some_text} Legislature Custom Search</strong>
                    </h2>
                    <p/>
                </div>
                <p class="tdaSearch_link2" style="text-align: center">
                    <a href="https://tsl.access.preservica.com/tda/texas-state-government/legislature/senate/">Browse the senate recordings</a>
                </p>
                <p>
                    <a href="#about">About the Senate Recordings</a>
                </p>
                <div align="center" class="tdaSearch_search_container">
                    <div align="left" class="tdaSearch_search_warning">
                        <p>Use the options below to filter recordings listed in the <a href="#senate">results table</a>. Then click a recording number link from the table <em>or</em> use the "Show Results in the TDA" button below the table.</p>
                        <p/>
                </div>
                <div class="tdaSearch_search_box">
                    <div class="tdaSearch_search_form_left" id="tdaSearch_search_form_left_senate">
                        <form class="form" style="padding-top: 10px; padding-left: 10px;" onkeyup="master_filter()" onchange="master_filter()" onsubmit="return dosearch();" id="form">
                            <div class="tdaSearch_thing1">
                                <h3>
                                    <label for="recording_num">Recording Number</label>
                                    <strong style="color:purple; display:none;" id="recording_num_note"> *Active filter</strong>
                                    <br/>
                                    <input type="text" placeholder="Enter a recording number" id="recording_num" class="inputs">
                                </h3>
                            </div>
                            <div class="tdaSearch_thing1">
                                <h3>
                                    <label for="date_drop">Date</label>
                                    <span style="color:#a91d2f"; display:none;" id="date_updated"> *options updated</span>
                                    <strong style="color:purple; display:none;" id="date_note"> *Active filter</strong>
                                    <br/>
                                    <select class="inputs" id="date_drop">
                                        <option value="">Select date</option>{date_set_text}
                                    </select>
                                </h3>
                            </div>
                            <div class="tdaSearch_thing1">
                                <h3>
                                    <label for="legislature_drop">Legislature Number</label>
                                    <span style="color:#a91d2f; display:none;" id="legislature_updated"> *options updated</span>
                                    <span style="color:purple; display:none;" id="legislature_note"> *Active filter</span>
                                    <br/>
                                    <select class="inputs" id="legislature_drop">
                                        <option value="">Select session or term</option>{legislature_text}     
                                    </select>
                                </h3>                
                            </div>
                            <div class="tdaSearch_thing1">
                                <h3>
                                    <label for="committee_drop">Committee Name</label>
                                    <span style="color:#a91d2f; display:none;" id="committee_updated"> *options updated</span>
                                    <span style="color:purple; display:none;" id="committee_note"> *Active filter</span>
                                    <br/>
                                    <select class="inputs" id="committee_drop">
                                        <option value="">Select committee</option>{committee_text}
                                    </select>
                                     <span style="font-size:0.7em"> *Senate floor discussions/debate are referred to as "Senate Floor"</span>
                                 </h3>
                             </div>
                             <div class="tdaSearch_thing1">
                                <h3>
                                    <label for="search_all">Keyword Search</label>
                                    <img decoding="async" class="tooltip_image" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2020/06/200px-Icon-round-Question_mark.svg_.png" max-width="5px" style="cursor:help" onclick="flip()">
                                    <strong style="color:purple; display:none;" id="keyword_note"> *Active filter</strong>
                                    <br/>
                                    <input type="text" placeholder="Enter your keyword term(s)" id="search_all" class="inputs" name="search_all">
                                </h3>
                            </div>
                            <div id="NullResultsMessage" style="display:none; border:5px outset $a91d2f; background-color:lightgrey; text-align:center; border-radius:10px;">
                                <p>
                                    <span class="message" style="font-weight:bold; color:#a91d2f; font-size:2em">Warning:</span>
                                    <br/>
                                    <br/>
                                    No matching results. Update your selections from the otpions above or click on reset to start over.
                                </p>
                            </div>
                            <div class="tdaSearch_thing5">
                                <input onclick="location.reload()" value="Reset" type="reset" class="form-button">
                            </div>
                            <p/>
                        </form>
                    </div>
                    <div class="tdaSearch_search_form_right" id="tdaSearch_search_form_right_senate">
                        <div id="tooltip_image">
                            <img decoding="async" title="Texas Senate logo" alt="Texas_Senate" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2019/12/200px-Seal_of_State_Senate_of_Texas.svg_.png" class="tdaSearch_graphic" id="senate_graphic">
                        </div>
                        <div id="tooltip" style="border:5px outset #2b6da7; border-radius:10px; display:none; max-width:400px">
                            <h3 id="keyword">
                                <strong style="color:a91d2f">About Keywords</strong>
                            </h3>
                            <p style="text-align:left; padding-left:5px; padding-right:5px;">The "Keyword search" matches the Keyword(s) column in the table above. Keywords can include the bill number, date, committee name, description, or subject. Bill numbers use abbreviations. For example, House Bill 174 is written as HB174 and House Joint Resolution 40 is written as HJR40.</p>
                            <p style="text-align:left; padding-left:5px; padding-right:5px;">Keywords were assigned based upon notes provided by Senate Staff Services. Not all recordings on a specific topic will have a keyword assigned to them.  Keywords can be used as a starting point for finding recordings, but should be used in coordination with Session, Committee, and Date. We suggest you consult the Legislative Reference Library's <a href="https://lrl.texas.gov/legis/BillSearch/index.cfm" target="_blank" title="Legislative Reference Library Archive System">Legislative Archive System</a> for a listing of <em>dates</em> and <em>committees</em> applicable to a bill as well as additional information such as bill text.</p>
                            <p>
                                <span style="color:#2b6da7; text-decoration:underline; cursor:pointer" tabindex:"0" onclick="flipper()" title="close">close</span>
                            </p>
                        </div>
                        <p class="tdaSearch_link1" style="text-align:center">
                            <a href="https://tsl.access.preservica.com/tda/texas-state-government/legislature/senate/">Browse the Senate Records</a>
                        </p>
                        <p/>
                    </div>
                    <p/>
                </div>
            </div>
        </div>
        {filedata}
        <div class="tdaSearch_thing5">
            <a class="form-button1" id="linkavich" href="">Show Results in the TDA</a>
        </div>
        <div class="tdaSearch_bottom_text">
            <h2 id="about">
                <strong>About Senate Recordings</strong><br>
            </h2>
            <p>
                <a href="#top">Back to top</a>
            </p>
            <p>The Texas Senate began to systematically record its committee hearings and floor debates during the 4th Called Session of the 62nd Legislature (1972). The recordings contain floor debate, press conferences, speeches, interviews, hearings, ceremonies, and joint meetings with House committees. Recordings span the 62nd Legislature, 4th Called Session, through the 79th Legislature, Interim Term (2006). These digital copies of the original 50,463 Senate audiotape recordings were created by the Texas State Library and Archives Commission with grant funding provided by the Library Services and Technology Act, Institute of Museum and Library Services. Selected recordings from the 76th Legislature (1999) to present are available through <a href="https://senate.texas.gov/av-archive.php" target="_blank" rel="noopener noreferrer">Senate Staff Services</a>.</p>
            <p>You can find more information about the Texas Senate recordings in the <a href="https://txarchives.org/tslac/finding_aids/13001.xml" target="_blank" rel="noopener noreferrer">online finding aid</a>. For additional assistance with these and other records, please contact us at <a href="mailto:ref@tsl.texas.gov">ref@tsl.texas.gov</a>.</p>
            <p><strong style="color:#a91e2f">Note:</strong> Legal and physical custody of the original audiocassette tapes now resides with the Legislative Reference Library. Access to the original audiocassette tapes must be requested through the Legislative Reference Library. Digital copies created by the Texas State Library and Archives Commission with grant funding provided by the Library Services and Technology Act, Institute of Museum and Library Services, are available through the Texas Digital Archive.</p>
            <p>Commercial use of legislatively produced audio or visual material is limited (<a href="https://statutes.capitol.texas.gov/Docs/GV/htm/GV.306.htm">Texas Government Code, Section 306.006</a>).</p>
            <p>Use the “Show Results in the TDA” button to search all text for a recording in the TDA.</p>
            <p></p>
        </div>
        <p>
            <script>
                {some_javascript}
            </script>
            <script>
                {some_javascript2}    
            </script>
        </p>
    </body>
</html>
"""
with open(search_page, "w") as w:
    w.write(new_text)
w.close()