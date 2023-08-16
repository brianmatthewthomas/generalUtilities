import lxml.etree as ET
import sys
import os
import pandas as PD

def reduceDupe(thingy):
    thingy = list(thingy)
    settler = set()
    for item in thingy:
        things = item.split("|")
        for thing in things:
            settler.add(thing)
    settler = list(settler)
    settler.sort()
    return settler

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
    case = row_data['case']
    link = row_data['link']
    oldCase = row_data['oldCase']
    year = row_data['year']
    court = row_data['court']
    county = row_data['county']
    judge = row_data['judge']
    lawyer = row_data['lawyer']
    party = row_data['party']
    cause = row_data['cause']
    row = f'''<tr>
        <td class="drop0">{case}</td>
        <td><a href="https://tsl.access.preservica.com/uncategorized/{link}" target="_blank" title="Link to case file">{case}</a></td>
        <td class="drop4">{oldCase}</td>
        <td>{year}</td>
        <td class="drop3">{court}</td>
        <td>{county}</td>
        <td class="drop2">{judge}</td>
        <td class="drop1">{lawyer}</td>
        <td>{party}</td>
        <td class="drop5">{cause}</td>
    </tr>'''
    return row

empty_dict = {'case':'','link':'','oldCase':"",'year':"",'court':"",'county':"",'judge':"",'lawyer':"",'party':"",'cause':""}
years = set()
countys = set()
courts = set()
judges = set()
dates = set()
causes = set()

metadata = input("directory to crawl for data: ")
data = []
for dirpath, dirnames, filenames in os.walk(metadata):
    for filename in filenames:
        if "metadata" in filename:
            row_dict = empty_dict
            filename_placeholder = filename
            filename = os.path.join(dirpath, filename)
            with open(filename, "r") as r:
                filedata = r.read()
                if "dcterms" in filedata:
                    print("processing", filename)
                    if "EntityAPI/v6.9" in filedata:
                        version = "v6.9"
                    if "EntityAPI/v6.8" in filedata:
                        version = "v6.8"
                    if "EntityAPI/v6.7" in filedata:
                        version = "v6.7"
                    if "EntityAPI/v6.6" in filedata:
                        version = "v6.6"
                    if "EntityAPI/v6.5" in filedata:
                        version = "v6.5"
                    if "EntityAPI/v6.4" in filedata:
                        version = "v6.4"
                    if "EntityAPI/v6.3" in filedata:
                        version = "v6.3"
                    if "EntityAPI/v6.2" in filedata:
                        version = "v6.2"
                    if "EntityAPI/v6.1" in filedata:
                        version = "v6.1"
                    if "EntityAPI/v6.0" in filedata:
                        version = "v6.0"
                    nsmap = {'MetadataResponse': f"http://preservica.com/EntityAPI/{version}",
                             'xip': f"http://preservica.com/XIP/{version}",
                             'dcterms': "http://dublincore.org/documents/dcmi-terms/",
                             'tslac': "https://www.tsl.texas.gov/"}
                    dom = ET.parse(filename)
                    root = dom.getroot()
                    row_dict['link'] = dom.find(".//xip:Entity", namespaces=nsmap).text
                    if filename_placeholder.startswith("IO"):
                        row_dict['link'] = "IO_" + row_dict['link']
                    if filename_placeholder.startswith("SO"):
                        row_dict['link'] = "SO_" + row_dict['link']
                    row_dict['case'] = dom.find(".//dcterms:title", namespaces=nsmap).text
                    row_dict['oldCase'] = dom.find(".//tslac:scotx.oldCaseNumber", namespaces=nsmap).text
                    row_dict['year'] = dom.find(".//tslac:scotx.dateFiled", namespaces=nsmap).text
                    years.add(row_dict['year'][:4])
                    row_dict['court'] = dom.find(".//tslac:scotx.court", namespaces=nsmap).text
                    courts.add(row_dict['court'])
                    row_dict['county'] = dom.find(".//dcterms:coverage.spatial", namespaces=nsmap).text
                    countys.add(row_dict['county'])
                    row_dict['judge'] = dom.find(".//tslac:scotx.presidingJudge", namespaces=nsmap).text
                    tempList = row_dict['judge'].split("; ")
                    for item in tempList:
                        judges.add(item)
                    row_dict['lawyer'] = dom.find(".//tslac:scotx.lawyer", namespaces=nsmap).text
                    myParty = root.xpath(".//tslac:scotx.party", namespaces=nsmap)
                    tempText = ""
                    if myParty != None:
                        for item in myParty:
                            tempText = tempText + item.text + " v. "
                    row_dict['party'] = tempText[:-4]
                    myCause = root.xpath(".//tslac:scotx.causeOfAction", namespaces=nsmap)
                    tempText = ""
                    if myCause != None:
                        for item in myCause:
                            tempText = tempText + item.text + "; "
                            causes.add(item.text)
                    row_dict['cause'] = tempText[:-2]
                    row_text = row_generator(row_dict)
                    data.append(row_text)
