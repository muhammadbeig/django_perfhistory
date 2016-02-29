from django.shortcuts import render, render_to_response
from django.template import RequestContext
from perfhistory.models import Project, Tag, Result, Transaction
from .forms import ProjectForm, TagForm, EditProjectForm, UserForm, TransactionForm
from django.http import JsonResponse, HttpResponse, QueryDict, HttpResponseRedirect, Http404
from django.db import transaction, IntegrityError
from django.core import serializers
import json,sys,datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

APPLICATION = 'perfhistory'
# Create your views here.


def logoutView(request):
    logout(request)
    form = UserForm(request.POST or None)
    HttpResponse.status_code = 200

    return render(request, 'login.html', {'userform': form })

def loginView(request):
	# request.session.set_test_cookie()
	# visits = int( request.COOKIES.get('visits', '0') )
	# if request.COOKIES.has_key('last_visit' ):
	# 	last_visit = request.COOKIES['last_visit']
	# 	# the cookie is a string - convert back to a datetime type
	# 	last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
	# 	curr_time = datetime.now()
	# 	if (curr_time-last_visit_time).days > 0:
	# 	# if at least one day has gone by then inc the visit count.
	# 		response.set_cookie('visits', visits + 1 )
	# 		response.set_cookie('last_visit', datetime.now())
	# 	else:
	# 		response.set_cookie('last_visit', datetime.now())
	
	# if request.COOKIES.has_key( 'visits' ):
	# 	v = request.COOKIES[ 'visits' ]
	# else:
	# 	v = 0
	# print v

	# if request.COOKIES.has_key( 'last_visit' ):
	# 	lv = request.COOKIES[ 'last_visit' ]
	# else:
	# 	lv = datetime.datetime.now().strftime( "%Y-%m-%d %H:%M:%S")
	# 	# response.set_cookie('last_visit', lv)
	


	if request.user.is_authenticated() is not True:
	    form = UserForm(request.POST or None)
	    nexturl = request.GET.get('next') or 'projects'
	    if request.POST:
	    	if form.is_valid():
	        	user = form.login(request)
	        	
	        	# if request.POST.get('next') is not None:
	        	nexturl = request.POST.get('next') or 'projects'

	        	if user:
	        		login(request, user)
	            	return HttpResponseRedirect(nexturl)
	            	# if nexturl is not None:
	            	# 	return HttpResponseRedirect(nexturl)
	            	# else:
	            	# 	return HttpResponseRedirect("projects")# Redirect to a success page.
	    	else:
	    		print form.errors

	    nexturl = nexturl if nexturl else ''
	    return render(request, 'login.html', {'userform': form,  'next':nexturl }) #'visits':v, 'lastvisit':lv,
	else:
	    return project(request)


def deleteTagObject(tag, projectId):
	try:
		childResults = Result.objects.filter(project_id=projectId, tag_id=tag.id);
		for result in childResults:
			Transaction.objects.filter(result_id=result.id).delete()
			result.delete()
		tag.delete()
	except Exception as e:
		print 'Exception occurred while deleting tag with id: %s, projectid: %s. Message: %s' % (tagId, projectId, e.message)



@login_required(login_url='/'+APPLICATION+'/')
def deleteProject (request, projectId):
	user = request.user
	if user.has_perm(APPLICATION+'.delete_project'):
		response_data = {}
		tagForm = TagForm()
		projectform = ProjectForm()
		editprojectform = EditProjectForm()
		allprojs= Project.objects.all()
		project = Project.objects.get(id=projectId)
		if request.method == 'DELETE': 
			# print 'method is delete'
			if project:
				try:
					with transaction.atomic():
						childTags = Tag.objects.filter(project_id=project.id)
						for tag in childTags:
							deleteTagObject(tag,projectId)
							# childResults = Result.objects.filter(project_id=projectId, tag_id=tag.id);
							# for result in childResults:
							# 	Transaction.objects.filter(result_id=result.id).delete()
							# 	result.delete()
							# tag.delete()
						project.delete()

						response_data['message'] = 'Project and its children deleted'
						response_data['status'] = True
						response_data['project_id'] = projectId
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
	else:
		return returnJsonWithResponseTextCodeAndStatus('Insufficient permissions', 403, False)

