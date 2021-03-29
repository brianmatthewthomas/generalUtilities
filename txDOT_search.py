import lxml.etree as ET
import sys
import os

namespaces = {'MetadataResponse': "http://preservica.com/EntityAPI/v6.0",
              'xip': "http://preservica.com/XIP/v6.0",
              'dcterms': "http://dublincore.org/documents/dcmi-terms/",
              'tslac': "https://www.tsl.texas.gov/"}


def optionGenerator(something):
    something = list(something)
    something.sort()
    stringy = ""
    for item in something:
        stringy += f'<option value="{item}">{item}</option>\n'
    return stringy


theFile = input("file to transform: ")
with open(theFile, "r") as r:
    filedata = r.read()
    filedata = filedata.replace('</MetadataResponse>\n<?xml version="1.0" encoding="UTF-8" standalone="yes"?><MetadataResponse xmlns="http://preservica.com/EntityAPI/v6.2" xmlns:xip="http://preservica.com/XIP/v6.2">',"")
with open(theFile, "w") as w:
    w.write(filedata)
w.close()
dom = ET.parse(theFile)
root = dom.getroot()
something = root.xpath("//tslac:txdot.district", namespaces=namespaces)
settler = set()
for i in something:
    myText = i.text
    settler.add(i)
district = optionGenerator(settler)
something = root.xpath("//dcterms:coverage.spatial", namespaces=namespaces)
settler2 = set()
for i in something:
    myText = i.text
    settler2.add(i)
county = optionGenerator(settler2)
county = county.replace('County (Tex.)</', '</')
something = root.xpath("//tslac:txdot.conveyanceType", namespaces=namespaces)
settler3 = set()
for i in something:
    myText = i.text
    settler3.add(i)
conveyance = optionGenerator(settler3)

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
				<div class="tdaSearch_search_form_left" id="tdaSearch_search_form_left_senate">
<form id="form" name="form" onchange="master_filter();" onkeyup="master_filter();">
	<div class="tdaSearch_thing1">
		<h3>
			<label for="district_drop">District</label>
			<span style="color#a91d2f; display:none;" id="district_updated"> *options updated</span>
			<strong style="color:purple; display:none;" id="district_note"> *Active filter</strong>
			<br/>
			<select class="inputs" id="district_drop" onchange="return changeable1();">
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
								<input type="text" placeholder="Enter a highway name" id="hwy" class="inputs"/>
							</h3>
						</div>
						<div class="tdaSearch_thing1">
							<h3>
								<label for="grantor">Grantor information</label>
								<strong style="color:purple; display:none;" id="grantor_note"> *Active filter</strong>
								<br/>
								<input type="text" placeholder="Enter a name" id="grantor" class="inputs"/>
							</h3>
						</div>
						<div class="tdaSearch_thing1">
							<h3>
								<label for="county_drop">County</label>
								<span style="color#a91d2f; display:none;" id="county_updated"> *options updated</span>
								<strong style="color:purple; display:none;" id="county_note"> *Active filter</strong>
								<br/>
								<select class="inputs" id="county_drop">
									<option value="">Select county</option>
									{county}
								</select>
							</h3>
						</div>
						<div class="tdaSearch_thing1">
							<h3>
								<label for="conveyance_drop">Conveyance type</label>
								<strong style="color:purple; display:none;" id="date_note"> *Active filter</strong>
								<br/>
								<select class="inputs" id="conveyance_drop">
									<option value="">Select conveyance type</option>
									{conveyance}
								</select>
							</h3>
						</div>
					<br/>
					<div class="tdaSearch_thing5">
						<input style="height:2.75em;" type="submit" value="Search the Texas Digital Archive"/>
					</div>
					<div class="tdaSearch_thing5">
						<input onClick="location.reload()" style="height:2.75em;" type="reset" value="Reset options"/>
					</div>
				</form>
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
function dosearch() '''
settlers = '''{
	var district = district_drop.option[district_drop.selectedIndex].value;
    var district1
    if (district != "") {
        if (district == "AUS") {
            district1 = "&parenthierarchy=SO_4ec205fa-8f6a-47c7-a960-20cf4ca18420"
        } elif (district == "HOU") {
            district1 = "&parenthierarchy=SO_0af33ec4-9d28-44d2-ae5d-8f4d9eead18c"
        }
    } else {
        district1 = "&amp;parenthierarchy=SO_735ef8cc-f549-4743-a401-e84b13595b06"
    }
    var dately = date1.value;
    var datelier = date2.value
    var dateA, dateB, date_note;
    if (dately != "") {
        dateA = "dcterms.dcterms_date/" + dately + "%20-%20" + datelier + "|";
        dateB = "dcterms.dcterms_date/" + dately + "%20-%20" + datelier + "|";
        date_note = document.getElementById("date_note").style.display = "inline";
    } else {
        dateA = "";
        dateB = "";
        date_note = document.getElementById("date_note").style.display = "none";
    }

    var cities = city.options[city.selectedIndex].value;
    var city1, city2;
    if (cities != "") {
        city1 = "dcterms.dcterms_geographic/" + cities + "|";
        city2 = "dcterms.dcterms_geographic/" + cities + "|";
    } else {
        city1 = "";
        city2 = "";
    }
    var counties = county.options[county.selectedIndex].value;
    var county1, county2
    if (counties != "") {
        county1 = "dcterms.dcterms_geographic/" + counties + "|";
        county2 = "dcterms.dcterms_geographic/" + counties + "|";
    } else {
        county1 = "";
        county2 = "";
    }
    var creators = creator.options[creator.selectedIndex].value;
    var creator1, creator2;
    if (creators != "") {
        creator1 = "dcterms.dcterms_creator/" + creators + "|";
        creator2 = "dcterms.dcterms_creator/" + creators + "|";
    } else {
        creator1 = "";
        creator2 = "";
    }
    var types = type.options[type.selectedIndex].value;
    var type1, type2;
    if (types != "") {
        type1 = "dcterms.dcterms_type/" + types + "|";
        type2 = "dcterms.dcterms_type/" + types + "|";
    } else {
        type1 = "";
        type2 = "";
    }
    var sf = document.searchform;
    var submitto = sf.url.value
           + sf.root.value
           + district1
           + "&hh_cmis_filter="
           + dateA
           + county1
           + creator1
           + type1
           + "&saved_filters="
           + dateB
    window.open(submitto);
    return false;
}

function changeable1() {
    var district1 = district.options[district.selectedIndex];
    changeable1a = document.getElementById("county");
    changeable1a_notice = document.getElementById("county_notice");
    var changeable1a_arr = [];
    changeable1a_opt = changeable1a.getElementsByTagName("option");
    for (i = 1; i < changeable1a_opt.length; i++) {
        if (changeable1a_opt[i].getAttribute("district").search(district1) == -1) {
            changeable1a_opt[i].style.display = "none";
            changeable1a_notice.style.display = "";
        } else {
            changeable1a_opt[i].style.display = "";
        }
    }
} 
</script>
</html>'''

writer = open("output.html", "w")
writer.write(catan + settlers)
writer.close()