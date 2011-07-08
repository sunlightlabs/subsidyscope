from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from sectors.models import Sector
from django.views.generic.simple import direct_to_template, redirect_to



urlpatterns = patterns('', 
    url(r'^direct-expenditures/search/', 'faads.views.search', {'sector_name': 'transportation'}, name='transportation-faads-search'),
    url(r'^direct-expenditures/programs/faads/(?P<cfda_id>[0-9]+)/', 'cfda.views.getFAADSLineItems',{'sector_name':'transportation'}, name='cfda-FAADS'),
    url(r'^direct-expenditures/programs/(?P<cfda_program_number>\d{2}\.\d{3})/', 'cfda.views.getProgramByCFDANumber', {'sector_name': 'transportation'}, name='transportation-cfda-programpage-by-programnumber'),
    url(r'^direct-expenditures/programs/(?P<cfda_id>[0-9]+)/', 'cfda.views.getProgram', {'sector_name': 'transportation'}, name='transportation-cfda-programpage'),
    url(r'^direct-expenditures/programs/$', 'cfda.views.getProgramIndex', {'sector_name': 'transportation'}, name='transportation-cfdaprograms-index'),
    url(r'^direct-expenditures/getchart/(?P<cfda_id>[0-9]+)/', 'cfda.views.ajaxChart', name='chart data'),
    url(r'^direct-expenditures/$', direct_to_template, {'template': 'transportation/direct_payments.html'}, name='transportation-direct-expenditures'),
    url(r'^tax-expenditures/', direct_to_template, {'template': 'transportation/tax_expenditures/index.html', 'extra_context': {'menu_name':'transportation'}}, name='transportation-tax-expenditures'),
    url(r'^tax-expenditures/employer-paid-benefits/', direct_to_template, {'template': 'transportation/tax_expenditures/employer_paid_benefits.html'}, name='transportation-tax-expenditures-employer-paid-benefits'),
    url(r'^tax-expenditures/capital-construction-funds/', direct_to_template, {'template': 'transportation/tax_expenditures/capital_construction_funds.html'}, name='transportation-tax-expenditures-capital-construction-funds'),
    url(r'^tax-expenditures/track-maintenance/', direct_to_template, {'template': 'transportation/tax_expenditures/track_maintenance.html'}, name='transportation-tax-expenditures-track-maintenance'),
    url(r'^tax-expenditures/bond-interest-exclusion/', direct_to_template, {'template': 'transportation/tax_expenditures/bond_interest_exclusion.html'}, name='transportation-tax-expenditures-bond-interest-exclusion'),
    url(r'^risk-transfers/exim/', direct_to_template, {'template': 'transportation/exim.html'}, name='transportation-exim'),
    url(r'^risk-transfers/marad/title-xi/', direct_to_template, {'template': 'transportation/marad-title-xi.html'}, name='transportation-marad-title-xi'),
    url(r'^risk-transfers/', direct_to_template, {'template': 'transportation/risk_transfers.html'}, name='transportation-risk-transfers'),
    
    url(r'^direct-expenditures/amtrak/table/', direct_to_template, {'template': 'transportation/amtrak_table.html'}, name='transportation-amtrak-table'),
    url(r'^direct-expenditures/amtrak/analysis/', direct_to_template, {'template': 'transportation/amtrak.html'}, name='transportation-amtrak'),
    url(r'^amtrak/table/', redirect_to, {'url': '/direct-expenditures/amtrak/table/'}),
    url(r'^amtrak/', redirect_to, {'url': '/direct-expenditures/amtrak/analysis/'}),
    url(r'^contracts/', direct_to_template, {'template': 'transportation/contracts.html'}, name='transportation-contracts'),
    url(r'^summary/', direct_to_template, { 'template': 'transportation/overview.html'}, name="transportation-overview"),
    url(r'^overview/', redirect_to, {'url': '/transportation/summary/'}),
    url(r'^docs/', direct_to_template, {'template': 'transportation/docs.html'}, name='transportation-docs'),
    url(r'^other/', direct_to_template, {'template': 'transportation/mode_page.html', 'extra_context':{'subsector': 1}}, name='transportation-general'),
    url(r'^aviation/', direct_to_template, {'template': 'transportation/mode_page.html', 'extra_context':{'subsector': 2}}, name='transportation-aviation'),
    
    url(r'^direct-expenditures/highways/funding/state/', direct_to_template, {'template': 'transportation/highways/funding_state.html', 'extra_context':{'subsector': 3}}, name='transportation-highway-funding-state'),
    url(r'^highways/funding/state/fundingtable/(?P<state_id>[0-9]+)/', 'transportation.views.get_state_highway_funding_table', name='transportation-highway-funding-state-funding-table'),
    url(r'^highways/funding/state/milestable/(?P<state_id>[0-9]+)/', 'transportation.views.get_state_highway_miles_table', name='transportation-highway-funding-state-miles-table'),
    url(r'^highways/funding/state/chart/(?P<state_id>[0-9]+)/', 'transportation.views.get_state_highway_funding_chart', name='transportation-highway-funding-state-chart'),
    url(r'^direct-expenditures/highways/funding/analysis/$', direct_to_template, {'template': 'transportation/highways/funding.html', 'extra_context':{'subsector': 3}}, name='transportation-highway-funding'),


    url(r'^highways/funding/state/', redirect_to, {'url': '/direct-expenditures/highways/funding/state/'}),
    url(r'^highways/funding/', redirect_to, {'url': '/direct-expenditures/highways/funding/analysis/'}),
    
    url(r'^highways/', direct_to_template, {'template': 'transportation/mode_page.html', 'extra_context':{'subsector': 3}}, name='transportation-highways'),
    url(r'^transit/', include('transit.urls')),
    url(r'^rail/', direct_to_template, {'template': 'transportation/mode_page.html', 'extra_context':{'subsector': 4}}, name='transportation-rail'),
    url(r'^maritime/', direct_to_template, {'template': 'transportation/mode_page.html', 'extra_context':{'subsector': 6}}, name='transportation-maritime'),
    url(r'^$', direct_to_template, {'template': 'transportation/index.html'}, name='transportation-index'),


    url(r'^direct-expenditures/aip/search/(?P<code>[A-Za-z0-9@*+]+)', 'aip.views.portdata', name='aip-airport-data'),
    url(r'^direct-expenditures/aip/search/$', 'aip.views.index', name='aip-index'),
    url(r'^direct-expenditures/aip/analysis/$', direct_to_template, {'template': 'aip/story.html'}, name='aip-story'),

    url(r'^aip/results/csv', 'aip.views.get_csv_from_search', name='aip-csv-download'),
    url(r'^aip/$', redirect_to, {'url': '/transportation/direct-expenditures/aip/analysis/'}),
    url(r'^aip/search/$', redirect_to, {'url': '/transportation/direct-expenditures/aip/search/'}),
    url(r'^aip/airports/(?P<code>[A-Za-z0-9@*+]+)', redirect_to, {'url': '/transportation/direct-expenditures/aip/search/%(code)s'}),
)
