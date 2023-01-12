import lxml.etree as ET
import sys
import os
import pandas as PD

namespaces = {'dcterms': "http://dublincore.org/documents/dcmi-terms/",
              'tslac': "https://www.tsl.texas.gov/"}

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

def optionGenerator(something, extra_attributes=list):
    attrib_counter = 0
    attrib_string = ""
    for extra_attribute in extra_attributes:
        attrib_counter += 1
        extra = ""
        extra_name = f"extra{str(attrib_counter)}"
        extra_attribute = reduceDupe(extra_attribute)
        for item in extra_attribute:
            extra += item + "|"
        extra = extra[:-1]
        attrib_string += f' {extra_name}="{extra}"'
    stringy = f'\t<option value="{something}"{attrib_string}>{something}</option>\n'
    return stringy


metadata = input("directory to crawl for data: ")
data = []
for dirpath, dirnames, filenames in os.walk(metadata):
    for filename in filenames:
        if filename.startswith("IO_") and "metadata" in filename:
            filename = os.path.join(dirpath, filename)
            with open(filename, "r") as r:
                filedata = r.read()
                if "<dcterms:dcterms" in filedata:
                    print(filename)
                    if "v6.0" in filedata:
                        version = "v6.0"
                    if "v6.1" in filedata:
                        version = "v6.1"
                    if "v6.2" in filedata:
                        version = "v6.2"
                    if "v6.3" in filedata:
                        version = "v6.3"
                    if "v6.4" in filedata:
                        version = "v6.4"
                    if "v6.5" in filedata:
                        version = "v6.5"
                    if "v6.6" in filedata:
                        version = "v6.6"
                    namespaces['MetadataResponse'] = f"http://preservica.com/EntityAPI/{version}"
                    namespaces['xip'] = f"http://preservica.com/XIP/{version}"
                    try:
                        dom = ET.parse(filename)
                        root = dom.getroot()
                        something = dom.find(".//tslac:militaryDept.organization", namespaces=namespaces).text
                        collection = root.xpath("//dcterms:relation.isPartOf", namespaces=namespaces)
                        collectionText = ""
                        for i in collection:
                            collectionText += i.text + "|"
                        collectionText = collectionText[:-1]
                        commander = root.xpath("//dcterms:subject", namespaces=namespaces)
                        commanderText = ""
                        unitText = ""
                        for i in commander:
                            ernie = i.text
                            if "Army" not in ernie and "Militia" not in ernie:
                                commanderText += ernie + "|"
                            if "Army" in ernie or 'Militia' in ernie:
                                unitText += ernie + "|"
                        commanderText = commanderText[:-1]
                        unitText = unitText[:-1]
                        if "|" in commanderText:
                            commander_list = commanderText.split("|")
                            for item in commander_list:
                                data.append([something, collectionText, item, unitText])
                        elif "|" in unitText:
                            unit_list = unitText.split("|")
                            for item in unit_list:
                                data.append([something, collectionText, commanderText, item])
                        else:
                            data.append([something,collectionText,commanderText,unitText])
                    except:
                        continue
df = PD.DataFrame(data, columns=['Organization', 'Collection', 'Commander', 'Unit'])
#df = df.drop_duplicates()
writer = df.to_csv(metadata + "/table.csv", index=False)
print("finished compiling data for processing, data saved")
print("starting to compile search page")
organization = ""
collection = ""
commander = ""
unit = ""
organizationList = df['Organization'].tolist()
organizationList = set(organizationList)
organizationList = list(organizationList)
organizationList.sort()
for item in organizationList:
    df2 = df.loc[df['Organization'] == item]
    setList1 = set()
    for index, row in df2.iterrows():
        setList1.add(row['Collection'])
    organization += optionGenerator(item, [setList1])
organization = organization.replace("extra1", "colname")
setList1 = ""
commanderList = df['Commander'].tolist()
commanderList = set(commanderList)
commanderList = list(commanderList)
commanderList.sort()
for item in commanderList:
    if item != "":
        df2 = df.loc[df['Commander'] == item]
        setList1 = set()
        setList2 = set()
        setList3 = set()
        for index, row in df2.iterrows():
            setList1.add(row['Collection'])
            setList2.add(row['Organization'])
            setList3.add(row['Unit'])
        commander += optionGenerator(item, [setList1, setList2, setList3])
