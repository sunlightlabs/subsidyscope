from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from django.views.generic.simple import direct_to_template, redirect_to
import bailout_pdfs
  
urlpatterns = patterns('',
    url(r'^$', 'tax_expenditures.views.render_tax_expenditures', name='render_tax_expenditures'),
    url(r'^(?P<category_id>[0-9]+)/$', 'tax_expenditures.views.render_tax_expenditures', name='render_tax_expenditures_by_id'),
    url(r'^expenditure/(?P<expenditure_id>[0-9]+)/$', 'tax_expenditures.views.render_tax_expenditure', name='render_tax_expenditure_by_id')
)