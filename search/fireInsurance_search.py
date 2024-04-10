import sys
import os
import lxml.etree as ET

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

def optionGenerator(input_dict):
    total_text = ""
    for key in input_dict.keys():
        total_text = f'{total_text}<option value='
        total_text = f'{total_text}"{key}"'
        temp_dict = input_dict[key]
        for more_keys in temp_dict.keys():
            total_text = f'{total_text} {more_keys}='
            temp_text = ""
            temp_list = list(temp_dict[more_keys])
            temp_list.sort()
            for item in temp_list:
                temp_text = f"{temp_text}{item}|"
            while temp_text.endswith("|"):
                temp_text = temp_text[:-1]
            total_text = f'{total_text}"{temp_text}"'
        total_text = f'{total_text}>{key}</option>\n'
    return total_text

# set source data location
to_crawl = '/media/sf_D_DRIVE/harvest/fire_insurance' #input("directory to crawl to create the search page off of: ")
# set-up initial dictionaries for data aggregation
city_dict = dict()
county_dict = dict()
map_type_dict = dict()
creator_dict = dict()
# set up listing for later creation of ordered dictions for option generation
city_sorter = set()
county_sorter = set()
map_type_sorter = set()
creator_sorter = set()

#start the crawl
for dirpath, dirnames, filenames in os.walk(to_crawl):
    for filename in filenames:
        if filename.startswith('IO') and "metadata" in filename:
            filename = os.path.join(dirpath, filename)
            with open(filename, "r") as r:
                filedata = r.read()
                if "dcterms" in filedata:
                    dom = ET.parse(filename)
                    root = dom.getroot()
                    namespaces = getNamespaces(root)
                    # grab needed content
                    cities = root.xpath(".//tslac:map.city", namespaces=namespaces)
                    city_list = []
                    for city in cities:
                        if city.text != "Unknown":
                            city_list.append(f'{city.text} (Tex.)')
                            city_sorter.add(f'{city.text} (Tex.)')
                    counties = root.xpath(".//tslac:map.county", namespaces=namespaces)
                    county_list = []
                    for county in counties:
                        county_list.append(f"{county.text} (Tex.)")
                        county_sorter.add(f'{county.text} (Tex.)')
                    maps = root.xpath(".//dcterms:type", namespaces=namespaces)
                    maps_list = []
                    for map in maps:
                        if map.text != "Image" and map.text != "Maps (documents)":
                            maps_list.append(map.text)
                            map_type_sorter.add(map.text)
                    creators = root.xpath(".//dcterms:creator", namespaces=namespaces)
                    creator_list = []
                    for creator in creators:
                        creator_list.append(creator.text)
                        creator_sorter.add(creator.text)
                    for item in city_list:
                        if item not in city_dict.keys():
                            city_dict[item] = {'county': set(), 'type': set(), 'creator': set()}
                        for x in county_list:
                            city_dict[item]['county'].add(x)
                        for x in maps_list:
                            city_dict[item]['type'].add(x)
                        for x in creator_list:
                            city_dict[item]['creator'].add(x)
                    for item in county_list:
                        if item not in county_dict.keys():
                            county_dict[item] = {'city': set(), 'type': set(), 'creator': set()}
                        for x in city_list:
                            county_dict[item]['city'].add(x)
                        for x in maps_list:
                            county_dict[item]['type'].add(x)
                        for x in creator_list:
                            county_dict[item]['creator'].add(x)
                    for item in maps_list:
                        if item not in map_type_dict.keys():
                            map_type_dict[item] = {'city': set(), 'county': set(), 'creator': set()}
                        for x in city_list:
                            map_type_dict[item]['city'].add(x)
                        for x in county_list:
                            map_type_dict[item]['county'].add(x)
                        for x in creator_list:
                            map_type_dict[item]['creator'].add(x)
                    for item in creator_list:
                        if item not in creator_dict.keys():
                            creator_dict[item] = {'city': set(), 'county': set(), 'type': set()}
                        for x in city_list:
                            creator_dict[item]['city'].add(x)
                        for x in county_list:
                            creator_dict[item]['county'].add(x)
                        for x in maps_list:
                            creator_dict[item]['type'].add(x)
                    print(f'processed {filename}')


print("compiling search page elements")
# make ordered dictionaries for option generation
city_sorter = list(city_sorter)
city_sorter.sort()
city_ordered = dict()
for item in city_sorter:
    city_ordered[item] = city_dict[item]
county_sorter = list(county_sorter)
county_sorter.sort()
county_ordered = dict()
for item in county_sorter:
    county_ordered[item] = county_dict[item]
