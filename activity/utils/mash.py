# Helpers
import csv
from django.utils.encoding import *
import cPickle as pickle

# Models
from models import Person, Lobbyist


def distincter():
  lobbyists = csv.reader(open("./data/lobbyists.txt", 'r'), delimiter='|')
  distinct_names = []
  for i, row in enumerate(lobbyists):
    xml, lda, name, one, two, three = row
    if name not in distinct_names:
      distinct_names.append(name)
      print "Added name %s => %s" % (len(distinct_names), name)
  pickle.dump(distinct_names, open("./data/lobbyists.pickle", 'w'))
 
def splitter():
  name_list = pickle.load(open("./data/lobbyists.pickle", 'r'))
  failfile = open('./data/failfile.out', 'w')
  for name in name_list:
    try:
      l, created = Lobbyist.objects.get_or_create(
        first_name = name.split(",")[0],
        last_name = name.split(",")[1]
        )
      if created:
        print "Added %s" % (name)
    except:
      print >> failfile, name
  failfile.out


def merger():
  o_list = Person.objects.all()
  result_list = []
  for o in o_list:
    l = Lobbyist.objects.filter(first_name__iexact=o.last_name).order_by("last_name")
    for x in l:
      result_list.append([smart_str(o.last_name), smart_str(o.first_name), smart_str(x.first_name), smart_str(x.last_name.strip())])
  writer = csv.writer(open('./data/last_name_hits.csv', 'w'), delimiter='|')
  writer.writerows(result_list)

def jackpot():
  o_list = Person.objects.all()
  result_list = []
  for o in o_list:
    l = Lobbyist.objects.filter(first_name__iexact=o.last_name, last_name__iexact=o.first_name)
    for x in l:
      result_list.append([smart_str(o.last_name), smart_str(o.first_name), smart_str(x.first_name), smart_str(x.last_name)])
  writer = csv.writer(open('data/both_name_hits.csv', 'w'))
  writer.writerows(result_list)


def load():
	# Open
	ppl = csv.reader(open("./data/people.csv", 'r'))
	# Skip header
	ppl.next()
	# Init a list for just the names in the style we prefer
	ppl_list = []
	# Loop
	for i, row in enumerate(ppl):
		name, first, last = row
		o, created = Person.objects.get_or_create(
			first_name = first.strip(),
			last_name = last.strip(),
		)
		if created:
			print "Added %s %s" % (first, last)
			

def mash():
	# Open
	ppl = csv.reader(open("./data/ppl.csv", 'r'))
	# Skip header
	obamatons.next()
	# Init a list for just the names in the style we prefer
	obamaton_list = []
	# Loop

	test_list = [[u'Ben', u'Welsh'], [u'Kevin', u'Bogardus'], [u'Sam', u'Myers']]

	for i, row in enumerate(obamatons):
	    name, first, last, position, department = row
	    name_obj = [smart_unicode(first.strip()), smart_unicode(last.strip())]
	    obamaton_list.append(name_obj)

	for obamaton in obamaton_list:
	    if obamaton in test_list:
	       hit = True
	       print "%s => %s" % (obamaton, hit)
	    else:
	       hit = False
    
    