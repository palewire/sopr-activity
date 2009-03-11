#!/usr/bin/env python
"""
Fetches, parses and archives the XML data dumps of lobbyist's
political activity published by The Senate Office of Public Records.
 
What it does:
1. Download and unzip files into a timestamped directory structure.
2. Parse through the XML and output CSV text dumps and pickle files of all the data

Soon it will:
3. Load that data into a Django app.

"""
import os
import re
import csv
import codecs
import urllib
import zipfile
import datetime
try:
	import cPickle as pickle
except ImportError:
	import pickle
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

def parse_xml(file_path):
	"""
	Opens up a XML file and parses through it according to patterns I've figured out by messing around and eyeballing the file structure.
	
	Returns a dictionary containing six lists:
		* filings
		* lobbyists
		* issues
		* foreign_entities
		* affiliated_orgs
		* govt_entities
	
	Example usage:
	
		filings, lobbyists, issues, foreign_entities, affiliated_orgs, govt_entities = parse_xml('./test.xml')
	
	"""
	print "Parsing file %s" % file_path
	xml = open(file_path, "r")
	soup = BeautifulStoneSoup(xml, selfClosingTags=['registrant', 'client'])
	
	filings, lobbyists, issues  = [], [], []
	foreign_entities, affiliated_orgs, govt_entities = [], [], []
	
	for record in soup.publicfilings.findAll('filing'):
		
		filings.append([
			file_path,
			record.get('id', None),
			record.get('year', None),
			record.get('received', None),
			record.get('type', None),
			record.get('period', None),
			record.registrant.get('registrantid', None),
			record.registrant.get('registrantname', None),
			record.registrant.get('generaldescription', None),
			record.registrant.get('address', None),
			record.registrant.get('registrantcountry', None),
			record.registrant.get('registrantppbcountry', None),
			record.client.get('clientid', None),
			record.client.get('clientname', None),
			record.client.get('clientstatus', None),
			record.client.get('contactfullname', None),
			record.client.get('clientcountry', None),
			record.client.get('clientppbcountry', None),
			record.client.get('clientstate', None),
			record.client.get('clientppbstate', None),
			])
			
		if record.lobbyists:
			for lobbyist_record in record.lobbyists:
				lobbyists.append([
					file_path,
					record.get('id', None),
					lobbyist_record.get('lobbyistname', None),
					lobbyist_record.get('lobbyiststatus', None),
					lobbyist_record.get('lobbyisteindicator', None),
					lobbyist_record.get('officialposition', None),
					])
		
		if record.issues:
			for issue_record in record.issues:
				issues.append([
					file_path,
					record.get('id', None),
					issue_record.get('code', None),
					])

		if record.foreignentities:
			for foreign_entities_record in record.foreignentities:
				foreign_entities.append([
					file_path,
					record.get('id', None),
					foreign_entities_record.get('foreignentityname', None),
					foreign_entities_record.get('foreignentitycountry', None),
					foreign_entities_record.get('foreignentityppbcountry', None),
					foreign_entities_record.get('foreignentitycontribution', None),
					foreign_entities_record.get('foreignentitystatus', None),
					])

		if record.affiliatedorgs:
			for affiliated_orgs_record in record.issues:
				affiliated_orgs.append([
					file_path,
					record.get('id', None),
					affiliated_orgs_record.get('affiliatedorgname', None),
					affiliated_orgs_record.get('affiliatedorgcountry', None),
					affiliated_orgs_record.get('affiliatedorgname', None),
					affiliated_orgs_record.get('affiliatedorgppbcountry', None),
					])
		
		if record.governmententities:
			for govt_entities_record in record.governmententities:
				govt_entities.append([
					file_path,
					record.get('id', None),
					govt_entities_record.get('goventityname', None),
					])

	return dict([
			('filings', filings), 
			('lobbyists', lobbyists),
			('issues', issues),
			('foreign_entities', foreign_entities),
			('affiliated_orgs', affiliated_orgs),
			('govt_entities', govt_entities),
		])

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
	csv_dir = mkdir(scrape_dir, 'csv')
	pickle_dir = mkdir(scrape_dir, 'pickle')
	
	# Downloading the zip files and unpacking the xml
	zip_links = get_zip_links()
	[download_file(url, zip_dir) for url in zip_links[0:1]] # Temporarily set to only work on the first file, so I can run through quicker.
	[unzip_file(os.path.join(zip_dir, file_name), xml_dir) for file_name in os.listdir(zip_dir) if re.search(".zip", file_name)]

	# Loop through the XML files and parse out the data in each
	xml_files = [os.path.join(xml_dir, file_name) for file_name in os.listdir(xml_dir) if re.search(".xml", file_name)]
	for xml_file in xml_files[0:1]: # Temporarily set to only work with the first XML, for testing
		data_dict = parse_xml(xml_file)
		for file_name, data in data_dict.items():
			if data:
				print "Writing out data from %s" % file_name
				# CSV
				writer = csv.writer(open(os.path.join(csv_dir, file_name + '.csv'), 'w+'))
				writer.writerows(data)
				# Pickle
				pickle_file = os.path.join(pickle_dir, file_name + '.pickle')
				if os.path.isfile(pickle_file):
					pickled_list = pickle.load(pickle_file)
					[pickled_list.append(record) for record in data]
					pickle.dump(pickled_list, open(pickle_file, 'w'))
				else:
					pickle.dump(data, open(pickle_file, 'w'))

if __name__ == '__main__':
	"""
	Fires off when the script is run through the shell or via crontab.
	
	Example usage::
	
		$ python fetch.py
	"""
	run()