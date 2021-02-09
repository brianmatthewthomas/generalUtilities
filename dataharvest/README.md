<h1>Data harvesting</h1>
Data harvesting is done for various bits of metadata manipulation when you need to have some specificity on what you are updating rather than across the board updated. For example, if text "x" occurs in "y" tag, then add "z" tag plus content. The other major application is for creation web analytics based upon the UUIDs of items since that is a constant factor in a repository even if the file tree is not.

These tools are written with the preservica system in mind with the underlying assumption that you are harvesting raw data as well as metadata, as well as that every item in the preservation system will have some kind of metadata attached.
<h3>python_newAPI_harvest_UUIDs_addMissingMetadata.py</h3>
This script will harvest metadata for a collection of items, recursively going through the structure of the items based upon the hierarchy in the preservation system metadata. For level of depth in the system, a new folder is populated with the harvested data and any metadata files using "_metadata-#.xml" convention. It assumes that if no metadata of a certain kind is present (Qualified Dublin Core) then a standard template should be added. It is set to log back in every 10 minutes by default.
<h4>parameters</h4>

`username` = system username which should be your email<br/>
`password` = system password, using the getpass module so the terminal window won't show the password.<br/>
`tenancy` = tenancy for the system, usually the letters before .access.preservica.com on the UA<br/>
`filepath` = where you want the files to be saved<br/>
`UUID for the collection` = the unique identifier for the collection to start from<br/>
`metadata filename` = template metadata file to insert of no metadata is attached
<h4>Invocation</h4>

In an open terminal window that has this script: `python3 python_newAPI_harvest_UUIDs_addMissingMetadata.py` . Answer the parameters when asked.
<h4>Notes</h4>
Due to expected issues with connections to API, it is necessary to do a second pass at the hest to catch any files accidentally skipped. First explore the levels and remove and files that show a connection error, then re-run. It is set up to crawl through and only harvest missing files so depending on how many instances you have going of this process it can be very quick.<br/>
This is set up log back in every 10 minutes to prevent an API timeout.
<h3>python_newAPI_harvest_errorCatcher.py</h3>
Despite best efforts, sometimes an error occurs in a data harvest. This script is meant to track those down to be able to patch the harvest. It will crawl through the targeted directory and search for "xip", which is a common element among all the harvested data. It will list the directory it is currently crawling so you know the status<br/>
If xip is not found in the text of the file, it will add the expected URL for the data file (not the metadata file), and the filepath of the bad file. Note that the url is derived from the naming convention on the data harvest so it is import that they correspond exactly.<br/>
To prep the output for a patch harvest you will need to replace the last "/" which seperates the filepath from filename with an ," then replace the .xml with a .xml",IO or .xml",SO as appropriate. You will also need replace the _metadata-# from the xml filename as a patch harvest will just append _metadata-# to whatever is there.
<h4>parameters</h4>

`csv filename` = whatever the file name you want for the error log<br/>
`directory to walk` = the folder you wish to crawl, it will crawl subfolders recursively.
<h4>invocation</h4>
In open terminal window that has this script: `python3 python_newAPI_harvest_errorCatcher.py` . Answer the question prompts. 