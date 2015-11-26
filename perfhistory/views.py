from django.shortcuts import render, render_to_response
from django.template import RequestContext
from perfhistory.models import Project, Tag, Result, Transaction
from .forms import ProjectForm, TagForm, EditProjectForm
from django.http import JsonResponse, HttpResponse, QueryDict
from django.db import transaction, IntegrityError
from django.core import serializers
import json,sys

# Create your views here.


def deleteProject (request, projectId):
	response_data = {}
	tagForm = TagForm()
	projectform = ProjectForm()
	editprojectform = EditProjectForm()
	allprojs= Project.objects.all()
	project = Project.objects.get(id=projectId)
	if request.method == 'DELETE': 
		print 'method is delete'
		if project:
			try:
				with transaction.atomic():
					childTags = Tag.objects.filter(project_id=project.id)
					for tag in childTags:
						childResults = Result.objects.filter(project_id=projectId, tag_id=tag.id);
						for result in childResults:
							Transaction.objects.filter(result_id=result.id).delete()
							result.delete()
						tag.delete()
					project.delete()

					
					response_data['message'] = 'Project and its children deleted'
					response_data['status'] = True
					# response_data['created_objects'] = None

			except IntegrityError as e:
				print 'Integrity error',e.message
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
		else:
			print "Project doesn't exist for id"
			return HttpResponse(json.dumps({'status':False,'message':"Project doesn't exist for id"}),
		            content_type="application/json")
	
	return HttpResponse(json.dumps(response_data),
		            		content_type="application/json")

def project(request):
	tagForm = TagForm()
	projectform = ProjectForm()
	editprojectform = EditProjectForm()
	allprojs= Project.objects.all().order_by('-last_modified')
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		# print '***request.POST:***',request.POST 
		# print '****request.POST.get:****',request.POST.get('data')
		# print form.errors
		if form.is_valid():
			print form.cleaned_data
			project = form.save()
		else:
			print 'Invalid Project Form'
	if request.method == 'PUT': #update case
		data = QueryDict(request.body)
		# print '***form PUT (POST):***', data
		project = Project.objects.get(id=data['id'])
		form = ProjectForm(data, instance=project)
		if form.is_valid():
			print form.cleaned_data
			project = form.save()
		else:
			print 'Invalid Project Form'
		allprojs= Project.objects.all() #to get an updated list
	

	
	return render(request, 'home.html', {'projectform':projectform,  'tagForm':tagForm,'object_list': allprojs, 'type': 'Project'})
	

def result(request, projectId, tagId):
	if request.method == 'GET':
		projectobj = Project.objects.get(id=projectId);
		tagobj = Tag.objects.get(id=tagId);
		results = Result.objects.filter(project_id=projectId, tag_id=tagId).order_by('created');
		data = []
		result_list = [] 
		alltxns = []
		for result in results:
			print result.id
			txns = Transaction.objects.filter(result_id=result.id)
			dictionary={'result': result.as_json(), 'transactions':[t.as_json() for t in txns]}
			data.append(dictionary)
			result_list.append(result.as_json())
			alltxns.extend([t.as_json() for t in txns])

	return render(request, 'result.html', {'object_list': json.dumps(data), 'type': 'Transaction', 'allresults':results, 'result_list': json.dumps(result_list), 'txn_list':json.dumps(alltxns), 'projectobj':projectobj, 'tagobj':tagobj })


# def ResultListView(FormMixin, ListView):


def updateResult(request, resultId):
	if request.method == 'PUT':
		data = QueryDict(request.body)
		print data

		response_data = {}
		try:
			with transaction.atomic():
				result = Result.objects.get(id=resultId)
				projectId = result.project_id;
				tagId = result.tag_id;
				if result:
					updatedObjects = []
					if data.get('baseline') is not None:
						print 'data.get(baseline):',data.get('baseline')
						print 'data.get(baseline):',data.get('baseline')
						baseline = int(data.get('baseline'))
						print 'data.get(baseline):',data.get('baseline')

						if baseline is 1: # is TRUE
							# print 'baseline is true:', baseline
							if not result.baseline: #don't do all this i.e. make it (result.baseline) true if it is already true
								result.baseline = True
								for res in Result.objects.filter(project_id=projectId, tag_id=tagId):
									if res.id is not resultId:
										res.baseline = False
										res.save()
										updatedObjects.append(res.as_json());
						else: # baseline is FALSE
							# print 'baseline is false:',baseline
							if result.baseline: # don't make it false if its already false
								result.baseline = False

					if data.get('version'):
						result.version = data['version'];
					if data.get('name'):
						result.name = data['name'];
					if data.get('description'):
						result.description = data['description'];
					if data.get('numberofusers'):
						result.numberofusers = data['numberofusers'];

					
					print 'result =>', result.as_json()
					result.save()


					print 'result.baseline =', result.baseline
					updatedObjects.append(result.as_json());

					response_data['updated_objects'] = updatedObjects
					response_data['status'] = True
					HttpResponse.status_code = 200
					response_data['message'] = "Result(s) updated successfully"

		except IntegrityError as e:
			print 'Integrity error',e.message
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
		return HttpResponse(
		            	json.dumps(response_data),
		            	content_type="application/json")

	if request.method == 'DELETE':
		print 'delete request for resultid:',resultId

		response_data = {}
		try:
			with transaction.atomic():
				result = Result.objects.get(id=resultId)
				deletedObjects = [] 
				if result:
					for txn in Transaction.objects.filter(result_id=result.id):
						txn.delete()
						deletedObjects.append(txn.as_json());
					result.delete()
					deletedObjects.append(result.as_json())
					response_data['deleted_objects'] = deletedObjects
					response_data['status'] = True
					HttpResponse.status_code = 200
					response_data['message'] = "Result deleted successfully"
		except IntegrityError as e:
			print 'Integrity error',e.message
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
		return HttpResponse(
		            	json.dumps(response_data),
		            	content_type="application/json")


	


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
							txn.p99_9 = txnData.get('p99.9')
							txn.p99_99 = txnData.get('p99.99')
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
	print 'project_id in form', project_id
	if request.method == 'POST':
		form = TagForm(request.POST)
		print '****Request.POST:****',request.POST
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
			HttpResponse.status_code = 500
			return HttpResponse(
	            json.dumps({"status":False,
	            	"message": form.errors}),
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
	return render(request, 'result_upload.html')	



def getTags(request, project_id):
	tags=Tag.objects.filter(project_id=project_id)
	results = [ob.as_json() for ob in tags]
	HttpResponse.status_code = 200
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
