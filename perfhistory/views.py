from django.shortcuts import render, render_to_response
from django.template import RequestContext
from perfhistory.models import Project, Tag
from .forms import ProjectForm, TagForm
from django.http import JsonResponse, HttpResponse
import json

# Create your views here.


def project(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		# print '***form:***',form 
		# print '****Request.body:****',request.POST
		# print form.errors
		if form.is_valid():
			print form.cleaned_data
			project = form.save()
		else:
			print 'Invalid Form'
	tagForm = TagForm()
	form = ProjectForm()
	allprojs= Project.objects.all()
	return render(request, 'projects.html', {'form':form,'tagForm':tagForm,'object_list': allprojs, 'type': 'Project'})


def projectdetail(request,project_id):
	project=Project.objects.get(id=project_id)
	return render(request, 'project_details.html', {'project': project})

def chart(request):
	# project=Project.objects.get(id=project_id)
	return render(request, 'chart.html')	

def d3(request):
	# project=Project.objects.get(id=project_id)
	return render(request, 'd3-example-3.html')	

def getTags(request, project_id):
	tags=Tag.objects.filter(project_id_id=project_id)
	results = [ob.as_json() for ob in tags]
	print tags, results
	# print json.dumps(tags.__dict__, default=encode_b)
	# json_tags = [json.dumps(tags.__dict__)]
	# print json_tags
	# return JsonResponse({'tagname':tags.name})
	# return JsonResponse(json_tags)
	return HttpResponse(json.dumps(results), mimetype="application/json")


def encode_b(obj):
 	if isinstance(obj, Tag):
 		return obj.__dict__
 	return obj