@login_required(login_url='/'+APPLICATION+'/')
def project(request):
	# print request.user.has_perm('perfhistory.change_project')
	# if request.session.test_cookie_worked():
	# 	print "The test cookie worked!!!"
	# 	request.session.delete_test_cookie()
	user = request.user
	# print 'user:',request.user.email
	tagForm = TagForm()
	projectform = ProjectForm(request.POST or None)
	editprojectform = EditProjectForm()
	allprojs= Project.objects.all().order_by('-last_modified')
	
	if request.method == 'POST':
		if user.has_perm(APPLICATION+'.add_project'):
			if projectform.is_valid():
				project = projectform.save()
			else:
				# print 'Invalid Project Form, POST'
				returnJsonWithResponseTextCodeAndStatus('Invalid Project Form', 500, False)
		else:
			return returnJsonWithResponseTextCodeAndStatus('Insufficient permissions', 403, False)
	
	
	if request.method == 'PUT': #update case
		if user.has_perm(APPLICATION+'.change_project'):
			data = QueryDict(request.body)
			# print '***form PUT (POST):***', data
			project = Project.objects.get(id=data['id'])
			form = ProjectForm(data, instance=project)
			if form.is_valid():
				print form.cleaned_data
				project = form.save()
			else:
				print 'Invalid Project Form, PUT'
			# allprojs= Project.objects.all() #to get an updated list
			response_data = {}
			response_data['message'] = 'Project updated'
			response_data['status'] = True
			# response_data['project_id'] = project.id
			# response_data['project_name'] = project_name
			# response_data['project_description'] = project_description
			HttpResponse.status_code = 200
			response_data['updated_object'] = project.as_json()
			return HttpResponse(
			            json.dumps(response_data),
			            content_type="application/json")
		else:
			return returnJsonWithResponseTextCodeAndStatus('Insufficient permissions', 403, False)
	
	return render(request, 'projects.html', {'projectform':projectform,  'tagForm':tagForm,'object_list': allprojs, 'type': 'Project'})
	

@login_required(login_url='/'+APPLICATION+'/')
def showComparisonChart(request, projectId, tagId, limit=99999):
	limit = int(limit)
	compare_by = request.GET.get('compareby', None);
	exclude = request.GET.get('exclude', None);
	show_only = request.GET.get('showonly', None);
	limit_qp = request.GET.get('limit', None);
	if not limit_qp:
		limit_qp = None
	else:
		try:
			l=int(limit_qp)
			limit=l
		except Exception as e:
			print e.message, "continuing with limit provided in the url:", limit
	if not exclude:
		exclude = None
	if not compare_by:
		compare_by = None
	if not show_only:
		show_only = None		

	if request.method == 'GET':
		projectobj = Project.objects.get(id=projectId);
		tagobj = Tag.objects.get(id=tagId);
		results = Result.objects.filter(project_id=projectId, tag_id=tagId);
		# print results
		# baseline_result = None 
		# new_results = []
		
		# print len(results)
		# separating baseline result and other results
		# for r in results:
		# 	# print r.version, r.baseline,
		# 	if r.baseline:
		# 		baseline_result = r
		# 	else:
		# 		new_results.append(r)
		# # print len(new_results)
		# results = new_results

		# sorting by version with assumption that version is an int/float and no other characters
		try:
			results = sorted(results, key=lambda x: float(x.version), reverse=False)
		except Exception as e:
			print e.message, 'so sorting results by version as a text instead of float'
			results = sorted(results, key=lambda x: x.version, reverse=False)			
		results = results[-limit:] if len(results) > limit else results
		if limit > 99: 
			limit = "all results"
		else:
			limit = "last %s results" % limit

		# inserting baseline at the start of results array
		# if baseline_result and results:
		# 	results.insert(0,baseline_result)

		data = []
		result_list = [] 
		alltxns = []
		for result in results:
			# print result.version,
			txns = Transaction.objects.filter(result_id=result.id)
			dictionary={'result': result.as_json(), 'transactions':[t.as_json() for t in txns]}
			data.append(dictionary)
			result_list.append(result.as_json())
			alltxns.extend([t.as_json() for t in txns])

		#result_list has list of all results, only results (as_json)
		#alltxns has all transactions for all results, sorted as results is (^^ version)
		#object_list or data is an array of dictionaries, each dictionary contains result and an array of its txns

	return render(request, 'comparisonChart.html', {'object_list': json.dumps(data), 'showonly':show_only, 'exclude':exclude, 'compareby':compare_by, 'limit': limit, 'type': 'Transaction', 'allresults':results, 'result_list': json.dumps(result_list), 'transactions':json.dumps(alltxns), 'projectobj':projectobj, 'tagobj':tagobj })



