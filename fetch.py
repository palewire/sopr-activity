#!/usr/bin/env python
"""
Fetches, parses and archives the XML data dumps of lobbyist's
political activity published by The Senate Office of Public Records.
 
What it does:
1. Download and unzip files into a timestamped directory structure.

Soon it will:
1. Parse through the XML and output CSV text dumps and pickle files of all the data
2. Load that data into a Django app.

"""
import os
import re
import codecs
import urllib
import zipfile
import datetime
try:
	from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup
except ImportError:
	print """
ImportError: Required module not found: Beautiful Soup.

Installation instructions:

If you have easy_install, enter: "sudo easy_install BeautifulSoup"

Otherwise, the source can be downloaded from http://www.crummy.com/software/BeautifulSoup/
"""
	raise SystemExit


def mkdir(parent_dir_path, child_dir_name):
	"""
	Creates a new directory if it doesn't already exist.
	
	Pass in a root directory and the desired name for new child directory.
	
	Returns the child directory path.
	
	Example usage::
	
		new_dir = mkdir('.', 'data')

	"""
	child_dir_path = os.path.join(parent_dir_path, child_dir_name)
	if not os.path.isdir(child_dir_path):
		os.mkdir(child_dir_path)
		print "Creating %s" % child_dir_path
	return child_dir_path

def get_zip_links():
	"""
	Snatches the HTML from the Senate Office of Public Records download site, extracts all the zip file for download.
	
	Returns a list of URLs.
	"""
	url = 'http://www.senate.gov/legislative/Public_Disclosure/database_download.htm'
	http = urllib.urlopen(url)
	soup = BeautifulSoup(http)
	anchor_tags = soup.findAll('a')
	zip_links = []
	for a in anchor_tags:
		href = a['href']
		if re.search('(.*).zip', href):
			zip_links.append(href)
	return zip_links

def download_file(url, target_dir):
	"""
	Accepts a URL leading to a file and downloads it to the target directory.
	"""
	file_name = url.split('/')[-1]
	file_path = os.path.join(target_dir, file_name)
	urllib.urlretrieve(url, file_path)
	print "Downloaded %s " % file_name

def unzip_file(file_path, target_dir):
	"""
	Cracks open a zipfile and saves its contents in the target directory.
	"""
	zip_file = zipfile.ZipFile(file_path)
	for file_name in zip_file.namelist():
		f = open(os.path.join(target_dir, file_name), 'wb')
		f.write(zip_file.read(file_name))
		f.close()
		print "Unzipped %s" % file_name

def run():
	# Setting timestamps
	now = datetime.datetime.now()
	datestamp = now.strftime('%Y-%m-%d')
	timestamp = now.strftime('%Hh%Mm%Ss')
	
	# Setting directory variables
	working_dir = os.path.dirname(__file__)
	data_dir = mkdir(working_dir, 'data')
	date_dir = mkdir(data_dir, datestamp)
	scrape_dir = mkdir(date_dir, timestamp)
	zip_dir = mkdir(scrape_dir, 'zip')
	xml_dir = mkdir(scrape_dir, 'xml')

	# Downloading the zip files and unpacking the xml
	zip_links = get_zip_links()
	[download_file(url, zip_dir) for url in zip_links[0:1]] # Temporarily set to only work on the first file, so I can run through quicker.
	[unzip_file(os.path.join(zip_dir, file_name), xml_dir) for file_name in os.listdir(zip_dir) if re.search(".zip", file_name)]

if __name__ == '__main__':
	"""
	Fires off when the script is run through the shell or via crontab.
	
	Example usage::
	
		$ python fetch.py
	"""
	run()