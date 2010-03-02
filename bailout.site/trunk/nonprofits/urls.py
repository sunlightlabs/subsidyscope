from django.conf import settings
from django.conf.urls.defaults import *
from sectors.models import Sector
from django.views.generic.simple import direct_to_template, redirect_to


urlpatterns = patterns('', 
    url(r'^direct-expenditures/search/', 'faads.views.search', {'sector_name': 'nonprofits'}, name='nonprofits-faads-search'),
    url(r'^direct-expenditures/programs/(?P<cfda_program_number>\d{2}\.\d{3})/', 'cfda.views.getProgramByCFDANumber', {'sector_name': 'nonprofits'}, name='nonprofits-cfda-programpage-by-programnumber'),    
    url(r'^contracts/search/', 'fpds.views.search', {'sector_name': 'nonprofits'}, name='nonprofits-fpds-search'),
    url(r'^direct-expenditures/', direct_to_template, {'template': 'nonprofits/direct_payments.html'}, name='nonprofits-direct-expenditures'),
    url(r'^tax-expenditures/', direct_to_template, {'template': 'nonprofits/tax_expenditures/index.html'}, name='nonprofits-tax-expenditures'),
    url(r'^risk-transfers/$', direct_to_template, {'template': 'nonprofits/risk_transfers.html'}, name='nonprofits-risk-transfers'),
    url(r'^risk-transfers/test', direct_to_template, {'template': 'nonprofits/risk_transfers.html'}, name='nonprofits-risk-transfers-test'),
    # url(r'^contracts/', direct_to_template, {'template': 'nonprofits/contracts.html'}, name='nonprofits-contracts'),
    url(r'^overview/', direct_to_template, {'template': 'nonprofits/overview.html'}, name='nonprofits-overview'),
    url(r'^docs/', direct_to_template, {'template': 'nonprofits/docs.html'}, name='nonprofits-docs'),
    url(r'^$', direct_to_template, {'template': 'nonprofits/index.html'}, name='nonprofits-index'),
)
