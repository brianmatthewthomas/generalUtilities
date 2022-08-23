import os
import time

error_log = input("name of error log file: ")
log = open(error_log, "a")
crawler = input("Directory to crawl for errors: ")

dir = ""
for dirpath, dirnames, filenames in os.walk(crawler):
	for filename in filenames:
		filename = os.path.join(dirpath, filename)
		if dir != dirpath:
			current = time.asctime()
			print("checking",dirpath,"starting at",current)
			dir = dirpath
		with open(filename, "r") as f:
			filedata = f.read()
			if "xip" not in filedata:
				print("error in",filename)
				if "IO_" in filename:
					type = "IO"
					core = "information-objects/"
					finder = filename.find("IO_")
					finder2 = finder - 1
					directory = filename[:finder2]
					xip_file = filename[finder:]
				if "SO_" in filename:
					type = "SO"
					core = "structural-objects/"
					finder = filename.find("SO_")
					finder2 = finder - 1
					directory = filename[:finder2]
					xip_file = filename[finder:]
				if "metadata" in filename:
					uuid = filename[-51:-15]
				else:
					uuid = filename[-40:-4]
				log.write("https://tsl.preservica.com/api/entity/" + core + uuid + "," + directory + "," + xip_file + "," + type + "\n")
				
print("all done")
print("don't forget to modify errors.csv to be in the format needed for newAPI_UUIDs_patch.py")
log.close()