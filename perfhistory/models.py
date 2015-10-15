from django.db import models
from datetime import datetime



# Create your models here.

class Project(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=400,blank=True)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	def __unicode__(self):
                return u'%d %s %s' % (self.id, self.name, self.description)

class Tag(models.Model):
		project_id = models.ForeignKey(Project)
		name = models.CharField(max_length=200)
		description = models.CharField(max_length=400)                