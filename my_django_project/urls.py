"""my_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
import perfhistory.views 
admin.autodiscover()

urlpatterns = [

    url(r'^(?i)admin/', include(admin.site.urls)),
    url(r'^$', perfhistory.views.loginView, name="Login"),
    url(r'^(?i)perfhistory/$', perfhistory.views.loginView, name="Login"),
    
    url(r'^(?i)d3/$', perfhistory.views.d3),
    url(r'^(?i)chart/$', perfhistory.views.chart),

    url(r'^(?i)perfhistory/logout$', perfhistory.views.logoutView, name="Logout"),
    # url(r'^(?i)perfhistory/home$', HomeView.as_view(template_name='login.html'), name='home'),
    url(r'^(?i)perfhistory/projects$', perfhistory.views.project, name="Project list"),
    url(r'^(?i)perfhistory/project/(?P<projectId>[\d+]+)$', perfhistory.views.deleteProject, name="Delete project"),
    
    url(r'^(?i)perfhistory/project/(?P<project_id>[\d+]+)/getTags$', perfhistory.views.getTags),
    url(r'^(?i)perfhistory/tags$', perfhistory.views.getAllTags),
    url(r'^(?i)perfhistory/results$', perfhistory.views.getAllResults),
    url(r'^(?i)perfhistory/project/(?P<project_id>[\d+])$', perfhistory.views.projectdetail),
    url(r'^(?i)perfhistory/chart/$', perfhistory.views.chart),
    url(r'^(?i)perfhistory/d3/$', perfhistory.views.d3),
    url(r'^(?i)perfhistory/project/(?P<project_id>[0-9]+)/createTag$', perfhistory.views.createTag),
    url(r'^(?i)perfhistory/project/(?P<project_id>[0-9]+)/tag/(?P<tagid>[0-9]+)/createResult$', perfhistory.views.createResult),
    url(r'^(?i)perfhistory/project/createResult$', perfhistory.views.createResultByProjectTagName),
    url(r'^(?i)perfhistory/project/(?P<projectId>[0-9]+)/tag/(?P<tagId>[0-9]+)/result$', perfhistory.views.result),
    url(r'^(?i)perfhistory/result/(?P<resultId>[0-9]+)$', perfhistory.views.updateResult),
    url(r'^(?i)perfhistory/project/(?P<projectId>[0-9]+)/tag/(?P<tagId>[0-9]+)/comparisonChart$', perfhistory.views.comparisonChart),
    url(r'^(?i)perfhistory/project/(?P<projectId>[0-9]+)/tag/(?P<tagId>[0-9]+)/comparisonChartByVersion$', perfhistory.views.comparisonChartbyVersion),
    url(r'^(?i)perfhistory/project/(?P<projectId>[0-9]+)/tag/(?P<tagId>[0-9]+)/comparisonChartWithLimit/(?P<limit>[0-9]+)$', perfhistory.views.comparisonChartWithLimit),
]
