from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'bailout/fdic/bank_failures.html'}, name='fdic_bank_failures'),
    url(r'^bank-failures\.xml$', 'fdic_bank_failures.views.fdic_bank_failures_xml', name="fdic_bank_failures_xml"),
    url(r'^bank-failures\.csv$', 'fdic_bank_failures.views.fdic_bank_failures_csv', name="fdic_bank_failures_csv"),    
)