map_type_sorter = list(map_type_sorter)
map_type_sorter.sort()
map_type_ordered = dict()
for item in map_type_sorter:
    map_type_ordered[item] = map_type_dict[item]
creator_sorter = list(creator_sorter)
creator_sorter.sort()
creator_ordered = dict()
for item in creator_sorter:
    creator_ordered[item] = creator_dict[item]


city_drop = optionGenerator(city_ordered)
print(city_drop)
county_drop = optionGenerator(county_ordered)
print(county_drop)
map_type_drop = optionGenerator(map_type_ordered)
print(map_type_drop)
creator_drop = optionGenerator(creator_ordered)
print(creator_drop)

print("generating search page")

html_head = f'''
		<head>
<link rel="stylesheet" href="./tda_search.css" media="all"/>
</head>
<div style="width:100%">
	<div width="100%" class="container">
		<h2 class="tdaSearch_search_title">
			<strong>Fire Insurance Maps Custom Search</strong>
		</h2>
	</div>
	<p class="tdaSearch_link2" style="text-align:center">
		<a href="https://tsl.access.preservica.com/uncategorized/SO_645f45f1-1197-40a5-b527-28f40db9c5c0/">Browse the fire insurance maps</a>
	</p>
	<p><a href="#aboutme">About fire insurance maps</a></p>
	<div align="center" class="tdaSearch_search_container">
		<div align="left" class="tdaSearch_search_warning">
			<p>For best results, start searches as broad as possible (one field). <a href="#tdaSearchHelp">Click here</a> for more information on how to use this search tool.  These drop-down searches have known issues with some versions of Internet Explorer. We recommend using Mozilla Firefox, Google Chrome or Microsoft Edge for complete functionality.</p>
		</div>
		<div class="tdaSearch_search_box">
			<div class="tdaSearch_search_form_left">
				<form name="searchform" onSubmit="return dosearch();">
					<input id="url" type="hidden" value="https://tsl.access.preservica.com/"/> 
					<input id="root" type="hidden" value="?s="/>
					<div class="tdaSearch_thing1">
						<h3>City or Place<span style="color:#a91d2f; display:none" id="city_notice"> *options updated</span>
							<br/>
							<select id="city" onchange="return changeable1();">
								<option value="" checked="checked">Select a city or place</option>
								{city_drop}
                            </select>
						</h3>
					</div>
					<div class="tdaSearch_thing1">
						<h3>County<span style="color:#a91d2f; display:none" id="county_notice"> *options updated</span>
							<br/>
							<select id="county" onchange="return changeable2();">
								<option value="">Select a county</option>
								{county_drop}
                            </select>
						</h3>
					</div>
					<div class="tdaSearch_thing1">
						<h3>Map type<span style="color:#a91d2f;display:none" id="type_notice"> *options updated</span>
							<br/>
							<select id="type" onchange="return changeable3();">
								<option value="">Select a map type</option>
								{map_type_drop}
                            </select>
						</h3>
					</div>
					<div class="tdaSearch_thing1">
						<h3>Creating entity<span style="color:#a91d2f;display:none" id="creator_notice"> *options updated</span>
							<br/>
							<select id="creator" onchange="return changeable4();">
								<option value="">Select a creator</option>
								{creator_drop}
                            </select>
						</h3>
					</div>
					<div class="tdaSearch_thing1">
						<h3>Map availability
							<br/>
							<span style="color:#2b6da7;"><input name="availability" type="radio" value=""/> All maps <input name="availability" type="radio" value="formatgroup/Document|"/> Maps available online</span>
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
			<div class="tdaSearch_search_form_right">
				<img alt="Amarillo Fire Insurance Map, after 1937" class="tdaSearch_graphic" src="https://tsl.access.preservica.com/wp-content/uploads/sites/10/2020/06/amarilloA.png" title="Amarillo Fire Insurance Map, after 1937"/>
				<p class="tdaSearch_link1" style="text-align:center">
					<a href="https://tsl.access.preservica.com/uncategorized/SO_645f45f1-1197-40a5-b527-28f40db9c5c0/">Browse the fire insurance maps</a>
				</p>
			</div>
		</div>
	</div>
</div>
<div class="tdaSearch_bottom_text">
	<h2 id="tdaSearchHelp">How to Use This Tool</h2>
	<p>This tool prepares a search of the fire insurance maps created by or for the Department of Insurance Fire Marshal's Office in the Texas Digital Archive (TDA). Click on "Search the Texas Digital Archive" to search the TDA using the options you select.</p>
	<p>Descriptive information is available for <em>all</em> maps in this collection. Due to U.S. copyright law, maps produced by the Sanborn Map Company, other private companies, or an unknown creator were not scanned. Map types such as street maps without keys, public utility maps, zoning maps, building plans, plat maps, and blueprints were not scanned. Additionally, a number of index maps were found to be too large to scan. A placeholder image is in the TDA to advise patrons when a map is not available online. Selecting "Map available online" will limit a search to maps where the full digitized image is available online.</p>
	<p>Selections by date are not available in this custom search as not all maps are dated. After starting your search, you can refine by date in the TDA.</p>
	<h2 id="aboutme">About the Fire Insurance Maps</h2>
	<p>The Texas Department of Insurance (TDI) regulates the Texas insurance industry. The Texas State Fire Marshal is a division of the TDI that promotes fire safety through prevention, education and protection. These Department of Insurance State Fire Marshal fire insurance maps are commercially printed and hand-drawn and were used by the State Fire Marshal's office to determine fire insurance rates for Texas cities and towns. Maps date from 1906 to 1992, undated, bulk dating from 1920 to 1980.</p>
	<p>See the <a href="https://txarchives.org/tslac/finding_aids/11002.xml" target="_blank">finding aid</a> for more information about the fire insurance maps.</p>
</div>
  <!-- Developed at the Texas State Library and Archives Commission by Brian Thomas. For use by the Preservica UA user community. --><!-- change the action="" to your UA base url --><!-- search method researched at http://www.mediacollege.com/internet/javascript/form/multi-search.html -->
'''

