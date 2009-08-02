from django.db import models
 
class Person(models.Model):
	"""
	A person who may or may not be a lobbyist.
	"""
	first_name = models.CharField(max_length=300)
	last_name = models.CharField(max_length=300)

	def __unicode__(self):
		return "%s %s" % (self.first_name, self.last_name)


class Lobbyist(models.Model):
	"""
	A lobbyist pulled from the SOPR registration documents.
	"""
	first_name = models.CharField(max_length=300)
	last_name = models.CharField(max_length=300)

	def __unicode__(self):
		return "%s %s" % (self.first_name, self.last_name)

