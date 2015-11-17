from django.shortcuts import render, render_to_response
from django.template import RequestContext
from perfhistory.models import Project, Tag, Result, Transaction
from .forms import ProjectForm, TagForm
from django.http import JsonResponse, HttpResponse
from django.db import transaction, IntegrityError
from django.core import serializers
import json,sys

# Create your views here.


def project(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		print '***form:***',request.POST 
		print '****Request.body:****',request.POST.get('data')
		# print form.errors
		if form.is_valid():
			print form.cleaned_data
			project = form.save()
		else:
			print 'Invalid Project Form'
	tagForm = TagForm()
	form = ProjectForm()
	allprojs= Project.objects.all()
	return render(request, 'home.html', {'form':form,'tagForm':tagForm,'object_list': allprojs, 'type': 'Project'})

def result(request, projectId, tagId):
	if request.method == 'GET':
		results = Result.objects.filter(project_id=projectId, tag_id=tagId);
		data = []
		for result in results:
			print result.id
			txns = Transaction.objects.filter(result_id=result.id)
			dictionary={}
			dictionary['result']=result
			dictionary['transactions']=[str(t.as_json()) for t in txns] 
			data.append(dictionary)
		print data

		# result = [ob.as_json() for ob in results]
		# fields = [str(ob).split(".")[-1].capitalize() for ob in Result._meta.get_fields()]

		# return HttpResponse(
		            	# json.dumps(result),
		            	# content_type="application/json")
		return render(request, 'result.html', {'object_list': json.dumps(data), 'type': 'Result', 'fields': None})


def createResult(request,project_id,tagid):
	if request.method == 'POST':
		response_data = {}
		insertionresult = []
		

		# print 'request.POST:',request.body, request
		print 'project_id:',project_id, 'tagid:',tagid
		# print request.body
		data = json.loads(request.body)
		if data.get('type') == 'summaryresults':			
			for resultData in data['results']:
				try:
					with transaction.atomic():
						result = Result(project_id=int(project_id), tag_id=int(tagid))
						txns = []
						result.name = resultData['name']
						result.version = resultData['version']
						if resultData.get('baseline'):
							# print 'is baseline'
							result.baseline = True
						print result.save()
						# insertionresultresult.id
						
						for txnData in resultData['data']:
							# print txnData
							txn = Transaction(result_id=result.id)
							txn.name = txnData.get('name')
							txn.description = txnData.get('description')

							txn.successcount = txnData.get('successcount')
							txn.failurecount = txnData.get('failurecount')
							txn.average = txnData.get('average')
							txn.median = txnData.get('median')
							txn.minimum = txnData.get('minimum')
							txn.maximum = txnData.get('maximum')
							txn.stddev = txnData.get('stddev')
							txn.p90 = txnData.get('p90')
							txn.p95 = txnData.get('p95')
							txn.p99 = txnData.get('p99')
							txn.p99_99 = txnData.get('p99_99')
							# txn.save()
							# print txn.as_json()
							txns.append(txn)
						bulkcreatedtxns= Transaction.objects.bulk_create(txns)
						listoftxns= [str(t.as_short_json()) for t in bulkcreatedtxns]
						insertionresult.append({'resultid':result.id, 'txns': listoftxns })
						# print insertionresult
				
				except IntegrityError as e:
					print 'integrity error',e.message
					response_data['message'] = 'Database IntegrityError occurred; ', str(e)
					response_data['status'] = False
					HttpResponse.status_code = 500
					response_data['created_objects'] = None
					return HttpResponse(
		            	json.dumps(response_data),
		            	content_type="application/json")

				except Exception as e:
					print 'exception', e.message
					response_data['message'] = 'Exception occurred; ', e.message
					response_data['status'] = False
					HttpResponse.status_code = 500
					response_data['created_objects'] = None
					return HttpResponse(
		            	json.dumps(response_data),
		            	content_type="application/json")

			response_data['status'] = True
			response_data['message'] = "Create Successful"
			response_data['created_objects'] = insertionresult

		else:
			response_data['message'] = 'Unknown result type; please set a "type" in the request data'
			response_data['status'] = False
			response_data['created_objects'] = None
			HttpResponse.status_code = 500

		return HttpResponse(json.dumps(response_data),
		            		content_type="application/json")
	return HttpResponse(
		            json.dumps({'status':False,'message':"Request method "+request.method+" not supported"}),
		            content_type="application/json")

def createTag(request,project_id):
	# print 'project_id in form', project_id
	if request.method == 'POST':
		form = TagForm(request.POST)
		print '****Request.body:****',request.POST
		if form.is_valid():
			response_data = {}
			tag = form.save(commit=False)
			tag.project_id = int(project_id)
			tag.save()
			response_data['project_id'] = tag.project_id
			response_data['status'] = True
			response_data['message'] = 'Create Tag successful!'
			response_data['tag_id'] = tag.id
			response_data['tag_name'] = tag.name
			response_data['tag_description'] = tag.description
			response_data['created'] = tag.created.strftime('%B %d, %Y %I:%M %p')
			return HttpResponse(
		            json.dumps(response_data),
		            content_type="application/json"
		        )
		else:
			print 'Invalid Tag Form'
			print form.errors
			return HttpResponse(
	            json.dumps({"status":False,
	            	"message": "Invalid Tag Form"}),
	            content_type="application/json"
	        )
	else:
		return HttpResponse(
	            json.dumps({"Error": "Only POST method is allowed"}),
	            content_type="application/json"
	        )
	# tagForm = TagForm()
	# form = ProjectForm()
	# allprojs= Project.objects.all()
	# return render(request, 'projects.html', {'form':form,'tagForm':tagForm,'object_list': allprojs, 'type': 'Project'})


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
	tags=Tag.objects.filter(project_id=project_id)
	results = [ob.as_json() for ob in tags]
	# print tags, results
	# print json.dumps(tags.__dict__, default=encode_b)
	# json_tags = [json.dumps(tags.__dict__)]
	# print json_tags
	# return JsonResponse({'tagname':tags.name})
	# return JsonResponse(json_tags)
	return HttpResponse(json.dumps(results), content_type="application/json")


def encode_b(obj):
 	if isinstance(obj, Tag):
 		return obj.__dict__
 	return obj