@login_required(login_url='/'+APPLICATION+'/')
def comparisonChart(request, projectId, tagId):
	limit = 15
	if request.method == 'GET':
		projectobj = Project.objects.get(id=projectId);
		tagobj = Tag.objects.get(id=tagId);
		results = Result.objects.filter(project_id=projectId, tag_id=tagId);
		# print results
		baseline_result = None 
		new_results = []
		
		print len(results)
		for r in results:
			# print r.version, r.baseline,
			if r.baseline:
				baseline_result = r
			else:
				new_results.append(r)
		print len(new_results)
		results = new_results

		# sorting by version with assumption that version is an int/float and no other characters
		results = sorted(results, key=lambda x: float(x.version), reverse=False)
		results = results[-limit:] if len(results) > limit else results

		if baseline_result and results:
			results.insert(0,baseline_result)

		data = []
		result_list = [] 
		alltxns = []
		for result in results:
			# print result.id
			txns = Transaction.objects.filter(result_id=result.id)
			dictionary={'result': result.as_json(), 'transactions':[t.as_json() for t in txns]}
			data.append(dictionary)
			result_list.append(result.as_json())
			alltxns.extend([t.as_json() for t in txns])


	
	return render(request, 'comparisonChart.html', {'object_list': json.dumps(data), 'type': 'Transaction', 'allresults':results, 'result_list': json.dumps(result_list), 'transactions':json.dumps(alltxns), 'projectobj':projectobj, 'tagobj':tagobj })


@login_required(login_url='/'+APPLICATION+'/')
def comparisonChartbyVersion(request, projectId, tagId):
	if request.method == 'GET':
		projectobj = Project.objects.get(id=projectId);
		tagobj = Tag.objects.get(id=tagId);
		results = Result.objects.filter(project_id=projectId, tag_id=tagId)#.order_by("version");
		# sorting by version with assumption that version is an int/float and no other characters
		try:
			results = sorted(results, key=lambda x: float(x.version), reverse=False)
		except Exception as e:
				print e.message, 'so sorting results by create date instead of version'
				results = sorted(results, key=lambda x: x.version, reverse=False)
		data = []
		result_list = [] 
		alltxns = []
		for result in results:
			# print result.id
			txns = Transaction.objects.filter(result_id=result.id)
			dictionary={'result': result.as_json(), 'transactions':[t.as_json() for t in txns]}
			data.append(dictionary)
			result_list.append(result.as_json())
			alltxns.extend([t.as_json() for t in txns])


	
	return render(request, 'comparisonChartbyVersion.html', {'object_list': json.dumps(data), 'type': 'Transaction', 'allresults':results, 'result_list': json.dumps(result_list), 'transactions':json.dumps(alltxns), 'projectobj':projectobj, 'tagobj':tagobj })


@login_required(login_url='/'+APPLICATION+'/')
def result(request, projectId, tagId):
	transactionForm = TransactionForm(result_qs=Result.objects.filter(tag_id=tagId))

	# Get all projects and build a map with projects along with their tags
	allprojects = []
	for p in Project.objects.all():
		print p.name
		projectDic = {}
		projectDic["name"] = p.name
		projectDic["id"] = p.id
		tags = Tag.objects.filter(project_id=p.id)
		projectDic["tags"] = []
		for t in tags:
			tagDic={}
			tagDic["name"]=t.name
			tagDic["id"]=t.id
			projectDic["tags"].append(tagDic)
		allprojects.append(projectDic)
	print 'All projects dictionary:', allprojects


	# print transactionForm
	try:
		if request.method == 'GET':
			projectobj = Project.objects.get(id=projectId);
			tagobj = Tag.objects.get(id=tagId);
			results = Result.objects.filter(project_id=projectId, tag_id=tagId);
			try:
			# sorting by version with assumption that version is an int/float and no other characters
				results = sorted(results, key=lambda x: float(x.version), reverse=False)
			except Exception as e:
				print e.message, 'so sorting results by create date instead of version'
				results = sorted(results, key=lambda x: x.version, reverse=False)
			data = []
			result_list = [] 
			alltxns = []
			for result in results:
				# print result.id
				txns = Transaction.objects.filter(result_id=result.id)
				dictionary={'result': result.as_json(), 'transactions':[t.as_json() for t in txns]}
				data.append(dictionary)
				result_list.append(result.as_json())
				alltxns.extend([t.as_json() for t in txns])
		if request.method == 'POST':
			return addTransactionToResult(request, project_id, tagId);

	except Exception as e:
		raise Http404(e.message)
		# return returnJsonWithResponseTextCodeAndStatus(e.message, 500, False)

	return render(request, 'result.html', {'allprojects':json.dumps(allprojects), 'object_list': json.dumps(data), 'type': 'Transaction', 'allresults':results, 'result_list': json.dumps(result_list), 'txn_list':json.dumps(alltxns), 'projectobj':projectobj, 'tagobj':tagobj, 'transactionForm':transactionForm })

