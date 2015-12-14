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
	class Meta:
		unique_together = ('name',)
	def as_json(self):
		return dict( 
			type='project', id=self.id, 
			name=self.name, description=self.description, created=str(self.created),
			last_modified=str(self.last_modified))

class Tag(models.Model):
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=400)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	def as_json(self):
		return dict(type='tag',
			tag_id=self.id, tag_name=self.name,
			tag_description=self.description, tag_created=str(self.created),
			tag_last_modified=str(self.last_modified))                

class Result(models.Model):
	project = models.ForeignKey(Project)
	tag = models.ForeignKey(Tag)

	name = models.CharField(max_length=200)
	description = models.CharField(max_length=400, blank=True, null=True)
	version = models.CharField(max_length=100)
	filename = models.CharField(max_length=100, null=True)
	duration = models.CharField(max_length=100, null=True)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	baseline = models.NullBooleanField(default=False, null=True)
	numberofusers = models.IntegerField(null=True)

	class Meta:
		unique_together = ('project', 'tag', 'version', 'name')

	def as_json(self):
		return dict( type='result', result_id=self.id,
			project_id=self.project_id, tag_id=self.tag_id,
			name=self.name, description=self.description, created=str(self.created),
			last_modified=str(self.last_modified), baseline=self.baseline, version=self.version, numberofusers=self.numberofusers)

class Transaction(models.Model):
	result = models.ForeignKey(Result)
	
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=400, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	successcount = models.IntegerField()
	failurecount = models.IntegerField()
	average = models.FloatField()
	median = models.FloatField()
	minimum = models.FloatField()
	maximum = models.FloatField()
	stddev = models.FloatField()
	p90 = models.FloatField()
	p95 = models.FloatField()
	p99 = models.FloatField()
	p99_99 = models.FloatField()

	

	def as_json(self):
		return dict(type='transaction',
			result_id=self.result_id,
			name=self.name, description=self.description, created=str(self.created),
			last_modified=str(self.last_modified), successcount=self.successcount, failurecount=self.failurecount,
			average=self.average, median=self.median, minimum=self.minimum, maximum=self.maximum, stddev=self.stddev,
			p90=self.p90, p95=self.p95, p99=self.p99, p99_99=self.p99_99)

	def as_short_json(self):
		return dict(type='transaction',
			id=self.id, result_id=self.result_id,
			name=self.name, description=self.description,  created=str(self.created),
			last_modified=str(self.last_modified), successcount=self.successcount, failurecount=self.failurecount,
			average=self.average, median=self.median, minimum=self.minimum, maximum=self.maximum, stddev=self.stddev,
			p90=self.p90, p95=self.p95, p99=self.p99, p99_99=self.p99_99)

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Result._meta.fields]