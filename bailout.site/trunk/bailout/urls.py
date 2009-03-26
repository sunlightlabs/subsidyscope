from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from django.views.generic.simple import direct_to_template
import bailout_pdfs

urlpatterns = patterns('',
    url(r'^tarp/$', 'bailout.views.tarp_index', name="tarp"),
    url(r'^tarp/visualization\.js$', 'bailout.views.tarp_js', name="tarp-javascript"),    
    url(r'^tarp/csv/$', 'bailout.views.tarp_csv', name="tarp-csv"),
    url(r'^tarp\.xml$', 'bailout.views.tarp_xml', name="tarp-xml"),
    url(r'^documents/', include('bailout_pdfs.urls')),
    url(r'^json/', direct_to_template, {'template': 'bailout/bailout_programs.json', 'mimetype': 'text/javascript'}, name='bailout-JSON'),
    url(r'cbo-table/$', 'bailout.views.redirect_to_tarp_subsidies', name='bailout-cbo-table'),
    url(r'tarp/subsidies/$', 'bailout.views.tarp_subsidies', name='tarp-subsidies'),
    url(r'tarp/subsidies/cop/$', direct_to_template, {'template': 'bailout/tarp_subsidy_table_cop.html'}, name='tarp-subsidies-cop'),
    url(r'tarp/subsidies/cbo/$', direct_to_template, {'template': 'bailout/tarp_subsidy_table_cbo.html'},  name='tarp-subsidies-cbo'),
    
    url(r'^tarp/warrants/$', 'bailout.views.tarp_warrants', name="tarp-warrants"),
    url(r'^tarp/warrants/calculation/$', 'bailout.views.tarp_warrants_calculation', name="tarp-warrants-calculation"),
    
    # framing viz + navigation
    url(r'^visualization\.js$', 'bailout.views.visualization_js', name="bailout-visualization-js"),
    url(r'^visualization\.css$', 'bailout.views.visualization_css', name="bailout-visualization-css"),
    url(r'^visualization\.json$', direct_to_template, {'template': 'bailout/bailout_programs.json', 'mimetype':'text/javascript'}, name="bailout-visualization-json"),    
    url(r'^treasury/$', 'bailout.views.agency_landing_page', {'agency': 'treasury'}, name='bailout_treasury_index'),
    url(r'^fdic/$', 'bailout.views.agency_landing_page', {'agency': 'fdic'}, name='bailout_fdic_index'),
    url(r'^fdic/FDIC_TLGP_opt-in\.csv$', 'bailout.views.fdic_tlgp_csv', name='bailout_fdic_tlgp_csv'),
    url(r'^fdic/bank-failures/', include('fdic_bank_failures.urls')),
    url(r'^federal-reserve/$', 'bailout.views.agency_landing_page', {'agency': 'federal_reserve'}, name='bailout_federal_reserve_index'),
    url(r'^federal-reserve/h41', include('fed_h41.urls')),
    url(r'^other/$', 'bailout.views.agency_landing_page', {'agency': 'other'}, name='bailout_other_index'),
    
    
    url(r'^tarp/alt/$', 'bailout.views.tarp_alt_index', name='tarp_alt'),
    url(r'^tarp/alt/bubbles/$', 'bailout.views.tarp_alt_bubbles_index', name='tarp_bubbles_visualization'),
    url(r'^tarp/visualization/data/$', 'bailout.views.tarp_timeline_visualization_json', name='tarp-timeline-visualization-json'),
    url(r'^tarp/visualization/institution/$', 'bailout.views.tarp_institution_visualization_json', name='tarp-institution-visualization-json'),
    url(r'^tarp/filter/institution/$', 'bailout.views.tarp_institution_filter_json', name='tarp-institution-filter-json'),
    
    url(r'^search/bank/$', 'bailout.views.bank_search_json', name='bank-search-json'),
    url(r'^search/bank/summary/(?P<bank_id>[0-9]+)/$', 'bailout.views.bank_summary', name='bank-summary'),

    url(r'^$', direct_to_template, {'template': 'bailout/bailout.html'}, name='Bailout'),    
    
)


