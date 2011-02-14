from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    url(r'^$', 'fdic_bank_failures.views.fdic_bank_failures', name='fdic_bank_failures'),
    url(r'^table\/$', 'fdic_bank_failures.views.fdic_bank_failures_table', name='fdic_bank_failures_table'),
    url(r'^prepayment-requirement\/$', direct_to_template, {'template': 'bailout/bailout.html'}, name='fdic_bank_failures_prepayment_requirement'),
    url(r'^bank-failures\.xml$', 'fdic_bank_failures.views.fdic_bank_failures_xml', name="fdic_bank_failures_xml"),
    url(r'^bank-failures\.csv$', redirect_to, {'url':'/media/data/bailout/fdic_bank_failures.csv'}, name="fdic_bank_failures_csv"),    
    url(r'^qbp-snapshots\.xml$', 'fdic_bank_failures.views.fdic_qbpsnapshot_xml', name="fdic_qbpsnapshot_xml"),        
    url(r'^qbp-snapshots\.csv$', redirect_to, {'url':'/media/data/bailout/fdic_qbp_snapshot.csv'}, name="fdic_qbpsnapshot_csv"),            
)