def makeTxnObjectForResult(result, txnData):
	try:
		txn = Transaction(result_id=result.id)
		txn.name = txnData.get('name')
		txn.description = txnData.get('description')
		txn.success_count = txnData.get('successcount')
		txn.failure_count = txnData.get('failurecount')
		txn.responsetime_average = txnData.get('average')
		txn.responsetime_median = txnData.get('median')
		txn.responsetime_minimum = txnData.get('minimum')
		txn.responsetime_maximum = txnData.get('maximum')
		txn.responsetime_stddev = txnData.get('stddev')
		txn.responsetime_p90 = txnData.get('p90')
		txn.responsetime_p95 = txnData.get('p95')
		txn.responsetime_p99 = txnData.get('p99')
		txn.responsetime_p99_9 = txnData.get('p99.9')
		txn.responsetime_p99_99 = txnData.get('p99.99')
		txn.success_qps = ( txnData.get('successcount') / (result.duration_minutes * 60.0) ) if txnData.get('successcount') else None;
		txn.failure_qps = ( txnData.get('failurecount') / (result.duration_minutes * 60.0) ) if txnData.get('failurecount') else None;
	except Exception as e:
		print 'Exception occurred, could be a malformed input json or bad data type. ' + e.message +' line:' +str(sys.exc_traceback.tb_lineno)
		return returnJsonWithResponseTextCodeAndStatus('Exception occurred, could be a malformed input json or bad data type' + e.message, 500, False)

	return txn

@login_required
def addTransactionToResult(request, resultId):
	response_data = {}
	try:
		resId=QueryDict(request.body)['result']
		print 'resId:', resId
		form = TransactionForm(request.POST,result_qs=Result.objects.get(id=resId))
		
		print 'form:', QueryDict(request.body)['result']
		# print form.errors, 
		print form
		# print 'form.is_valid():', form.is_valid()
	except Exception as e:
		print "an exception occurred", e.message

	
	try:
		with transaction.atomic():
			if request.method == 'POST':
				result = Result.objects.get(id=resultId)
				Project.objects.get(id=result.project_id).save()
				Tag.objects.get(id=result.tag_id).save()
				txn = makeTxnObjectForResult(result, txnData);
				txn.save()
	except Exception as e:
		print 'exception', e.message
		response_data['message'] = 'Exception occurred; ', e.message
		response_data['status'] = False
		HttpResponse.status_code = 500
		response_data['created_objects'] = None
		return HttpResponse(
			    json.dumps(response_data),
			    content_type="application/json")

	return render(request, 'result.html', {'object_list': json.dumps(data), 'type': 'Transaction', 'allresults':results, 'result_list': json.dumps(result_list), 'txn_list':json.dumps(alltxns), 'projectobj':projectobj, 'tagobj':tagobj, 'transactionForm':transactionForm })

@login_required(login_url='/'+APPLICATION+'/')
def updateResult(request, resultId):
	user = request.user
	if user.has_perm(APPLICATION+'.change_result'):
		if request.method == 'PUT':
			data = QueryDict(request.body)
			# print data

			response_data = {}
			try:
				with transaction.atomic():
					result = Result.objects.get(id=resultId)
					projectId = result.project_id;
					tagId = result.tag_id;
					if result:
						updatedObjects = []
						if data.get('baseline') is not None:
							# print 'data.get(baseline):',data.get('baseline')
							# print 'data.get(baseline):',data.get('baseline')
							baseline = int(data.get('baseline'))
							# print 'data.get(baseline):',data.get('baseline')

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

						
						# print 'result =>', result.as_json()
						result.save()


						# print 'result.baseline =', result.baseline
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
	else:
		return returnJsonWithResponseTextCodeAndStatus('Insufficient permissions', 403, False)

	if user.has_perm(APPLICATION+'.delete_result'):
		if request.method == 'DELETE':
			# print 'delete request for resultid:',resultId

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
	else:
		return returnJsonWithResponseTextCodeAndStatus('Insufficient permissions', 403, False)



