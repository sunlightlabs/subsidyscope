from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from django.views.generic.simple import direct_to_template, redirect_to
import bailout_pdfs
  
urlpatterns = patterns('tax_expenditures.views',
    #url(r'^add/(?P<expenditure_id>.*)/$', 'expenditure_add', name="tax_expenditures-expenditure-add"),
    url(r'^expenditure/(?P<expenditure_id>.*)/$', 'expenditure', name="tax_expenditures-expenditure"),
    url(r'^category/(?P<category_id>.*)/$', 'category', name="tax_expenditures-category"),
    url(r'^.*$', 'main', name="tax_expenditures-main"))