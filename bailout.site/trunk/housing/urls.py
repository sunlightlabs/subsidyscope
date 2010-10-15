from django.conf import settings
from django.conf.urls.defaults import *
from sectors.models import Sector
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('', 
    url(r'^direct-expenditures/search/', 'faads.views.search', {'sector_name': 'housing'}, name='housing-faads-search'),
    url(r'^direct-expenditures/programs/(?P<cfda_program_number>\d{2}\.\d{3})/', 'cfda.views.getProgramByCFDANumber', {'sector_name': 'housing'}, name='housing-cfda-programpage-by-programnumber'),    
    url(r'^contracts/search/', 'fpds.views.search', {'sector_name': 'housing'}, name='housing-fpds-search'),
    url(r'^direct-expenditures/', direct_to_template, {'template': 'housing/generic_housing_template.html'}, name='housing-direct-expenditures'),
    url(r'^tax-expenditures/', direct_to_template, {'template': 'housing/tax_expenditures.html'}, name='housing-tax-expenditures'),
    url(r'^regulations/', direct_to_template, {'template': 'housing/generic_housing_template.html'}, name='housing-regulations'),
    url(r'^risk-transfers/', direct_to_template, {'template': 'housing/generic_housing_template.html'}, name='housing-risk-transfers'),

    url(r'^overview/structure/', redirect_to, {'url': '/housing/summary/structure/'}),
    url(r'^overview/', redirect_to, {'url':'/housing/summary/'}),
    url(r'^overview/data-limitations/', redirect_to, {'template': '/housing/summary/data-limitations'}),
    url(r'^summary/structure/', direct_to_template, {'template': 'housing/generic_housing_template.html'}, name='housing-overview-structure'),
    url(r'^summary/', direct_to_template, {'template': 'housing/generic_housing_template.html'}, name='housing-overview'),
    url(r'^summary/data-limitations/', direct_to_template, {'template': 'housing/generic_housing_template.html'}, name='housing-overview-data-limitations'),
    url(r'^docs/', direct_to_template, {'template': 'housing/docs.html'}, name='housing-docs'),
    url(r'^$', direct_to_template, {'template': 'housing/index.html'}, name='housing-index'),
)
