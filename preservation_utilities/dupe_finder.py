# use this tool to check a directory for duplicate files. It uses SHA256 to check rather than filename
# if you have very large files this will take a while
# it checks ALL files and gives and EXACT so make sure you can see system files since those are included
import os
import hashlib


def create_sha256(filename):
    sha256 = hashlib.sha256()
    blocksize = 65536
    with open(filename, 'rb') as f:
        buffer = f.read(blocksize)
        while len(buffer) > 0:
            sha256.update(buffer)
            buffer = f.read(blocksize)
    fixity = sha256.hexdigest()
    return fixity

hashdict = {}
# input variables, use relative OR full filepaths
tocrawl = input("directory to check for dupes: ")
logger = input("name of log file for duplicates: ")

print("checking directory for duplicates")
dirname1 = ""
# start crawling directory recursively
for dirpath, dirnames, filenames in os.walk(tocrawl):
    for filename in filenames:
        # print out directory name so users know where in the process it is
        if dirname1 != dirpath:
            dirname1 = dirpath
            print("checking",dirname1)
        filename = os.path.join(dirpath, filename)
        # send file to be checksummed
        hashish = create_sha256(filename)
        # check dictionary, add to list of files if checksum match exists, create new key/list pair if not
        if hashish in hashdict:
            hashdict[hashish].append(filename)
        else:
            hashdict[hashish] = [filename]
print("checking done, writing results")
log = open(logger, "a")
# check dictionary for lists with more than one item and print the filenames to a log file if that is the case
for key in hashdict:
    variable = hashdict[key]
    if len(variable) > 1:
        print(hashdict[key])
        for item in variable:
            log.write(item + "\n")
        log.write("-----------------------------\n")
log.close()
print("finished outputting results")