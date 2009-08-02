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

##Opening out files 
this_scripts_data_subdirectory = './data'
out_filings = codecs.open(os.path.join(this_scripts_data_subdirectory, "filings.txt"), "w", "utf-8")
out_lobbyists = codecs.open(os.path.join(this_scripts_data_subdirectory, 'lobbyists.txt'), "w", "utf-8")
out_issues = codecs.open(os.path.join(this_scripts_data_subdirectory, 'issues.txt'), "w", "utf-8")
out_gov_entities = codecs.open(os.path.join(this_scripts_data_subdirectory, 'govt_entities.txt'), "w", "utf-8")
out_affliated_orgs = codecs.open(os.path.join(this_scripts_data_subdirectory, 'affiliated_orgs.txt'), "w", "utf-8")
out_foreign_entities = codecs.open(os.path.join(this_scripts_data_subdirectory, 'foreign_entities.txt'), "w", "utf-8")


##Downloading the latest file

root_url = "http://soprweb.senate.gov/downloads/"
zip_names = ['2009_3.zip', '2009_2.zip', '2009_1.zip',
			 '2008_4.zip', '2008_3.zip', '2008_2.zip', '2008_1.zip', 
#			 '2007_4.zip', '2007_3.zip', '2007_2.zip', '2007_1.zip', 
#			 '2006_4.zip', '2006_3.zip', '2006_2.zip', '2006_1.zip',
#			 '2005_4.zip', '2005_3.zip', '2005_2.zip', '2005_1.zip',
#			 '2004_4.zip', '2004_3.zip', '2004_2.zip', '2004_1.zip',
#			 '2003_4.zip', '2003_3.zip', '2003_2.zip', '2003_1.zip',
#			 '2002_4.zip', '2002_3.zip', '2002_2.zip', '2002_1.zip',
#			 '2001_4.zip', '2001_3.zip', '2001_2.zip', '2001_1.zip',
#			 '2000_4.zip', '2000_3.zip', '2000_2.zip', '2000_1.zip',
#			 '1999_4.zip', '1999_3.zip', '1999_2.zip', '1999_1.zip'
			]
for zip_name in zip_names:
	target_zip = root_url + zip_name
	local_zip = os.path.join(this_scripts_data_subdirectory, zip_name)

	try:
		urllib.urlretrieve(target_zip, local_zip)
		print "Downloaded %s" % zip_name
	except:
		print "Failed to download %s" % zip_name

##Unzip file

	unzip_command = "unzip %s -d %s" % (local_zip, this_scripts_data_subdirectory)

	try:
	   os.system(unzip_command)
	   print "Unzipped %s" % zip_name
	except:
	   print "Failed to unzip %s" % zip_name

##Open XML contents

this_scripts_downloads = os.listdir(this_scripts_data_subdirectory)
this_scripts_xml_files = []

for file in this_scripts_downloads:
	if re.search(".xml", file): 
		this_scripts_xml_files.append(file)

for xml_file_name in this_scripts_xml_files:
	print "Opening %s" % xml_file_name

	xml_file = os.path.join(this_scripts_data_subdirectory, xml_file_name)
	xml = open(xml_file, "r")

