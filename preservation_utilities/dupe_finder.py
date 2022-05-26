# use this tool to check a directory for duplicate files. It uses SHA256 to check rather than filename
# if you have very large files this will take a while
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

tocrawl = input("directory to check for dupes: ")
logger = input("name of log file for duplicates: ")

print("checking directory for duplicates")
dirname1 = ""
for dirpath, dirnames, filenames in os.walk(tocrawl):
    for filename in filenames:
        if dirname1 != dirpath:
            dirname1 = dirpath
            print("checking",dirname1)
        filename = os.path.join(dirpath, filename)
        hashish = create_sha256(filename)
        if hashish in hashdict:
            hashdict[hashish].append(filename)
        else:
            hashdict[hashish] = [filename]
print("checking done, writing results")
log = open(logger, "a")
for key in hashdict:
    variable = hashdict[key]
    if len(variable) > 1:
        print(hashdict[key])
        for item in variable:
            log.write(item + "\n")
        log.write("-----------------------------\n")
log.close()
print("finished outputting results")