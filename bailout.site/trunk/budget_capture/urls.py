from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from django.views.generic.simple import direct_to_template, redirect_to
import bailout_pdfs
  
urlpatterns = patterns('',
    url(r'^$', 'budget_capture.views.main', name='budget_capture-main'),
    url(r'^task/(?P<task_id>[0-9]+)/$', 'budget_capture.views.task', name='budget_capture-task'),
    url(r'^capture/(?P<item_id>[0-9]+)/$', 'budget_capture.views.capture', name='budget_capture-capture'),
    url(r'^edit/(?P<data_id>[0-9]+)/$', 'budget_capture.views.edit', name='budget_capture-edit'),
    url(r'^cfda/(?P<cfda_id>[0-9]+)/$', 'budget_capture.views.cfda', name='budget_capture-cfda'),
)