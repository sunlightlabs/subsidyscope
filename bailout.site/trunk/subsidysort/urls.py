from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from django.views.generic.simple import direct_to_template, redirect_to
import bailout_pdfs
  
urlpatterns = patterns('',
    url(r'^$', 'subsidysort.views.main', name='subsidysort-main'),
    url(r'^task/(?P<task_id>[0-9]+)/$', 'subsidysort.views.task', name='subsidysort-task'),
    url(r'^vote/(?P<item_id>[0-9]+)/$', 'subsidysort.views.vote', name='subsidysort-vote'),
    url(r'^cfda/(?P<cfda_id>[0-9]+)/$', 'subsidysort.views.cfda', name='subsidysort-cfda'),
    url(r'^login/$', 'subsidysort.views.login'),
    url(r'^logout/$', 'subsidysort.views.logout'),
    url(r'^change_password/$', 'subsidysort.views.change_password'),
)