filter(None, data)
data.sort()
table_data = ""
for item in data:
    table_data = table_data + item + "\n"
year = optionGenerator(years)
county = optionGenerator(countys)
court = optionGenerator(courts)
cause = optionGenerator(causes)
judge = optionGenerator(judges)
case_script = '''<script>
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
                </script>'''
party_script = '''<script>
                  var tooltip_party_1 = document.getElementById("tooltip_party_1");
                  var tooltip_party = document.getElementById("tooltip_party");
                  var span = document.getElementById("closeify_tooltip_party");
                  tooltip_party.onclick = function() {
                    tooltip_party_1.style.display = "block";
                  }
                  span.onclick = function() {
                    tooltip_party_1.style.display = "none";
                  }
                  window.onclick = function(event) {
                    if (event.target == tooltip_party_1) {
                      tooltip_party_1.style.display = "none";
                    }
                  }
                </script>'''
cause_script = '''<script>
                  var tooltip_cause_1 = document.getElementById("tooltip_cause_1");
                  var tooltip_cause = document.getElementById("tooltip_cause");
                  var span = document.getElementById("closeify_tooltip_cause");
                  tooltip_cause.onclick = function() {
                    tooltip_cause_1.style.display = "block";
                  }
                  span.onclick = function() {
                    tooltip_cause_1.style.display = "none";
                  }
                  window.onclick = function(event) {
                    if (event.target == tooltip_cause_1) {
                      tooltip_cause_1.style.display = "none";
                    }
                  }
                </script>'''
year_script = '''<script>
                  var tooltip_year_1 = document.getElementById("tooltip_year_1");
                  var tooltip_year = document.getElementById("tooltip_year");
                  var span = document.getElementById("closeify_tooltip_year");
                  tooltip_year.onclick = function() {
                    tooltip_year_1.style.display = "block";
                  }
                  span.onclick = function() {
                    tooltip_year_1.style.display = "none";
                  }
                  window.onclick = function(event) {
                    if (event.target == tooltip_year_1) {
                      tooltip_year_1.style.display = "none";
                    }
                  }
                </script>'''
lawyer_script = '''<script>
                  var tooltip_lawyer_1 = document.getElementById("tooltip_lawyer_1");
                  var tooltip_lawyer = document.getElementById("tooltip_lawyer");
                  var span = document.getElementById("closeify_tooltip_lawyer");
                  tooltip_lawyer.onclick = function() {
                    tooltip_lawyer_1.style.display = "block";
                  }
                  span.onclick = function() {
                    tooltip_lawyer_1.style.display = "none";
                  }
                  window.onclick = function(event) {
                    if (event.target == tooltip_lawyer_1) {
                      tooltip_lawyer_1.style.display = "none";
                    }
                  }
                </script>'''
