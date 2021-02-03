# common definitions file
import errno
import os
import requests
#login routine would go here
def login (url, payload):
	#this will log into the preservica API and get an access token
	auth = requests.post(url, data=payload).json()
	sessionToken = auth["token"]
	headers = {'Preservica-Access-Token': sessionToken}
	headers['Content-Type'] = 'application/xml'
	headers['Accept-Charset'] = 'UTF-8'
	return headers

def dirMaker (filename):
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename), exist_ok=True)
		except OSError as exc:
			if exc.errno != errno.EExist:
				raise

def filemaker(filename, response):
	with open(filename, "wb") as md:
		for chunk in response.iter_content(chunk_size=128):
			md.write(chunk)
	md.close()