@login_required(login_url='/'+APPLICATION+'/')
def createResultByProjectTagName(request):
	user = request.user

	if user.has_perm(APPLICATION+'.add_result'):	
		data = json.loads(request.body)
		# print data
		try:
			# print request.body
			projectName = data.get('project_name')
			project = Project.objects.get(name=projectName)
		except Project.DoesNotExist as e:
			print 'Invalid project name:', projectName, 'Exception:', e
			raise Http404('Invalid project name:', projectName, 'Exception:', e.message)
		try:
			tagName = data.get('tag_name')
			tag = Tag.objects.get(name=tagName, project_id=project.id)
		except Tag.DoesNotExist as e:
			print 'Invalid tag name:', tagName, 'Exception:', e
			raise Http404('Invalid tag name:', tagName, 'Exception:', e.message)

		return createResult(request, project.id, tag.id)
	else:
		return returnJsonWithResponseTextCodeAndStatus('Insufficient permissions', 403, False)


	

@login_required(login_url='/'+APPLICATION+'/')
def createResult(request, project_id, tagid):
	user = request.user

	if user.has_perm(APPLICATION+'.add_result'):	
		if request.method == 'POST':
			response_data = {}
			insertionresult = []
			try:
				existingResults = Result.objects.filter(project_id=int(project_id), tag_id=int(tagid))
			except Result.DoesNotExist as e:
				existingResults = None
				print 'Exception (ignorable?):', e

			# print 'request.POST:',request.body, request
			# print 'project_id:',project_id, 'tagid:',tagid
			# print request.body
			# print 'file read time:',request.META.get('HTTP_FILEREADTIME')

			data = json.loads(request.body)
			if data.get('type') == 'summaryresults':			
				for resultData in data['results']:
					try:
						with transaction.atomic():
							result = Result(project_id=int(project_id), tag_id=int(tagid))
							Project.objects.get(id=int(project_id)).save()
							Tag.objects.get(id=int(tagid)).save()
							txns = []
							result.name = resultData['name']
							result.version = resultData['version']
							result.numberofusers = resultData.get('numberofusers')
							result.filename = resultData.get('filename')
							result.duration_minutes = round(resultData.get('duration_minutes'),1)
							if resultData.get('start_time'):
								result.start_time = resultData['start_time']
							result.description = resultData.get('description')
							# print 'here', existingResults, len(existingResults)
							if resultData.get('baseline') or existingResults is None or len(existingResults) == 0:
								# print 'is baseline'
								result.baseline = True
								if existingResults is not None:
									for res in existingResults:#Result.objects.filter(project_id=int(project_id), tag_id=int(tagid)):
										res.baseline = False
										res.save()
							result.save()
							# insertionresultresult.id
							
							for txnData in resultData['data']:
								# print json.dumps(txnData)
								txn = makeTxnObjectForResult(result, txnData);
								# txn = Transaction(result_id=result.id)
								# txn.name = txnData.get('name')
								# txn.description = txnData.get('description')

								# txn.success_count = txnData.get('successcount')
								# txn.failure_count = txnData.get('failurecount')
								# txn.responsetime_average = txnData.get('average')
								# txn.responsetime_median = txnData.get('median')
								# txn.responsetime_minimum = txnData.get('minimum')
								# txn.responsetime_maximum = txnData.get('maximum')
								# txn.responsetime_stddev = txnData.get('stddev')
								# txn.responsetime_p90 = txnData.get('p90')
								# txn.responsetime_p95 = txnData.get('p95')
								# txn.responsetime_p99 = txnData.get('p99')
								# txn.responsetime_p99_9 = txnData.get('p99.9')
								# txn.responsetime_p99_99 = txnData.get('p99.99')
								# txn.success_qps = txnData.get('successcount') / (result.duration_minutes * 60.0);
								# txn.failure_qps = txnData.get('failurecount') / (result.duration_minutes * 60.0);
								## print ('successcount',txnData.get('successcount'),'duration_minutes:',result.duration_minutes, 'success qps:',txnData.get('successcount') / (3600 * 60.00));
								## txn.save()
								## print txn.as_json()
								txns.append(txn)
							bulkcreatedtxns= Transaction.objects.bulk_create(txns)
							listoftxns= [str(t.as_short_json()) for t in bulkcreatedtxns]
							insertionresult.append({'resultid':result.id, 'txns': listoftxns })
							# print insertionresult
					
					except IntegrityError as e:
						print 'integrity error',e.message
						response_data['detailed_message'] = 'Database IntegrityError occurred; ', str(e)
						if "UNIQUE constraint failed" in e.message:
							response_data['message'] = 'Duplicate result upload failed, another result with the same name and version exists in the same tag under the same project'
						else:
							response_data['message'] = 'Database integrity error while result upload, upload failed.'
						response_data['status'] = False
						HttpResponse.status_code = 500
						response_data['created_objects'] = None
						return HttpResponse(
			            	json.dumps(response_data),
			            	content_type="application/json")

					except Exception as e:
						print 'exception', e.message, 'line:', sys.exc_traceback.tb_lineno 
						response_data['message'] = 'Exception occurred;', e.message, 'line:',sys.exc_traceback.tb_lineno 
						response_data['status'] = False
						HttpResponse.status_code = 500
						response_data['created_objects'] = None
						return HttpResponse(
			            	json.dumps(response_data),
			            	content_type="application/json")

				response_data['status'] = True
				response_data['message'] = "Create Successful"
				response_data['created_objects'] = insertionresult
				HttpResponse.status_code = 200

			else:
				response_data['message'] = 'Unknown result type; please set a "type" in the request data (acceptable types: summaryresults)'
				response_data['status'] = False
				response_data['created_objects'] = None
				HttpResponse.status_code = 500

			return HttpResponse(json.dumps(response_data),
			            		content_type="application/json")
	else:
		return returnJsonWithResponseTextCodeAndStatus('Insufficient permissions', 403, False)

	return HttpResponse(
		            json.dumps({'status':False,'message':"Request method "+request.method+" not supported"}),
		            content_type="application/json")