form_text = f'''<form id="form" onchange="master_filter()" onkeyup="master_filter()">
          <div class="tdaSearch_thing1">
            <h3>
              <label for="search_all" class="collapsible">
                <span style="position:relative">Keyword Search</span>
              </label>
              <div class="collapsibleContent">
              <input name="search_all" id="search_all" placeholder="Does not update table below" type="text" class="inputs"/>
              </div>
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3>
              <label for="case_num" class="collapsible">Case Number</label>
              <div class="collapsibleContent"><span style="font-size:0.85em;color: #a91e2f;">Case number must be 5 digits. Use zeros at the beginning if necessary</span><strong id="case_num_note" style="color:purple; display:none;"> *Active filter</strong><br/><select id="case_num_prefix" style="width:100px"><option value="">Prefix</option><option value="M-">M</option></select>
						-
						<input id="case_num" placeholder="Enter a case number" class="inputs" type="text" style="width:200px"/></div></h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3>
              <label for="old_case_num" class="collapsible">Old/Original Case Number </label>
              <img class="tooltip_image" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2020/06/200px-Icon-round-Question_mark.svg_.png" max-width="5px" style="cursor:help" title="Click for more information" id="tooltip_case_number"/>
              <div class="tooltip-test" id="tooltip_case_number_1" style="display:none;">
                <div class="modal-content">
                    <span class="closeify" id="closeify_tooltip_case_number">x</span>
                    <h1 style="text-align: center;">
                        <strong>About Old Case Numbers</strong>
                    </h1>
                    <p style="line-height: 1em; color:black; font-size:0.85em;font-family:auto;">The original case number given before case numbers were standardized in the 1940s.</p>
                </div>
              </div>
                {case_script}
              <strong id="old_case_note" style="color:purple; display:none;"> *Active filter</strong>
              <div class="collapsibleContent">
              <input id="old_case_num" placeholder="Enter an old case number" type="text" class="inputs"/></div>
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3>
              <label for="party" class="collapsible">Parties (Last Name, First Name)  </label>
              <img class="tooltip_image" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2020/06/200px-Icon-round-Question_mark.svg_.png" max-width="5px" style="cursor:help" title="Click for more information" id="tooltip_party"/>
              <div class="tooltip-test" id="tooltip_party_1" style="display: none;">
                  <div class="modal-content">
                    <span class="closeify" id="closeify_tooltip_party">x</span>
                    <h1 style="text-align: center;">
                      <strong>About Parties</strong>
                    </h1>
                    <p style="line-height: 1em;color:black;font-size:0.85em;font-family:auto;">Search by one or both party names. If using both search boxes, a TDA search will return results for either name. For persons, use the convention Lastname, Firstname. If you are unsure of spelling, try name variants or initial. Corporations may be listed by full name or an abbreviation.') alt=Search by one or both party names. If using both search boxes, a TDA search will return results for either name. For persons, use the convention Lastname, Firstname. If you are unsure of spelling, try name variants or initial. Corporations may be listed by full name or an abbreviation.</p>
                   </div>
                </div>
                {party_script}
              <strong id="partynote" style="color:purple; display:none;"> *Active filter</strong>
              <div class="collapsibleContent"><input style="width:250px;" type="text" id="party" placeholder="Enter either party name"/> AND <label for="partyhardy" style="display:none">second party</label><input style="width:250px;" type="text" id="partyhardy" placeholder="Enter either party name"/></div></h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3>
              <label for="cause_drop" class="collapsible">Cause of Action </label>
              <img class="tooltip_image" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2020/06/200px-Icon-round-Question_mark.svg_.png" max-width="5px" style="cursor:help" title="Click for more information" id="tooltip_cause"/>
                <div class="tooltip-test" id="tooltip_cause_1" style="display: none;">
                  <div class="modal-content">
                    <span class="closeify" id="closeify_tooltip_cause">x</span>
                    <h1 style="text-align: center;">
                      <strong>About Cause of Action</strong>
                    </h1>
                    <p style="line-height: 1em;color:black;font-size:0.85em;font-family:auto;">The main cause(s) of the case. Terms are based on legal definitions.</p>
                  </div>
                </div>
                {cause_script}
              <strong id="causenote" style="color:purple; display:none;"> *Active filter</strong>
              <div class="collapsibleContent">
              <select id="cause_drop">
                <option value="" selected="selected">Select cause of action</option>
                {cause}
              </select>
              </div>
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3>
              <label for="date_drop" class="collapsible">Year Filed with Supreme Court </label>
              <img class="tooltip_image" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2020/06/200px-Icon-round-Question_mark.svg_.png" max-width="5px" style="cursor:help" title="Click for more information" id="tooltip_year"/>
                <div class="tooltip-test" id="tooltip_year_1" style="display: none;">
                  <div class="modal-content">
                    <span class="closeify" id="closeify_tooltip_year">x</span>
                    <h1 style="text-align: center;">
                      <strong>About Year Filed</strong>
                    </h1>
                    <p style="line-height: 1em;color:black;font-size:0.85em;font-family:auto;">The year filed with the Supreme Court. Original/initial court filings may have occurred in previous years, and the actual case may not have been heard by the Supreme Court in the same year that it was filed.</p>
                  </div>
                </div>
                {year_script}
              <strong id="datenote" style="color:purple; display:none;"> *Active filter</strong>
              <div class="collapsibleContent">
              <select id="date_drop">
                <option value="">Select year</option>
                {year}
              </select>
              </div>
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3>
              <label for="court_drop" class="collapsible">Court Jurisdiction </label><strong id="courtnote" style="color:purple; display:none;"> *Active filter</strong>
              <div class="collapsibleContent">
              <select id="court_drop">
                <option value="" selected="selected">Select court jurisdiction</option>
                {court}
              </select>
              </div>
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3>
              <label for="county_drop" class="collapsible">County of Origin </label><strong id="countynote" style="color:purple; display:none;"> *Active filter</strong>
              <div class="collapsibleContent">
              <select id="county_drop">
                <option value="" selected="selected">Select county</option>
                {county}
              </select>
              </div>
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3>
              <label for="judge" class="collapsible">District Court Judge </label><strong id="judgenote" style="color:purple; display:none;"> *Active filter</strong>
              <div class="collapsibleContent">
              <select id="judge">
                <option value="">Select a presiding judge</option>
                {judge}
              </select>
              </div>
            </h3>
          </div>
          <div class="tdaSearch_thing1">
            <h3>
              <label for="lawyer" class="collapsible">Attorney/Lawyer Last Name 
              </label><strong id="lawyernote" style="color:purple; display:none;"> *Active filter</strong>
              <img class="tooltip_image" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2020/06/200px-Icon-round-Question_mark.svg_.png" max-width="5px" style="cursor:help" title="Clock for more information" id="tooltip_lawyer"/>
                <div class="tooltip-test" id="tooltip_lawyer_1" style="display: none;">
                  <div class="modal-content">
                    <span class="closeify" id="closeify_tooltip_lawyer">x</span>
                    <h1 style="text-align: center;">
                      <strong>About Lawyer Names</strong>
                    </h1>
                    <p style="line-height: 1em;color:black;font-size:0.85em;font-family:auto;">Search by plaintiff or defendant attorneys, last names only. If you are unsure of spelling, try name variants. State of Texas cases use Attorney General instead of individual attorney names.</p>
                  </div>
                </div>
                {lawyer_script}
              <div class="collapsibleContent">
              <input type="text" id="lawyer" placeholder="Enter a lawyer name" class="inputs"/>
              </div>
            </h3>
          </div>
          <div id="NullResultsMessage" style="display:none;border:5px outset #a91d2f;background-color:lightgrey;text-align:center;border-radius:10px;">
            <p><span class="message" style="font-weight:bold;color:#a91d2f;font-size:2em;">Warning:</span><br/><br/>No matching results. Update your selections from the options above or click on reset to start over.</p>
          </div>
          <br/>
          <div class="tdaSearch_thing5">
            <input onClick="location.reload()" style="height:2.75em;" type="reset" value="Reset options"/>
          </div>
        </form>
'''

table_text = f'''<table style="border: 3px solid black;padding: 0px" id="scotx">
      <tr style="background-color:lightgray;border-bottom:3px solid black;padding: 0px" class="silly">
        <td class="drop0" />
        <td>Case No.</td>
        <td class="drop4">Old Case No.</td>
        <td>Date filed</td>
        <td class="drop3">Court</td>
        <td>County</td>
        <td class="drop2">Presiding Judge</td>
        <td class="drop1">Lawyer</td>
        <td>Parties</td>
        <td class="drop5">Cause of Action</td>
      </tr>\n
      {table_data}\n
    </table>'''

output = metadata + "output.html"
with open(output, "w") as w:
    w.write(form_text + "\n\n\n" + table_text)
w.close()