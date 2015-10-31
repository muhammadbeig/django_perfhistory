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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^perfhistory/$', 'perfhistory.views.project'),
    url(r'^perfhistory/projects$', 'perfhistory.views.project'),
    # url(r'^myapp/', 'myapp.views.projects'),
    # url(r'^projects/', 'myapp.views.projects'),
    url(r'^tags/', 'myapp.views.tags'),
    url(r'^perfhistory/project/(?P<project_id>[\d+]+)/getTags$', 'perfhistory.views.getTags'),
    url(r'^projects/new/$', 'myapp.views.project_new', name='project_new'),
    url(r'^projects/new1/$', 'myapp.views.project_new1', name='project_new'),
    url(r'^perfhistory/project/(?P<project_id>[\d+])$', 'perfhistory.views.projectdetail'),
    url(r'^perfhistory/chart/$', 'perfhistory.views.chart'),
    url(r'^perfhistory/d3/$', 'perfhistory.views.d3'),
    url(r'^perfhistory/project/(?P<project_id>[0-9]+)/createTag$', 'perfhistory.views.createTag'),
]