javascript = '''
<script type="text/javascript">
function dosearch() {
	var cities = city.options [city.selectedIndex].value;
	var city1, city2;
	if (cities != "") {
		city1 = "dcterms.dcterms_geographic/" + cities + "|";
		city2 = "dcterms.dcterms_geographic/" + cities + "|";
	} else {
		city1 = "";
		city2 = "";
	}
	var counties = county.options [county.selectedIndex].value;
	var county1, county2
	if (counties != "") {
		county1 = "dcterms.dcterms_geographic/" + counties + "|";
		county2 = "dcterms.dcterms_geographic/" + counties + "|";
	} else {
		county1 = "";
		county2 = "";
	}
	var creators = creator.options [creator.selectedIndex].value;
	var creator1, creator2;
	if (creators != "") {
		creator1 = "dcterms.dcterms_creator/" + creators + "|";
		creator2 = "dcterms.dcterms_creator/" + creators + "|";
	} else {
		creator1 = "";
		creator2 = "";
	}
	var types = type.options [type.selectedIndex].value;
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
+ "&parenthierarchy=SO_645f45f1-1197-40a5-b527-28f40db9c5c0" 
+ "&hh_cmis_filter=" 
+ city1 
+ county1 
+ creator1 
+ type1 
+ sf.availability.value; 
window.open(submitto);
return false;
}
function changeable1() {
	var city1 = city.options [city.selectedIndex].innerHTML.slice(0,-7);
	changeable1a = document.getElementById("county");
	changeable1a_notice = document.getElementById("county_notice");
	var changeable1a_arr = [];
	changeable1a_opt = changeable1a.getElementsByTagName("option");
	for (i = 1; i < changeable1a_opt.length; i++) {
		if (changeable1a_opt[i].getAttribute("city").search(city1) == -1){
			changeable1a_opt[i].style.display = "none";
			changeable1a_notice.style.display = "";
		} else {
			changeable1a_opt[i].style.display = "";
		}
	}
	changeable1b = document.getElementById("type");
	changeable1b_notice = document.getElementById("type_notice");
	var changeable1b_arr = [];
	changeable1b_opt = changeable1b.getElementsByTagName("option");
	for (i = 1; i < changeable1b_opt.length; i++) {
		if (changeable1b_opt[i].getAttribute("city").search(city1) == -1){
			changeable1b_opt[i].style.display = "none";
			changeable1b_notice.style.display = "";
		} else {
			changeable1b_opt[i].style.display = "";
		}
	}
	changeable1c = document.getElementById("creator");
	changeable1c_notice = document.getElementById("creator_notice");
	var changeable1c_arr = [];
	changeable1c_opt = changeable1c.getElementsByTagName("option");
	for (i = 1; i < changeable1c_opt.length; i++) {
		if (changeable1c_opt[i].getAttribute("city").search(city1) == -1){
			changeable1c_opt[i].style.display = "none";
			changeable1c_notice.style.display = "";
		} else {
			changeable1c_opt[i].style.display = "";
			
		}
	}
}
function changeable2() {
	var county1 = county.options [county.selectedIndex].innerHTML.slice(0,-7);
	changeable2a = document.getElementById("city");
	changeable2a_notice = document.getElementById("city_notice");
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
	changeable2b = document.getElementById("type");
	changeable2b_notice = document.getElementById("type_notice");
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
	changeable2c = document.getElementById("creator");
	changeable2c_notice = document.getElementById("creator_notice");
	var changeable2c_arr = [];
	changeable2c_opt = changeable2c.getElementsByTagName("option");
	for (i = 1; i < changeable2c_opt.length; i++) {
		if (changeable2c_opt[i].getAttribute("county").search(county1) == -1){
			changeable2c_opt[i].style.display = "none";
			changeable2c_notice.style.display = "";
		} else {
			changeable2c_opt[i].style.display = "";
			
		}
	}
}
function changeable3() {
	var type1 = type.options [type.selectedIndex].innerHTML;
	changeable3a = document.getElementById("city");
	changeable3a_notice = document.getElementById("city_notice");
	var changeable3a_arr = [];
	changeable3a_opt = changeable3a.getElementsByTagName("option");
	for (i = 1; i < changeable3a_opt.length; i++) {
		if (changeable3a_opt[i].getAttribute("type").search(type1) == -1){
			changeable3a_opt[i].style.display = "none";
			changeable3a_notice.style.display = "";
		} else {
			changeable3a_opt[i].style.display = "";
		}
	}
	changeable3b = document.getElementById("county");
	changeable3b_notice = document.getElementById("county_notice");
	var changeable3b_arr = [];
	changeable3b_opt = changeable3b.getElementsByTagName("option");
	for (i = 1; i < changeable3b_opt.length; i++) {
		if (changeable3b_opt[i].getAttribute("type").search(type1) == -1){
			changeable3b_opt[i].style.display = "none";
			changeable3b_notice.style.display = "";
		} else {
			changeable3b_opt[i].style.display = "";
		}
	}
	changeable3c = document.getElementById("creator");
	changeable3c_notice = document.getElementById("creator_notice");
	var changeable3c_arr = [];
	changeable3c_opt = changeable3c.getElementsByTagName("option");
	for (i = 1; i < changeable3c_opt.length; i++) {
		if (changeable3c_opt[i].getAttribute("type").search(type1) == -1){
			changeable3c_opt[i].style.display = "none";
			changeable3c_notice.style.display = "";
		} else {
			changeable3c_opt[i].style.display = "";
			
		}
	}
}
function changeable4() {
	var creator1 = creator.options [creator.selectedIndex].innerHTML;
	changeable4a = document.getElementById("city");
	changeable4a_notice = document.getElementById("city_notice");
	var changeable4a_arr = [];
	changeable4a_opt = changeable4a.getElementsByTagName("option");
	for (i = 1; i < changeable4a_opt.length; i++) {
		if (changeable4a_opt[i].getAttribute("creator").search(creator1) == -1){
			changeable4a_opt[i].style.display = "none";
			changeable4a_notice.style.display = "";
		} else {
			changeable4a_opt[i].style.display = "";
		}
	}
	changeable4b = document.getElementById("county");
	changeable4b_notice = document.getElementById("county_notice");
	var changeable4b_arr = [];
	changeable4b_opt = changeable4b.getElementsByTagName("option");
	for (i = 1; i < changeable4b_opt.length; i++) {
		if (changeable4b_opt[i].getAttribute("creator").search(creator1) == -1){
			changeable4b_opt[i].style.display = "none";
			changeable4b_notice.style.display = "";
		} else {
			changeable4b_opt[i].style.display = "";
		}
	}
	changeable4c = document.getElementById("type");
	changeable4c_notice = document.getElementById("type_notice");
	var changeable4c_arr = [];
	changeable4c_opt = changeable4c.getElementsByTagName("option");
	for (i = 1; i < changeable4c_opt.length; i++) {
		if (changeable4c_opt[i].getAttribute("creator").search(creator1) == -1){
			changeable4c_opt[i].style.display = "none";
			changeable4c_notice.style.display = "";
		} else {
			changeable4c_opt[i].style.display = "";
			
		}
	}
}
</script>
'''

html_output = f"<html>{html_head}{javascript}</html>"

with open(f'{to_crawl}/output.html', 'w') as w:
    w.write(html_output)
w.close()
print("compilation complete")