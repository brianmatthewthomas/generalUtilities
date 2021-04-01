import lxml.etree as ET
import sys
import os
import pandas as PD

namespaces = {'MetadataResponse': "http://preservica.com/EntityAPI/v6.0",
              'xip': "http://preservica.com/XIP/v6.0",
              'dcterms': "http://dublincore.org/documents/dcmi-terms/",
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

def optionGenerator(something, extraAttribute1, extraAttribute2):
    extraAttribute1 = reduceDupe(extraAttribute1)
    extra1 = ""
    for item in extraAttribute1:
        extra1 += item + "|"
    extra1 = extra1[:-1]
    extra2 = ""
    extraAttribute2 = reduceDupe(extraAttribute2)
    for item in extraAttribute2:
        extra2 += item + "|"
    extra2 = extra2[:-1]
    stringy = f'\t<option value="{something}" extraAttribute1="{extra1}" extraAttribute2="{extra2}">{something}</option>\n'
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
                    try:
                        dom = ET.parse(filename)
                        root = dom.getroot()
                        something = dom.find(".//tslac:txdot.district", namespaces=namespaces).text
                        county = root.xpath("//dcterms:coverage.spatial", namespaces=namespaces)
                        countyText = ""
                        for i in county:
                            countyText += i.text + "|"
                        countyText = countyText[:-1]
                        conveyance = root.xpath("//tslac:txdot.conveyanceType", namespaces=namespaces)
                        conveyanceText = ""
                        for i in conveyance:
                            conveyanceText += i.text + "|"
                        conveyanceText = conveyanceText[:-1]
                        data.append([something,countyText,conveyanceText])
                    except:
                        continue
df = PD.DataFrame(data, columns=['District', 'County', 'Conveyance'])
df = df.drop_duplicates()
writer = df.to_csv(metadata + "/table.csv", index=False)
print("finished compiling data for processing, data save")
print("starting to compile search page")
district = ""
county = ""
conveyance = ""
districtList = df['District'].tolist()
districtList = set(districtList)
districtList = list(districtList)
districtList.sort()
for item in districtList:
    df2 = df.loc[df['District'] == item]
    setList1 = set()
    setList2 = set()
    for index, row in df2.iterrows():
        setList1.add(row['County'])
        setList2.add(row['Conveyance'])
    district += optionGenerator(item, setList1, setList2)
district = district.replace("extraAttribute1", "county")
district = district.replace("extraAttribute2", "conveyance")
setList1 = ""
setList2 = ""
countyList = df['County'].tolist()
countyList = set(countyList)
countyList = list(countyList)
countyList.sort()
for item in countyList:
    if item != "":
        df2 = df.loc[df['County'] == item]
        setList1 = set()
        setList2 = set()
        for index, row in df2.iterrows():
            setList1.add(row['District'])
            setList2.add(row['Conveyance'])
        county += optionGenerator(item, setList1, setList2)
county = county.replace("extraAttribute1", "district")
county = county.replace("extraAttribute2", "conveyance")
county = county.replace(" County (Tex.)</","</")
setList1 = ""
setList2 = ""
conveyanceList = df['Conveyance'].tolist()
conveyanceList = set(conveyanceList)
conveyanceList = list(conveyanceList)
conveyanceList.sort()
for item in conveyanceList:
    if item != "":
        df2 = df.loc[df['Conveyance'] == item]
        setList1 = set()
        setList2 = set()
        for index, row in df2.iterrows():
            setList1.add(row['District'])
            setList2.add(row['County'])
        conveyance += optionGenerator(item, setList1, setList2)
conveyance = conveyance.replace("extraAttribute1", "district")
conveyance = conveyance.replace("extraAttribute2", "county")

catan = f'''<html>
	<body>
    <div style="width: 100%">
		<div width="100%" class="container">
			<h2 class="tdaSearch_search_title">
				<strong>Texas Department of Transportation<br/>Right of Way Custom Search</strong>
			</h2>
		</div>
		<p class="tdaSearch_link2" style="text-align:center">
			<a href="https://tsl.access.preservica.com/uncategorized/SO_735ef8cc-f549-4743-a401-e84b13595b06/">Browse the Right of Way records</a>
		</p>
		<p>
			<a href="#about">About Right of Way records</a>
		</p>
		<div align="center" class="tdaSearch_search_container">
			<div align="left" class="tdaSearch_search_warning">
				<p>For best results, start searches as broad as possible (one field). <a href="#tdaSearchHelp">Click here</a> for more information on how to use this search tool.  These drop-down searches have known issues with some versions of Internet Explorer. We recommend using Mozilla Firefox, Google Chrome or Microsoft Edge for complete functionality.</p>
			</div>
			
      <div class="tdaSearch_search_box">
        <div class="tdaSearch_search_form_left">
		
          <form name="searchform" onSubmit="return dosearch();">
            <div class="tdaSearch_thing1">
              <h3>
				  <label for="district_drop">District</label>
				  <span style="color:#a91d2f; display:none;" id="district_updated">*options updated</span>
				  <span style="color:purple; display:none;" id="district_note">*Active filter</span>
				  <br/>
					<select id="district_drop" class="inputs" onchange="return changeable1();">
						<option value="">Select District</option>
						{district}
					</select>
				</h3>
            </div>
			<div class="tdaSearch_thing1">
				<h3>
					<label for="date">Date(s)</label>
					<br>
					<span style="font-size:.75em">Between </span><input class="inputs" id="date1" placeholder="YYYY-MM-DD" type="text" style="max-width:150px"><span style="font-size:.75em"> AND </span>
					<input class="inputs" id="date2" placeholder="YYYY-MM-DD" type="text" style="max-width:150px">
					<strong id="date_note" style="color:purple; display:none;">Active filter</strong>
				</h3>
			</div>
			<div class="tdaSearch_thing1">
				<h3>
					<label for="hwy">Highway</label>
					<strong style="color:purple; display:none;" id="hwy_note"> *Active filter</strong>
					<br/>
					<input type="text" placeholder="Enter a highway name" name="hwy" id="hwy" class="inputs"/>
				</h3>
			</div>
			<div class="tdaSearch_thing1">
				<h3>
					<label for="county_drop">County</label>
					<span style="color:#a91d2f; display:none;" id="county_updated"> *options updated</span>
					<span style="color:#a91d2f; display:none;" id="county_note"> *Active filter</span>
					<br/>
					<select class="inputs" id="county_drop" onchange="return changeable2();">
						<option value="">Select county</option>
						{county}
					</select>
				</h3>
			</div>
			<div class="tdaSearch_thing1">
				<h3>
					<label for="conveyance_drop">Conveyance type</label>
					<span style="color:#a91d2f; display:none;" id="conveyance_updated"> *options updated</span>
					<span style="color:#a91d2f; display:none;" id="conveyance_note"> *Active filter</span>
					<br/>
					<select class="inputs" id="conveyance_drop" onchange="return changeable3();">
						<option value="">Select conveyance type</option>
						{conveyance}
					</select>
				</h3>
			</div>'''
settlers = '''
			<div class="tdaSearch_thing1">
				<h3>
					<label for="search_all">Other search term</label>
					<strong style="color:purple; display:none;" id="search_all_note"> *Active filter</strong>
					<br/>
					<input type="text" placeholder="Enter other search terms" name="search_all" id="search_all" class="inputs"/>
				</h3>
			</div>
            <br/>
            <div class="tdaSearch_thing5">
              <input style="height:2.75em;" type="submit" value="Search the Texas Digital Archive"/>
            </div>
            <div class="tdaSearch_thing5">
              <input style="height:2.75em;" type="reset" value="Reset options" onclick="location.reload()"/>
            </div>
          </form>
		  
			</div>
			<div class="tdaSearch_search_form_right">
				<img alt="District Boundary map courtesy of Texas Department of Transportation site" class="tdaSearch_graphic" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2021/03/texas.jpg" title="District Boundary map courtesy of Texas Department of Transportation site"/>
				<p class="tdaSearch_link1" style="text-align:center">
					<a href="https://tsl.access.preservica.com/uncategorized/SO_735ef8cc-f549-4743-a401-e84b13595b06/">Browse the Right of Way records</a>
				</p>
			</div>
		</div>
	</div>
</div>
<div class="tdaSearch_bottom_text">
	<h2 id="tdaSearchHelp">How to Use This Tool</h2>
	<p>This tool prepares a search of the historic Right of Way Division records of the Texas Department of Transportation in the Texas Digital Archive (TDA). Click on "Search the Texas Digital Archive" to search the TDA using the options you select.</p>
	<p>The records are divided by District and are actively being digitized on a district-by-district basis. Occasionally records are found filed within one district but meant to be included in another district. Due to the volume of records involved, the options in this search tool will only be updated when a district is most likely complete. For the most recent visual representation of the current district names and boundaries, go to <a href="https://www.txdot.gov/inside-txdot/district.html" target="_blank">https://www.txdot.gov/inside-txdot/district.html</a>.</p>
	<p>Selecting a specific district will limit results to just that district and district boundaries may have changed over time. Highway names are based on how they are listed in the record, which can change over time relative to the current name of the roadway. It is recommended that users search use multiple searches with variations of potential highway names if attempting to locate a record by highway.</p>
	<h2 id="aboutme">About the Right of Way Division records</h2>
	<p>These records include conveyances, maps, and titles for property owned by the Texas Department of Transportation (TxDOT) Right of Way Division. The Right of Way Division coordinates the acquisition of land to build, widen, or enhance highways and provides relocation assistance when needed. The division also coordinates utility adjustments, and the disposition and leasing of surplus real property owned by TxDOT. The records document these land transfers and date from 1924 to 2017, and some records are undated. The records are part of an ongoing digitization project by TxDOT that began with the Austin District; the project will continue with other major-municipality districts and finish with the less populous ones. Records within a district are organized by a CCSJ or RCSJ identifier. Each document within a CCSJ/RCSJ is numbered based on the order in which it was digitized; the number assigned to a document <em>is not</em> a Department of Transportation identifier. A district is usually spread across several counties but may not encompass all of a county. County borders can shift over time and counties listed for a document are based on the county boundaries at the time the record was created.</p>
	<p>See the <a href="http://www.lib.utexas.edu/taro/tslac/13003/tsl-13003.html" target="_blank">finding aid</a> for more information about the Right of Way Division records.</p>
</div>
  <script type="text/javascript">
function dosearch() {
	var collection = district_drop.options [district_drop.selectedIndex].value;
	var collectible
	if (collection != "") {
        if (collection == "AUS") {
            collectible = "&parenthierarchy=SO_4ec205fa-8f6a-47c7-a960-20cf4ca18420"
        } else if (collection == "HOU") {
            collectible = "&parenthierarchy=SO_0af33ec4-9d28-44d2-ae5d-8f4d9eead18c"
        }
    } else {
        collectible = "&parenthierarchy=SO_735ef8cc-f549-4743-a401-e84b13595b06"
    }
    var dately = date1.value;
    var datelier = date2.value
    var dateA, dateB, date_note;
    if (dately != "") {
        dateA = "dcterms.dcterms_date/" + dately + "%20-%20" + datelier + "|";
        dateB = "dcterms.dcterms_date/" + dately + "%20-%20" + datelier + "|";
    } else {
        dateA = "";
        dateB = "";
    }
	var counties = county_drop.options [county_drop.selectedIndex].value; 
	var county1, county2
	if (counties != "") {
		county1 = "dcterms.dcterms_geographic/" + counties + "|";
		county2 = "dcterms.dcterms_geographic/" + counties + "|";
	} else {
		county1 = "";
		county2 = "";
	}
	var highway = hwy.value;
	var highway1, highway2
	if (highway != "") {
		highway1 = "dcterms.txdot_hwy/" + highway + "|";
		highway2 = "dcterms.txdot_hwy/" + highway + "|";
	} else {
		highway1 = "";
		highway2 = "";
	}
	var conveyances = conveyance_drop.options [conveyance_drop.selectedIndex].value;
	var conveyance1, conveyance2
	if (conveyances != "") {
		conveyance1 = "dcterms.txdot_conveyance/" + conveyances + "|";
		conveyance2 = "dcterms.txdot_conveyance/" + conveyances + "|";
	} else {
		conveyance1 = "";
		conveyance2 = "";
	}
	
var sf = document.searchform;
var submitto = "https://tsl.access.preservica.com/?s=" 
+ search_all.value 
+ collectible  
+ "&hh_cmis_filter=" 
+ dateA 
+ highway1 
+ conveyance1 
+ county1 
+ "&saved_filters=" 
+ dateB 
+ highway2 
+ conveyance2
window.open(submitto);
return false;
}
function changeable1() {
	var district1 = district_drop.options [district_drop.selectedIndex].innerHTML;
	changeable1a = document.getElementById("county_drop");
	changeable1a_notice = document.getElementById("county_updated");
	var changeable1a_arr = [];
	changeable1a_opt = changeable1a.getElementsByTagName("option");
	for (i = 1; i < changeable1a_opt.length; i++) {
		if (changeable1a_opt[i].getAttribute("district").search(district1) == -1){
			changeable1a_opt[i].style.display = "none";
			changeable1a_notice.style.display = "";
		} else {
			changeable1a_opt[i].style.display = "";
		}
	}
	changeable1b = document.getElementById("conveyance_drop");
	changeable1b_notice = document.getElementById("conveyance_updated");
	var changeable1b_arr = [];
	changeable1b_opt = changeable1b.getElementsByTagName("option");
	for (i = 1; i < changeable1b_opt.length; i++) {
		if (changeable1b_opt[i].getAttribute("district").search(district1) == -1){
			changeable1b_opt[i].style.display = "none";
			changeable1b_notice.style.display = "";
		} else {
			changeable1b_opt[i].style.display = "";
		}
	}
}
function changeable2() {
	var county1 = county_drop.options [county_drop.selectedIndex].innerHTML;
	changeable2a = document.getElementById("district_drop");
	changeable2a_notice = document.getElementById("district_updated");
	var changeable2a_arr = [];
	changeable2a_opt = changeable2a.getElementsByTagName("option");
	for (i = 1; i < changeable2a_opt.length; i++) {
		if (changeable2a_opt[i].getAttribute("county").search(county1) == -1){
			changeable2a_opt[i].style.display = "none";
			changeable2a_notice.style.display = "";
		} else {
			changeable2a_opt[i].style.display = "";
		}
	}
	changeable2b = document.getElementById("conveyance_drop");
	changeable2b_notice = document.getElementById("conveyance_updated");
	var changeable2b_arr = [];
	changeable2b_opt = changeable2b.getElementsByTagName("option");
	for (i = 1; i < changeable2b_opt.length; i++) {
		if (changeable2b_opt[i].getAttribute("county").search(county1) == -1){
			changeable2b_opt[i].style.display = "none";
			changeable2b_notice.style.display = "";
		} else {
			changeable2b_opt[i].style.display = "";
		}
	}
}
function changeable3() {
	var conveyance1 = conveyance_drop.options [conveyance_drop.selectedIndex].value;
	changeable3a = document.getElementById("district_drop");
	changeable3a_notice = document.getElementById("district_updated");
	var changeable3a_arr = [];
	changeable3a_opt = changeable3a.getElementsByTagName("option");
	for (i = 1; i < changeable3a_opt.length; i++) {
		if (changeable3a_opt[i].getAttribute("conveyance").search(conveyance1) == -1){
			changeable3a_opt[i].style.display = "none";
			changeable3a_notice.style.display = "";
		} else {
			changeable3a_opt[i].style.display = "";
		}
	}
	changeable3b = document.getElementById("county_drop");
	changeable3b_notice = document.getElementById("county_updated");
	var changeable3b_arr = [];
	changeable3b_opt = changeable3b.getElementsByTagName("option");
	for (i = 1; i < changeable3b_opt.length; i++) {
		if (changeable3b_opt[i].getAttribute("conveyance").search(conveyance1) == -1){
			changeable3b_opt[i].style.display = "none";
			changeable3b_notice.style.display = "";
		} else {
			changeable3b_opt[i].style.display = "";
		}
	}
}
</script>
</html>'''

writer = open(metadata + "/output.html", "w")
writer.write(catan + settlers)
writer.close()