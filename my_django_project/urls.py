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
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^(?i)admin/', include(admin.site.urls)),
    url(r'^(?i)perfhistory/$', 'perfhistory.views.loginView'),
    url(r'^(?i)perfhistory/logout$', 'perfhistory.views.logoutView'),
    # url(r'^(?i)perfhistory/home$', HomeView.as_view(template_name='login.html'), name='home'),
    url(r'^(?i)perfhistory/projects$', 'perfhistory.views.project'),
    url(r'^(?i)perfhistory/project/(?P<projectId>[\d+]+)$', 'perfhistory.views.deleteProject'),
    # url(r'^myapp/', 'myapp.views.projects'),
    # url(r'^projects/', 'myapp.views.projects'),
    url(r'^(?i)tags/', 'myapp.views.tags'),
    url(r'^(?i)perfhistory/project/(?P<project_id>[\d+]+)/getTags$', 'perfhistory.views.getTags'),
    # url(r'^(?i)projects/new/$', 'myapp.views.project_new', name='project_new'),
    # url(r'^(?i)projects/new1/$', 'myapp.views.project_new1', name='project_new'),
    url(r'^(?i)perfhistory/project/(?P<project_id>[\d+])$', 'perfhistory.views.projectdetail'),
    url(r'^(?i)perfhistory/chart/$', 'perfhistory.views.chart'),
    url(r'^(?i)perfhistory/d3/$', 'perfhistory.views.d3'),
    url(r'^(?i)perfhistory/project/(?P<project_id>[0-9]+)/createTag$', 'perfhistory.views.createTag'),
    url(r'^(?i)perfhistory/project/(?P<project_id>[0-9]+)/tag/(?P<tagid>[0-9]+)/createResult$', 'perfhistory.views.createResult'),
    url(r'^(?i)perfhistory/project/(?P<projectId>[0-9]+)/tag/(?P<tagId>[0-9]+)/result$', 'perfhistory.views.result'),
    url(r'^(?i)perfhistory/result/(?P<resultId>[0-9]+)$', 'perfhistory.views.updateResult'),
    url(r'^(?i)perfhistory/project/(?P<projectId>[0-9]+)/tag/(?P<tagId>[0-9]+)/comparisonChart$', 'perfhistory.views.comparisonChart'),

]
