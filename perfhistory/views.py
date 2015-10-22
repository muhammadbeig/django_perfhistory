from django.shortcuts import render, render_to_response
from django.template import RequestContext
from perfhistory.models import Project, Tag
from .forms import ProjectForm

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
	
	form = ProjectForm()
	allprojs= Project.objects.all()
	return render(request, 'projects.html', {'form':form,'object_list': allprojs, 'type': 'Project'})


def projectdetail(request,project_id):
	project=Project.objects.get(id=project_id)
	return render(request, 'project_details.html', {'project': project})

def chart(request):
	# project=Project.objects.get(id=project_id)
	return render(request, 'chart.html')	

def d3(request):
	# project=Project.objects.get(id=project_id)
	return render(request, 'd3-example-2.html')	