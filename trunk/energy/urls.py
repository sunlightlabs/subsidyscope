from django.conf import settings
from django.conf.urls.defaults import *
from sectors.models import Sector
from django.views.generic.simple import direct_to_template, redirect_to


urlpatterns = patterns('', 
    url(r'^direct-expenditures/search/', 'faads.views.search', {'sector_name': 'energy'}, name='energy-faads-search'),
    url(r'^direct-expenditures/programs/(?P<cfda_program_number>\d{2}\.\d{3})/', 'cfda.views.getProgramByCFDANumber', {'sector_name': 'energy'}, name='energy-cfda-programpage-by-programnumber'),    
    url(r'^direct-expenditures/programs/(?P<cfda_id>[0-9]+)/', 'cfda.views.getProgram', {'sector_name': 'energy'}, name='energy-cfda-programpage'),
    url(r'^contracts/search/', 'fpds.views.search', {'sector_name': 'energy'}, name='energy-fpds-search'),
    url(r'^direct-expenditures/', direct_to_template, {'template': 'energy/direct_payments.html'}, name='energy-direct-expenditures'),
    url(r'^tax-expenditures/', direct_to_template, {'template': 'energy/tax_expenditures/index.html'}, name='energy-tax-expenditures'),
    url(r'^regulations/', direct_to_template, {'template': 'energy/regulations.html'}, name='energy-regulations'),
    url(r'^risk-transfers/', direct_to_template, {'template': 'energy/risk_transfers.html'}, name='energy-risk-transfers'),

    url(r'^overview/structure/', redirect_to, {'url': '/energy/summary/structure/'}),
    url(r'^overview/', redirect_to, {'url':'/energy/summary/'}),
    url(r'^overview/data-limitations/', redirect_to, {'template': '/energy/summary/data-limitations'}),
    url(r'^summary/structure/', direct_to_template, {'template': 'energy/overview.html'}, name='energy-overview-structure'),
    url(r'^summary/', direct_to_template, {'template': 'energy/overview.html'}, name='energy-overview'),
    url(r'^summary/data-limitations/', direct_to_template, {'template': 'energy/overview.html'}, name='energy-overview-data-limitations'),
    url(r'^docs/', direct_to_template, {'template': 'energy/docs.html'}, name='energy-docs'),
    url(r'^$', direct_to_template, {'template': 'energy/index.html'}, name='energy-index'),
)