@login_required(login_url='/'+APPLICATION+'/')
def deleteTag(request, projectId, tagId):
	user = request.user
	if request.method == 'DELETE':
		if user.has_perm(APPLICATION+'.delete_tag'):
			try:
				with transaction.atomic():
					project = Project.objects.get(id=projectId)
					tag = Tag.objects.get(id=tagId)
					if project and tag:
						tagasjson = tag.as_json()
						deleteTagObject(tag, projectId);
						response_data = {}
						response_data['message'] = 'Tag deleted'
						response_data['status'] = True
						HttpResponse.status_code = 200
						response_data['deleted_object'] = tagasjson
						return HttpResponse(json.dumps(response_data),content_type="application/json")
					else:
						return returnJsonWithResponseTextCodeAndStatus('Invalid project and/or tag', 404, False)
			except IntegrityError as e:
				print 'Integrity error',e.message
				response_data['message'] = 'Database IntegrityError occurred; ', str(e)
				response_data['status'] = False
				HttpResponse.status_code = 500
				response_data['deleted_object'] = None
				return HttpResponse(
		            	json.dumps(response_data),
		            	content_type="application/json")

			except Exception as e:
				print 'exception', e.message
				response_data['message'] = 'Exception occurred; ', e.message
				response_data['status'] = False
				HttpResponse.status_code = 500
				response_data['deleted_object'] = None
				return HttpResponse(
		            	json.dumps(response_data),
		            	content_type="application/json")
	
		else:
			return returnJsonWithResponseTextCodeAndStatus('Insufficient permissions', 403, False)
	return returnJsonWithResponseTextCodeAndStatus('Invalid method', 500, False)

