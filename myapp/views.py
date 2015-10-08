from django.shortcuts import render_to_response, render
from django.template import RequestContext
from myapp.models import Project, Tag

from .forms import ProjectForm



def project_new(request):
	form = ProjectForm()
	return render(request, 'project_edit.html', {'form':form})



def projects(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		print '***form:***',form 
		print '****Request.body:****',request.POST
		print form.errors
		if form.is_valid():
			print form.cleaned_data
		else:
			print 'Invalid Form'
	
	form = ProjectForm()
	allprojs= Project.objects.all()
	return render(request, 'projects.html', {'form':form,'object_list': allprojs, 'type': 'Project'})

	
def tags(request):
	context = RequestContext(request)
	alltags= Tag.objects.all()
	
	return render_to_response('tags.html', { 'object_list': alltags, 'type': 'Tag' }, context)
	