commander = commander.replace("extra1", "colname")
commander = commander.replace("extra2", "militaryorganization")
commander = commander.replace("extra3", "unit")
setList1 = ""
setList2 = ""
setList3 = ""
unitList = df['Unit'].tolist()
unitList = set(unitList)
unitList = list(unitList)
unitList.sort()
for item in unitList:
    if item != "":
        df2 = df.loc[df['Unit'] == item]
        setList1 = set()
        setList2 = set()
        setList3 = set()
        for index, row in df2.iterrows():
            setList1.add(row['Collection'])
            setList2.add(row['Commander'])
            setList3.add(row['Organization'])
        unit += optionGenerator(item, [setList1, setList2, setList3])
unit = unit.replace("extra1", "colname")
unit = unit.replace("extra2", "commander")
unit = unit.replace("extra3", "militaryorganization")


catan = f'''<html>
    <h1 class="new-primary page-title">Military Rolls Custom Search</h1>
    <div class="at-above-post-page addthis_tool" data-url="https://tsl.access.preservica.com/tda/reference-tools/militaryrollsearch/"></div>
    <div class="container">
        <h2 class="tdaSearch_search_title"><strong>Military Rolls Custom Search</strong></h2>
    </div>
    <p class="tdaSearch_link2" style="text-align:center">
        <a href="https://tsl.access.preservica.com/uncategorized/SO_de947210-c2ed-42a2-8b6b-dbcb1ed8ad3a/">Browse the military rolls</a>
    </p>
    <p>
        <a href="#aboutme">About military rolls</a> | <a href="#confed">About Confederate and Texas State Troops Military Rolls</a>
    </p>
    <div align="center" class="tdaSearch_search_container">
        <div align="left" class="tdaSearch_search_warning">
            <p>For best results, start searches as broad as possible (one field). <a href="#tdaSearchHelp">Click here</a> for more information on how to use this search tool. These drop-down searches have known issues with some versions of Internet Explorer. We recommend using Mozilla Firefox, Google Chrome or Microsoft Edge for complete functionality.</p>
        </div>
        <div class="tdaSearch_search_box">
            <div class="tdaSearch_search_form_left">
                <form name="searchform" onsubmit="return dosearch();">
                    <input id="url" type="hidden" value="https://tsl.access.preservica.com/" /> 
                    <input id="root" type="hidden" value="?s=" />
                    <div class="tdaSearch_thing1">
                        <h3>Collection<br />
                            <select id="collections" onchange="return changeable1()">
                                <option value="">Select a collection</option>
                                <option value="SO_798a5331-558c-458d-8b90-5962965c378b">Texas Adjutant General&#39;s Department Civil War military rolls</option> 
                            </select>
                        </h3>
                    </div>
                    <div class="tdaSearch_thing1">
                        <h3>Military Organization<span id="mo_notice" style="display:none"> *options updated</span><br />
                            <select id="mo" onchange="return changeable2()">
                                <option value="">Select an organization</option>
                                {organization}
                            </select>
                        </h3>
                    </div>
                    <div class="tdaSearch_thing1">
                        <h3>Commander<span id="commander_notice" style="display:none"> *options updated</span><br />
                            <select id="commander" onchange="return changeable3()">
                                <option checked="checked" value="">Select a commander name</option>
                                {commander}
                            </select>
                        </h3>
                    </div>
                    <div class="tdaSearch_thing1">
                        <h3>Unit<span id="unit_notice" style="display:none"> *options updated</span><br />
                            <select id="unit" onchange="return changeable4()">
                                <option value="">Select a unit</option>
                                {unit}
                            </select>
                        </h3>
                    </div>'''

