# this script will take a google analytics csv export and prepare it for data crunching
# it uses regular expressions to look for the preservica UUID, then
# uses re and csv modules to load a google analytics csv and replace column1 text with UUID it contains
# if no UUID it leaves it alone
# generates a placeholder file for next step
# uses pandas and openpyxl to consolidate data from the csv and spit out a excel workbook
# avg time on page and a handful of other columns dropped as incompatible with this process
# output excel file created to line up with vlookup.py configuration
# use in coordination with python_vlookup/python_vlookupDirectory to get collection level stats
import sys, os, re, csv

import pandas as PD

from openpyxl import load_workbook
# print beginning directions
print("go to google analytics and download data as csv format")
print("put that csv file in same folder as this file")
print("remove the header summary data and summary numbers data from the las line")
print("proceed...")
# get input variables and set the stage
sourceFile = input("Name of analytics file: ")
newFile = input("Name of output file for analytics crunching, use xlsx file extension: ")
outfile = open('placeholder.csv', 'w', newline='')
writer = csv.writer(outfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
# process the first step, replace unnecessary stuff with just the UUIDs
with open(sourceFile, newline='\n') as f:
	spam = csv.reader(f, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
	for row in spam:
		#use try instead of do so it will pass up rows where the steps encapsulated don't work
		try:
			df1 = row[0]
			#below if the regex used to accomplish task
			if re.search(r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}", df1):
				courtesy = re.search(r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}", df1)
				testy = courtesy[0]
				row[0] = testy
			df2 = row[5]
			df2 = df2.replace('%','')
			row[5] = df2
		except:
			writer.writerow(row)
			continue
		#write the file
		writer.writerow(row)
f.close()
outfile.close()
#wrap up first step and start second step
print("placeholder file something.txt created")
print("starting pandas processing...")
# read placeholder file as a system table for manipulation
df1 = PD.read_csv("placeholder.csv")
# change the pageviews, unique pagesview and bounce rate to integers for processing
df1['Pageviews'] = PD.to_numeric(df1['Pageviews'])
df1['Unique Pageviews'] = PD.to_numeric(df1['Unique Pageviews'])
df1['Bounce Rate'] = PD.to_numeric(df1['Bounce Rate'])
# change avg time on page to a number, may add it back into output later
df1['Avg. Time on Page'] = PD.to_timedelta(df1['Avg. Time on Page'], unit='h')
# consolidate data together based on whether it matches in the first column1
# sum function for addition, first means it sorts alpha
results = df1.groupby(df1['Page']).agg({'Page': 'first', 'Pageviews': 'sum', 'Unique Pageviews': 'sum', 'Bounce Rate': 'sum'})
# change 1st column to UUIDs to align with analytics crunching scripts already in existence
results = results.rename(columns={'Page': 'UUIDs'})
# write it up
written = PD.ExcelWriter(newFile, engine='xlsxwriter')
results.to_excel(written, "processed", index=False)
# cleanup and let resource go
written.save()
written.close()
print("all done!")
# friendly reminder to remove placeholder file since it is ephemeral
print("Don't forget to delete placeholder.csv")
os.remove('placeholder.csv')