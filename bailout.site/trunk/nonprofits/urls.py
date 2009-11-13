from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from sectors.models import Sector
from django.views.generic.simple import direct_to_template, redirect_to


urlpatterns = patterns('', 
    url(r'^direct-expenditures/search/', 'faads.views.search', {'sector_name': 'nonprofits'}, name='nonprofits-faads-search'),
    url(r'^direct-expenditures/', direct_to_template, {'template': 'nonprofits/direct_payments.html'}, name='nonprofits-direct-expenditures'),
    url(r'^tax-expenditures/', direct_to_template, {'template': 'nonprofits/tax_expenditures/index.html'}, name='nonprofits-tax-expenditures'),
    url(r'^risk-transfers/', direct_to_template, {'template': 'nonprofits/risk_transfers.html'}, name='nonprofits-risk-transfers'),
    # url(r'^contracts/', direct_to_template, {'template': 'nonprofits/contracts.html'}, name='nonprofits-contracts'),
    url(r'^overview/', direct_to_template, {'template': 'nonprofits/overview.html'}, name='nonprofits-overview'),
    url(r'^docs/', direct_to_template, {'template': 'nonprofits/docs.html'}, name='nonprofits-docs'),
    # url(r'^other/', direct_to_template, {'template': 'transportation/mode_page.html', 'extra_context':{'subsector': 1}}, name='transportation-general'),
    # url(r'^aviation/', direct_to_template, {'template': 'transportation/mode_page.html', 'extra_context':{'subsector': 2}}, name='transportation-aviation'),
    # url(r'^highways/', direct_to_template, {'template': 'transportation/mode_page.html', 'extra_context':{'subsector': 3}}, name='transportation-highways'),
    # url(r'^transit/', direct_to_template, {'template': 'transportation/mode_page.html', 'extra_context':{'subsector': 5}}, name='transportation-transit'),
    # url(r'^rail/', direct_to_template, {'template': 'transportation/mode_page.html', 'extra_context':{'subsector': 4}}, name='transportation-rail'),
    # url(r'^maritime/', direct_to_template, {'template': 'transportation/mode_page.html', 'extra_context':{'subsector': 6}}, name='transportation-maritime'),
    url(r'^$', direct_to_template, {'template': 'nonprofits/index.html'}, name='nonprofits-index'),
)