##Parse the file with BeautifulSoup

	soup = BeautifulStoneSoup(xml, selfClosingTags=['registrant', 'client'])



	for record in soup.publicfilings.findAll('filing'):
	
		filing = []
		filing.append(xml_file_name)
		try: filing.append(record['id'])
		except: filing.append('null')
		try: filing.append(record['year'])
		except: filing.append('null')
		try: filing.append(record['received'])
		except: filing.append('null')
		try: filing.append(record['type'])
		except: filing.append('null')
		try: filing.append(record['period'])
		except: filing.append('null')

		try: filing.append(record.registrant['registrantid'])
		except: filing.append('null')
		try: filing.append(record.registrant['registrantname'])
		except: filing.append('null')
		try: filing.append(record.registrant['generaldescription'])
		except: filing.append('null')
		try: filing.append(record.registrant['address'])
		except: filing.append('null')
		try: filing.append(record.registrant['registrantcountry'])
		except: filing.append('null')
		try: filing.append(record.registrant['registrantppbcountry'])
		except: filing.append('null')

		try: filing.append(record.client['clientid']) 
		except: filing.append('null')
		try: filing.append(record.client['clientname'])
		except: filing.append('null')
		try: filing.append(record.client['clientstatus'])
		except: filing.append('null')
		try: filing.append(record.client['contactfullname'])
		except: filing.append('null')
		try: filing.append(record.client['clientcountry'])
		except: filing.append('null')
		try: filing.append(record.client['clientppbcountry'])
		except: filing.append('null')
		try: filing.append(record.client['clientstate'])
		except: filing.append('null')
		try: filing.append(record.client['clientppbstate'])
		except: filing.append('null')

		print >> out_filings, '|'.join(filing)

	
		try:
			for lobbyists in record.lobbyists:
				lobbyist = []
				lobbyist.append(xml_file_name)
				try: lobbyist.append(record['id'])
				except: lobbyist.append('null')
				try: lobbyist.append(lobbyists['lobbyistname'])
				except: lobbyist.append('null')
				try: lobbyist.append(lobbyists['lobbyiststatus'])
				except: lobbyist.append('null')
				try: lobbyist.append(lobbyists['lobbyisteindicator'])
				except: lobbyist.append('null')
				try: lobbyist.append(lobbyists['officialposition'])
				except: lobbyist.append('null')
				print >> out_lobbyists,'|'.join(lobbyist)
		except:
			pass 
	

		try:
			for issues in record.issues:
				issue = []
				issue.append(xml_file_name)
				try: issue.append(record['id'])
				except: issue.append('null')
				try: issue.append(issues['code'])
				except: issue.append('null')
				print >> out_issues, '|'.join(issue)
		except:
			pass 
	
	
		try:
			for foreigns in record.foreignentities:
				foreign = []
				foreign.append(xml_file_name)
				try: foreign.append(record['id'])
				except: foreign.append('null')
				try: foreign.append(foreigns['foreignentityname'])
				except: foreign.append('null')
				try: foreign.append(foreigns['foreignentitycountry'])
				except: foreign.append('null')
				try: foreign.append(foreigns['foreignentityppbcountry'])
				except: foreign.append('null')
				try: foreign.append(foreigns['foreignentitycontribution'])
				except: foreign.append('null')
				try: foreign.append(foreigns['foreignentitystatus'])
				except: foreign.append('null')
				print >> out_foreign_entities, '|'.join(foreign)
		except:
			pass

		try:
			for affiliates in record.affiliatedorgs:
				affiliate = []
				affiliate.append(xml_file_name)
				try: affiliate.append(record['id'])
				except: affiliate.append('null')
				try: affiliate.append(affiliates['affiliatedorgname'])
				except: affiliate.append('null')
				try: affiliate.append(affiliates['affiliatedorgcountry'])
				except: affiliate.append('null')
				try: affiliate.append(affiliates['affiliatedorgname'])
				except: affiliate.append('null')
				try: affiliate.append(affiliate['affiliatedorgppbcountry'])
				except: affiliate.append('null')
				print >> out_affliated_orgs, '|'.join(affiliate)
		except:
			pass 
	
		try:
			for govt_entities in record.governmententities:
				govt_entity = []
				govt_entity.append(xml_file_name)
				try: govt_entity.append(record['id'])
				except: govt_entity.append('null')
				try: govt_entity.append(govt_entities['goventityname'])
				except: govt_entity.append('null')
				print >> out_gov_entities, '|'.join(govt_entity)
		except:
			pass 



out_filings.close()
out_lobbyists.close()
out_issues.close()
out_gov_entities.close()
out_affliated_orgs.close()
out_foreign_entities.close()   
