from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from django.views.generic.simple import direct_to_template, redirect_to
import bailout_pdfs
  
urlpatterns = patterns('tax_expenditures.views',
    url(r'^csv/(?P<group_id>\d+)/$', 'te_csv', name="tax_expenditures-csv"),
    url(r'^csv/$', 'te_csv', name="tax_expenditures-csv"),
    url(r'^db/group/(?P<group_id>\d+)/$', 'group', name="tax_expenditures-group"),
    url(r'^db/$', 'main', name="tax_expenditures-main"),
    url(r'^methodology/$', direct_to_template, {'template': 'tax_expenditures/index.html'}, name="tax_expenditures-methodology"),
    url(r'^search$', 'search', name='search'),
    url(r'^summary/$', direct_to_template, {'template': 'tax_expenditures/index.html'}, name="tax_expenditures-summary"),
    url(r'^$', redirect_to, {'url': '/tax_expenditures/summary/'})
)
    
