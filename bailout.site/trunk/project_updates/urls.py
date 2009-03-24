from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from project_updates.models import *

urlpatterns = patterns('',
    url(r'^(?P<entry_year>\d{4})\/(?P<entry_month>\d+)\/(?P<entry_day>\d+)\/(?P<entry_slug>[\w\-]+)/$', 'project_updates.views.entry', name='project_update_permalink')
)


