from django.shortcuts import render_to_response
from django.template import RequestContext
from myapp.models import Project, Tag

from .forms import ProjectForm





def projects(request):
	if request.method == 'POST':
		# try:
		# except:
		form = ProjectForm(request.POST)
		print 'Request.POST:',request.body
		if form.is_valid():
			print form.cleaned_data
		else:
			print 'Invalid Form'

	context = RequestContext(request)
	allprojs= Project.objects.all()
	
	return render_to_response('projects.html', { 'object_list': allprojs, 'type': 'Project' }, context)
	
def tags(request):
	context = RequestContext(request)
	alltags= Tag.objects.all()
	
	return render_to_response('tags.html', { 'object_list': alltags, 'type': 'Tag' }, context)
	