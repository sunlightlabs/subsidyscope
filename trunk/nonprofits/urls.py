from django.conf import settings
from django.conf.urls.defaults import *
from sectors.models import Sector
from django.views.generic.simple import direct_to_template, redirect_to


urlpatterns = patterns('', 
    url(r'^direct-expenditures/search/', 'faads.views.search', {'sector_name': 'nonprofits'}, name='nonprofits-faads-search'),
    url(r'^direct-expenditures/programs/(?P<cfda_program_number>\d{2}\.\d{3})/', 'cfda.views.getProgramByCFDANumber', {'sector_name': 'nonprofits'}, name='nonprofits-cfda-programpage-by-programnumber'),    
    url(r'^direct-expenditures/programs/(?P<cfda_id>[0-9]+)/', 'cfda.views.getProgram', {'sector_name': 'nonprofits'}, name='nonprofits-cfda-programpage'),
    url(r'^contracts/search/', 'fpds.views.search', {'sector_name': 'nonprofits'}, name='nonprofits-fpds-search'),
    url(r'^direct-expenditures/', direct_to_template, {'template': 'nonprofits/direct_payments.html'}, name='nonprofits-direct-expenditures'),
    
    
    url(r'^tax-expenditures/other-charitable-contributions/', direct_to_template, {'template': 'nonprofits/tax_expenditures/index.html'}, name='nonprofits-tax-expenditures-other-contrib'),
    url(r'^tax-expenditures/health-charitable-contributions/', direct_to_template, {'template': 'nonprofits/tax_expenditures/index.html'}, name='nonprofits-tax-expenditures-health-contrib'),
    url(r'^tax-expenditures/education-charitable-contributions/', direct_to_template, {'template': 'nonprofits/tax_expenditures/index.html'}, name='nonprofits-tax-expenditures-edu-contrib'),
    url(r'^tax-expenditures/credit-union-income/', direct_to_template, {'template': 'nonprofits/tax_expenditures/index.html'}, name='nonprofits-tax-expenditures-credit-union-income'),
    url(r'^tax-expenditures/bond-interest-for-educational-facilities/', direct_to_template, {'template': 'nonprofits/tax_expenditures/index.html'}, name='nonprofits-tax-expenditures-edu-bonds'),
    url(r'^tax-expenditures/blue-cross-blue-shield/', direct_to_template, {'template': 'nonprofits/tax_expenditures/index.html'}, name='nonprofits-tax-expenditures-bcbs'),
    url(r'^tax-expenditures/minister-housing-exclusion/', direct_to_template, {'template': 'nonprofits/tax_expenditures/index.html'}, name='nonprofits-tax-expenditures-minister-housing'),
    
    url(r'^tax-expenditures/', direct_to_template, {'template': 'nonprofits/tax_expenditures/index.html'}, name='nonprofits-tax-expenditures'),
    url(r'^risk-transfers/', direct_to_template, {'template': 'nonprofits/risk_transfers.html'}, name='nonprofits-risk-transfers'),
    # url(r'^contracts/', direct_to_template, {'template': 'nonprofits/contracts.html'}, name='nonprofits-contracts'),
    url(r'^summary/structure/', direct_to_template, {'template': 'nonprofits/overview.html'}, name='nonprofits-overview-structure'),
    url(r'^summary/', direct_to_template, {'template': 'nonprofits/overview.html'}, name='nonprofits-overview'),
    url(r'^overview/structure/', redirect_to, {'url': '/nonprofits/summary/structure/'}),
    url(r'^overview/', redirect_to, {'url': '/nonprofits/summary/'}),
    url(r'^docs/', direct_to_template, {'template': 'nonprofits/docs.html'}, name='nonprofits-docs'),
    url(r'^$', direct_to_template, {'template': 'nonprofits/index.html'}, name='nonprofits-index'),
)
