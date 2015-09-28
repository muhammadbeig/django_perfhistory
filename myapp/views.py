from django.shortcuts import render_to_response
from django.template import RequestContext
from myapp.models import Project, Tags


def index(request):
	context = RequestContext(request)
	allprojs= Project.objects.all()
    	return render_to_response('index.html', { 'an_attrib': allprojs }, context)