from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from sectors.models import Sector
from django.views.generic.simple import direct_to_template, redirect_to



urlpatterns = patterns('', 
    url(r'^direct-expenditures/search/by-year/', 'faads.views.annual_chart_data', {'sector_name': 'transportation'}, name='transportation-faads-search-by-year'),
    url(r'^direct-expenditures/search/map/', 'faads.views.map_data', {'sector_name': 'transportation'}, name='transportation-faads-search-map-data'),
    url(r'^direct-expenditures/search/', 'faads.views.search', {'sector_name': 'transportation'}, name='transportation-faads-search'),
    url(r'^direct-expenditures/programs/faads/(?P<cfda_id>[0-9]+)/', 'cfda.views.getFAADSLineItems',{'sector_name':'transportation'}, name='cfda-FAADS'),
    url(r'^direct-expenditures/programs/(?P<cfda_id>[0-9]+)/', 'cfda.views.getProgram', {'sector_name': 'transportation'}, name='cfda-programpage'),
    url(r'^direct-expenditures/programs/$', 'cfda.views.getProgramIndex', {'sector_name': 'transportation'}, name='cfdaprograms-index'),
    url(r'^direct-expenditures/', direct_to_template, {'template': 'transportation/direct_payments.html'}, name='transportation-direct-expenditures'),
    url(r'^tax-expenditures/', direct_to_template, {'template': 'transportation/tax_expenditures.html'}, name='transportation-tax-expenditures'),
    url(r'^risk-transfers/', direct_to_template, {'template': 'transportation/tax_expenditures.html'}, name='transportation-risk-transfers'),
    url(r'^contracts/', direct_to_template, {'template': 'transportation/contracts.html'}, name='transportation-contracts'),
    url(r'^backgrounders/', direct_to_template, {'template': 'transportation/backgrounders.html'}, name='transportation-backgrounders'),
    url(r'^docs/', direct_to_template, {'template': 'transportation/docs.html'}, name='transportation-docs'),
    url(r'^general/', direct_to_template, {'template': 'transportation/mode_page.html'}, name='transportation-general'),
    url(r'^aviation/', direct_to_template, {'template': 'transportation/mode_page.html'}, name='transportation-aviation'),
    url(r'^highways/', direct_to_template, {'template': 'transportation/mode_page.html'}, name='transportation-highways'),
    url(r'^transit/', direct_to_template, {'template': 'transportation/mode_page.html'}, name='transportation-transit'),
    url(r'^rail/', direct_to_template, {'template': 'transportation/mode_page.html'}, name='transportation-rail'),
    url(r'^maritime/', direct_to_template, {'template': 'transportation/mode_page.html'}, name='transportation-maritime'),
    url(r'^$', direct_to_template, {'template': 'transportation/index.html'}, name='transportation-index')
)
