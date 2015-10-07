from django.db import models

# Create your models here.

class Project(models.Model):
        name = models.CharField(max_length=200)
        description = models.CharField(max_length=400)

        def __unicode__(self):
                return u'%d %s %s' % (self.id, self.name, self.description)

class Tag(models.Model):
		project = models.ForeignKey(Project)
        	name = models.CharField(max_length=200)
        	description = models.CharField(max_length=400)
