from django.db import models
from datetime import datetime
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


# Create your models here.

 
class CaseInsensitiveModelBackend(ModelBackend):
  """
  By default ModelBackend does case _sensitive_ username authentication, which isn't what is
  generally expected.  This backend supports case insensitive username authentication.
  """
  def authenticate(self, username=None, password=None):
    try:
      user = User.objects.get(username__iexact=username)
      if user.check_password(password):
        return user
      else:
        return None
    except User.DoesNotExist:
      return None

      
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
	description = models.CharField(max_length=400, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ('name','project')

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
	start_time = models.DateTimeField(null=True)
	duration_minutes = models.FloatField()
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
			last_modified=str(self.last_modified), baseline=self.baseline, version=self.version, numberofusers=self.numberofusers, duration_minutes=self.duration_minutes)

class Transaction(models.Model):
	result = models.ForeignKey(Result)
	
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=400, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	success_count = models.IntegerField()
	success_qps = models.FloatField()
	failure_count = models.IntegerField()
	failure_qps = models.FloatField()
	responsetime_average = models.FloatField()
	responsetime_median = models.FloatField()
	responsetime_minimum = models.FloatField()
	responsetime_maximum = models.FloatField()
	responsetime_stddev = models.FloatField()
	responsetime_p90 = models.FloatField()
	responsetime_p95 = models.FloatField()
	responsetime_p99 = models.FloatField()
	responsetime_p99_99 = models.FloatField()

	

	def as_json(self):
		return dict(type='transaction',
			result_id=self.result_id,
			name=self.name, description=self.description, created=str(self.created),
			last_modified=str(self.last_modified), success_count=self.success_count, failure_count=self.failure_count,
			success_qps=self.success_qps, failure_qps=self.failure_qps,
			responsetime_average=self.responsetime_average, responsetime_median=self.responsetime_median, responsetime_minimum=self.responsetime_minimum, 
			responsetime_maximum=self.responsetime_maximum, responsetime_stddev=self.responsetime_stddev,responsetime_p90=self.responsetime_p90, 
			responsetime_p95=self.responsetime_p95, responsetime_p99=self.responsetime_p99, responsetime_p99_99=self.responsetime_p99_99)

	def as_short_json(self):
		return dict(type='transaction',
			id=self.id, result_id=self.result_id,
			name=self.name, description=self.description,  created=str(self.created),
			last_modified=str(self.last_modified), success_count=self.success_count, failure_count=self.failure_count,
			success_qps=self.success_qps, failure_qps=self.failure_qps,
			responsetime_average=self.responsetime_average, responsetime_median=self.responsetime_median, responsetime_minimum=self.responsetime_minimum, 
			responsetime_maximum=self.responsetime_maximum, responsetime_stddev=self.responsetime_stddev, responsetime_p90=self.responsetime_p90, 
			responsetime_p95=self.responsetime_p95, responsetime_p99=self.responsetime_p99, responsetime_p99_99=self.responsetime_p99_99)

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Result._meta.fields]