settlers = '''		<br/>
					<div class="tdaSearch_thing5">
						<input style="height:2.75em;" type="submit" value="Search the Texas Digital Archive"/>
					</div>
			        <div class="tdaSearch_thing5">
				        <input style="height:2.75em;" type="reset" value="Reset options" onclick="location.reload()"/>
			        </div>
				</form>
			</div>
			<div class="tdaSearch_search_form_right">
				<img alt="Muster Roll 1401" class="tdaSearch_graphic" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2019/02/musterRoll.png" caption="Example Military Roll" title="Example military roll from the Confederate and Texas State Troops military rolls"/>
				<p style="text-align:center" class="tdaSearch_link1">
					<a href="https://tsl.access.preservica.com/uncategorized/SO_de947210-c2ed-42a2-8b6b-dbcb1ed8ad3a/">Browse the military rolls</a>
				</p>
			</div>
		</div>
	</div>
</div>
<div class="tdaSearch_bottom_text">
    <h2 id="tdaSearchHelp">How to Use This Tool</h2>
    <p>This tool prepares a search of the military rolls in the Texas Digital Archive (TDA). Each drop-down menu corresponds to a level of hierarchy within the military department, down to the individual commander. Commander is listed before unit since a commander may have served multiple units. Click on "Search the Texas Digital Archive" to search the TDA using the options you select.</p>
    <p>Individual members of a unit listed on a military roll are not searchable in the TDA. Only information about the Unit and Commander are recorded for each roll. If you do not know the name of the Unit or Commander, see the military roll <a href="https://www.tsl.texas.gov/arc/tda/CivilWarMilitaryRolls">search tips</a> for directions on how to find this information.</p>
    <p>Please also note that this webpage relies on JavaScript. If the webpage does not function you may need to update your browser settings to permit JavaScript.</p>
    <h2 id="aboutme">About Military Rolls</h2>
    <p>Military rolls consist of muster rolls, muster-in rolls, muster-out rolls, muster and payrolls, payrolls, receipt rolls, and other lists of officers and/or men, for the various military and para-military organizations (primarily Rangers and Militia units), of both the Republic and the State of Texas. They date 1835-1915, 1917, 1935, and undated. Except for some of the Republic rolls which were drawn up after the fact, these military rolls were compiled at the time, usually by the company commanders. The information contained on the rolls varies considerably, ranging from mere lists of names to detailed physical descriptions. The search page only covers military rolls that have been digitized and made available on the Texas Digital Archive.</p>
    <h2 id="confed">Confederate and Texas State Troops Military Rolls</h2>
    <p>The Confederate and Texas State Troops military rolls are in the process of being digitized to facilitate public access. As military rolls are scanned, digital images will be made available through the Texas Digital Archive (TDA).<strong> Select a commanding officer from the list above to bring up a TDA page displaying the military rolls associated with that officer.</strong> To view images in greater detail, please download a high resolution version by clicking on the download button.</p>
    <p>Digitized Confederate military rolls can also be browsed or searched through the main TDA page for <a target="_blank" href="https://tsl.access.preservica.com/uncategorized/SO_c0fcfea2-a1bb-4430-ae13-20532637d319/">Confederate and Texas State Troops military rolls</a>. Please note that not all Confederate and Texas State Troops military rolls have been digitized. Further description and a complete inventory of Confederate and Texas State Troops military rolls in our holdings are located in the records' <a target="_blank" href="http://www.lib.utexas.edu/taro/tslac/30073/tsl-30073.html">finding aid</a>.</p>
    <p>A card file indexing these records by individual and by commanding officer is available. See the military roll <a href="https://www.tsl.texas.gov/arc/tda/CivilWarMilitaryRolls">search tips</a> for more information. For additional information concerning this collection or for assistance searching these records for a particular individual, please contact us at <a href="mailto:ref@tsl.texas.gov?subject=Reference%20Question">ref@tsl.texas.gov</a>.</p>
</div>
<script type="text/javascript">
function dosearch() {
	var collection = collections.options [collections.selectedIndex].value;
	var collectible
	if (collection != "") {
		collectible = "&parenthierarchy=" + collection;
	} else {
		collectible = "&parenthierarchy=SO_de947210-c2ed-42a2-8b6b-dbcb1ed8ad3a";
	}
	var org = mo.options [mo.selectedIndex].value;
	var mo1, mo2
	if (org != "") {
		mo1 = "dcterms.military_org/" + org + "|";
		mo2 = "dcterms.military_org/" + org + "|";
	} else {
		mo1 = "";
		mo2 = "";
	}
	var commanders = commander.options [commander.selectedIndex].value;
	var commander1, commander2;
	if (commanders != "") {
		commander1 = "dcterms.dcterms_subject_freetext/" + commanders + "|";
		commander2 = "dcterms.dcterms_subject_freetext/" + commanders + "|";
	} else {
		commander1 = "";
		commander2 = "";
	}
	var units = unit.options [unit.selectedIndex].value;
	var unit1, unit2;
	if (units != "") {
		unit1 = "dcterms.dcterms_subject/" + units + "|";
		unit2 = "dcterms.dcterms_subject/" + units + "|";
	} else {
		unit1 = "";
		unit2 = "";
	}
var sf = document.searchform;
var submitto = sf.url.value 
+ sf.root.value 
+ collectible  
+ "&hh_cmis_filter=" 
+ "xip.content_type_r_Display/document|"
/* or use xip.document_type/SO| to limit to folders only */
+ commander1 
+ unit1 
+ mo1 
+ "&saved_filters=" 
+ mo2 
+ commander2 
window.open(submitto);
return false;
}
function changeable1() {
	var collection1 = collections.options [collections.selectedIndex].innerHTML;
	changeable1a = document.getElementById("mo");
	changeable1a_notice = document.getElementById("mo_notice");
	var changeable1a_arr = [];
	changeable1a_opt = changeable1a.getElementsByTagName("option");
	for (i = 1; i < changeable1a_opt.length; i++) {
		if (changeable1a_opt[i].getAttribute("colName").search(collection1) == -1){
			changeable1a_opt[i].style.display = "none";
			changeable1a_notice.style.display = "";
		} else {
			changeable1a_opt[i].style.display = "";
		}
	}
	changeable1b = document.getElementById("commander");
	changeable1b_notice = document.getElementById("commander_notice");
	var changeable1b_arr = [];
	changeable1b_opt = changeable1b.getElementsByTagName("option");
	for (i = 1; i < changeable1b_opt.length; i++) {
		if (changeable1b_opt[i].getAttribute("colName").search(collection1) == 1){
			changeable1b_opt[i].style.display = "none";
			changeable1b_notice.style.display = "";
		} else {
			changeable1b_opt[i].style.display = "";
		}
	}
	changeable1c = document.getElementById("unit");
	changeable1c_notice = document.getElementById("unit_notice");
	var changeable1c_arr = [];
	changeable1c_opt = changeable1c.getElementsByTagName("option");
	for (i = 1; i < changeable1c_opt.length; i++) {
		if (changeable1c_opt[i].getAttribute("colName").search(collection1) == -1){
			changeable1c_opt[i].style.display = "none";
			changeable1c_notice.style.display = "";
		} else {
			changeable1c_opt[i].style.display = "";
			
		}
	}
}
function changeable2() {
	var mo1 = mo.options [mo.selectedIndex].value;
	changeable2a = document.getElementById("commander");
	changeable2a_notice = document.getElementById("commander_notice");
	var changeable2a_arr = [];
	changeable2a_opt = changeable2a.getElementsByTagName("option");
	for (i = 1; i < changeable2a_opt.length; i++) {
		if (changeable2a_opt[i].getAttribute("militaryOrganization").search(mo1) == -1){
			changeable2a_opt[i].style.display = "none";
			changeable2a_notice.style.display = "";
		} else {
			changeable2a_opt[i].style.display = "";
		}
	}
	changeable2b = document.getElementById("unit");
	changeable2b_notice = document.getElementById("unit_notice");
	var changeable2b_arr = [];
	changeable2b_opt = changeable2b.getElementsByTagName("option");
	for (i = 1; i < changeable2b_opt.length; i++) {
		if (changeable2b_opt[i].getAttribute("militaryOrganization").search(mo1) == -1){
			changeable2b_opt[i].style.display = "none";
			changeable2b_notice.style.display = "";
		} else {
			changeable2b_opt[i].style.display = "";
		}
	}
}
function changeable3() {
	var commander1 = commander.options [commander.selectedIndex].value;
	changeable3a = document.getElementById("unit");
	changeable3a_notice = document.getElementById("unit_notice");
	var changeable3a_arr = [];
	changeable3a_opt = changeable3a.getElementsByTagName("option");
	for (i = 1; i < changeable3a_opt.length; i++) {
		if (changeable3a_opt[i].getAttribute("commander").search(commander1) == -1){
			changeable3a_opt[i].style.display = "none";
			changeable3a_notice.style.display = "";
		} else {
			changeable3a_opt[i].style.display = "";
		}
	}
}
function changeable4() {
	var unit1 = unit.options [unit.selectedIndex].value;
	changeable4a = document.getElementById("commander");
	changeable4a_notice = document.getElementById("commander_notice");
	var changeable4a_arr = [];
	changeable4a_opt = changeable4a.getElementsByTagName("option");
	for (i = 1; i < changeable4a_opt.length; i++) {
		if (changeable4a_opt[i].getAttribute("unit").search(unit1) == -1){
			changeable4a_opt[i].style.display = "none";
			changeable4a_notice.style.display = "";
		} else {
			changeable4a_opt[i].style.display = "";
		}
	}
}
</script>
</html>'''

writer = open(metadata + "/output.html", "w")
writer.write(catan + settlers)
writer.close()