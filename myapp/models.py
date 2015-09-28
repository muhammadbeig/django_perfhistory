from django.db import models

# Create your models here.

class Project(models.Model):
        project_name = models.CharField(max_length=200)
        project_description = models.CharField(max_length=400)

        def __unicode__(self):
                return u'%s %s' % (self.project_name, self.id)

class Tags(models.Model):
		project = models.ForeignKey(Project)
        	tag_name = models.CharField(max_length=200)
        	tag_description = models.CharField(max_length=400)
