from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from django.views.generic.simple import direct_to_template, redirect_to
import bailout_pdfs
  
urlpatterns = patterns('tax_expenditures.views',
    url(r'^csv/(?P<group_id>.*)/$', 'te_csv', name="tax_expenditures-csv"),
    url(r'^csv/$', 'te_csv', name="tax_expenditures-csv"),
    url(r'^group/(?P<group_id>.*)/(?P<estimate>[1-3])/$', 'group', name="tax_expenditures-group"),
    url(r'^(?P<estimate>[1-3])/$', 'main', name="tax_expenditures-main"),
    url(r'^summary/$', direct_to_template, {'template': 'tax_expenditures/index.html'}, name="tax_expenditures-summary"),
    url(r'^.*$', 'main', name="tax_expenditures-main"))