@login_required(login_url='/'+APPLICATION+'/')
def updateTag(request):
	user = request.user
	if request.method == 'POST': #update case
		if user.has_perm(APPLICATION+'.change_tag'):
			data = QueryDict(request.body)
			print '***form (POST):***', data
			tag = Tag.objects.get(id=data['id'])
			form = TagForm(data, instance=tag)
			if form.is_valid():
				print 'form is valid: ', form.cleaned_data
				tag = form.save()
			else:
				print 'Invalid Tag Form, POST'
			response_data = {}
			response_data['message'] = 'Tag updated'
			response_data['status'] = True
			# response_data['tagform'] = form
			HttpResponse.status_code = 200
			response_data['updated_object'] = tag.as_json()
			return HttpResponse(
			            json.dumps(response_data),
			            content_type="application/json")
		else:
			return returnJsonWithResponseTextCodeAndStatus('Insufficient permissions', 403, False)

	# return render(request, 'tags.html', { 'tagForm':tagForm,'object_list': allprojs, 'type': 'Project'})
	return HttpResponse(
	            json.dumps(response_data),
	            content_type="application/json")

@login_required(login_url='/'+APPLICATION+'/')
def createTag(request,project_id):
	user = request.user
	if user.has_perm(APPLICATION+'.add_tag'):	
		# print 'project_id in form', project_id
		try:
			if request.method == 'POST':
				form = TagForm(request.POST)
				# print '****Request.POST:****',request.POST
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
					# print form.errors
					HttpResponse.status_code = 500
					return HttpResponse(
			            json.dumps({"status":False, 'project_id':project_id,
			            	"message": form.errors}),
			            content_type="application/json"
			        )
			else:
				return HttpResponse(
			            json.dumps({"Error": "Only POST method is allowed"}),
			            content_type="application/json"
			        )
		except IntegrityError as e:
			print 'Integrity error',e
			response_data['message'] = {'Database IntegrityError': ['Duplicate entry, another tag with this name exists in the same context']}
			response_data['status'] = False
			HttpResponse.status_code = 500
			response_data['project_id'] = project_id
			return HttpResponse(
			            	json.dumps(response_data),
			            	content_type="application/json")
		except Exception as e:
			print 'exception', e.message
			response_data['message'] = 'Exception occurred; ', e.message
			response_data['status'] = False
			HttpResponse.status_code = 500
			response_data['project_id'] = project_id
			return HttpResponse(
			            	json.dumps(response_data),
			            	content_type="application/json")
		# tagForm = TagForm()
		# form = ProjectForm()
		# allprojs= Project.objects.all()
		# return render(request, 'projects.html', {'form':form,'tagForm':tagForm,'object_list': allprojs, 'type': 'Project'})
	else:
		return returnJsonWithResponseTextCodeAndStatus('Insufficient permissions', 403, False)

@login_required(login_url='/'+APPLICATION+'/')
def projectdetail(request,project_id):
	project=Project.objects.get(id=project_id)
	return render(request, 'project_details.html', {'project': project})

def chart(request):
	# project=Project.objects.get(id=project_id)
	return render(request, 'd3-example.html')	

def d3(request):
	# project=Project.objects.get(id=project_id)
	data = request.body;
	# print json.dumps(request.body)
	# print "**** d3 request was made:", request.method, "*****"
	# print request.body
	# print request.POST
	if request.method == "POST":
		data=request.POST;

	return render(request, 'my_base.html', {'transactions': request.body})	



def getTags(request, project_id):
	tags=Tag.objects.filter(project_id=project_id).order_by('-last_modified', 'name')
	results = [ob.as_json() for ob in tags]
	HttpResponse.status_code = 200
	# print tags, results
	# print json.dumps(tags.__dict__, default=encode_b)
	# json_tags = [json.dumps(tags.__dict__)]
	# print json_tags
	# return JsonResponse({'tagname':tags.name})
	# return JsonResponse(json_tags)
	return HttpResponse(json.dumps(results), content_type="application/json")

@login_required(login_url='/'+APPLICATION+'/')
def getAllTags(request):
	tags=Tag.objects.all().order_by("project_id")
	# results = [ob.as_json() for ob in tags]
	HttpResponse.status_code = 200
	return render(request, 'tags.html', {'tags': tags})


@login_required(login_url='/'+APPLICATION+'/')
def getAllResults(request):
	results=Result.objects.all().order_by("project_id", "tag_id")
	HttpResponse.status_code = 200
	return render(request, 'results_page.html', {'results': results})


def returnJsonWithResponseTextCodeAndStatus(responseText, responseCode, responseStatus):
	# print responseText, responseCode, responseStatus
	HttpResponse.status_code = responseCode
	return HttpResponse(
		json.dumps({'status':responseStatus,'message':responseText}),
		            content_type="application/json")


def encode_b(obj):
 	if isinstance(obj, Tag):
 		return obj.__dict__
 	return obj
