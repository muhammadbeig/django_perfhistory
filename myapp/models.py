from django.db import models

# Create your models here.

class Project(models.Model):
        project_name = models.CharField(max_length=200)
        project_description = models.CharField(max_length=400)

        def __unicode__(self):
                return u'%d|%s|%s' % (self.id, self.project_name, self.project_description)

class Tags(models.Model):
		project = models.ForeignKey(Project)
        	tag_name = models.CharField(max_length=200)
        	tag_description = models.CharField(max_length=400)
