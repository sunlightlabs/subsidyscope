from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from django.views.generic.simple import direct_to_template, redirect_to
import bailout_pdfs
  
urlpatterns = patterns('',
    url(r'^tarp/$', 'bailout.views.tarp_index', name="tarp"),
    url(r'^tarp/visualization\.js$', 'bailout.views.tarp_js', name="tarp-javascript"),    
    url(r'^tarp/csv/$', redirect_to, {'url':'/media/data/bailout/tarp_transactions.csv'}, name="tarp-csv"),
    url(r'^tarp\.xml$', 'bailout.views.tarp_xml', name="tarp-xml"),
    url(r'^json/', direct_to_template, {'template': 'bailout/bailout_programs.json', 'mimetype': 'text/javascript'}, name='bailout-JSON'),
    url(r'cbo-table/$', 'bailout.views.redirect_to_tarp_subsidies', name='bailout-cbo-table'),
    url(r'tarp/subsidies/$', 'bailout.views.tarp_subsidies', name='tarp-subsidies'),
    url(r'tarp/subsidies/cop/$', direct_to_template, {'template': 'bailout/tarp_subsidy_table_cop.html'}, name='tarp-subsidies-cop'),
    url(r'tarp/subsidies/cbo/$', direct_to_template, {'template': 'bailout/tarp_subsidy_table_cbo.html'},  name='tarp-subsidies-cbo'),
    
    url(r'^tarp/warrants/$', direct_to_template, {'template': 'bailout/tarp_warrants.html'}, name="tarp-warrants"),
    url(r'^tarp/warrants/original/$', 'bailout.views.tarp_warrants', name="tarp-warrants-original"),
    url(r'^tarp/warrants/calculation/$', 'bailout.views.tarp_warrants_calculation', name="tarp-warrants-calculation"),
    
    url(r'^tarp/map/$', 'bailout.views.tarp_map', name='tarp-map'),
    url(r'^tarp/map/filter/institution/$', 'bailout.views.tarp_map_filter_institution_search', name='tarp-map-filter-institution-search'),
    url(r'^tarp/map/filter/institution/(?P<bank_id>[0-9]+)/$', 'bailout.views.tarp_map_filter_institution', name='tarp-map-filter-institution'),
    
    # framing viz + navigation
    url(r'^visualization\.js$', 'bailout.views.visualization_js', name="bailout-visualization-js"),
    url(r'^visualization\.css$', 'bailout.views.visualization_css', name="bailout-visualization-css"),
    url(r'^visualization\.json$', direct_to_template, {'template': 'bailout/bailout_programs.json', 'mimetype':'text/javascript'}, name="bailout-visualization-json"),    
    url(r'^treasury/$', 'bailout.views.agency_landing_page', {'agency': 'treasury'}, name='bailout_treasury_index'),
    url(r'^fdic/$', 'bailout.views.agency_landing_page', {'agency': 'fdic'}, name='bailout_fdic_index'),
    url(r'^fdic/ppip/llp/comments/', direct_to_template, {'template': 'bailout/fdic/llp_comments.html'}, name="fdic_llp_comments"),
    url(r'^fdic/tlgp/', direct_to_template, {'template': 'bailout/fdic/tlgp.html'}, name="fdic_tlgp"),
    url(r'^fdic/FDIC_TLGP_opt-in\.csv$', redirect_to, {'url':'/media/data/tlgp_opt_in_source_20090131.csv'}, name='bailout_fdic_tlgp_csv'),
    url(r'^fdic/bank-failures/', include('fdic_bank_failures.urls')),
    url(r'^federal-reserve/$', 'bailout.views.agency_landing_page', {'agency': 'federal_reserve'}, name='bailout_federal_reserve_index'),
    url(r'^federal-reserve/h41', include('fed_h41.urls')),
    url(r'^treasury/fannie-freddie/$', 'bailout.views.agency_landing_page', {'agency': 'fannie_freddie'}, name='fannie_freddie_index'),
    url(r'^fhlb/$', 'bailout.views.agency_landing_page', {'agency': 'fhlb'}, name='fhlb_index'),
    url(r'^other/$', 'bailout.views.agency_landing_page', {'agency': 'other'}, name='bailout_other_index'),
    
    url(r'^tarp/visualization/data/$', 'bailout.views.tarp_timeline_visualization_json', name='tarp-timeline-visualization-json'),
    url(r'^tarp/visualization/institution/$', 'bailout.views.tarp_institution_visualization_json', name='tarp-institution-visualization-json'),
    url(r'^tarp/filter/institution/$', 'bailout.views.tarp_institution_filter_json', name='tarp-institution-filter-json'),
    
    url(r'^search/bank/$', 'bailout.views.bank_search_json', name='bank-search-json'),
    url(r'^search/bank/summary/(?P<bank_id>[0-9]+)/$', 'bailout.views.bank_summary', name='bank-summary'),

    url(r'^roundup/$', direct_to_template, {'template': 'bailout/bailout.html'}, name='bailout-roundup'),    
    url(r'^$', direct_to_template, {'template': 'bailout/bailout.html'}, name='bailout-index'),    
        
)

