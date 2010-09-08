from django.conf import settings
from django.conf.urls.defaults import *
from sectors.models import Sector
from django.views.generic.simple import direct_to_template, redirect_to


urlpatterns = patterns('', 
    url(r'^direct-expenditures/search/by-year/', 'faads.views.annual_chart_data', {}, name='faads-search-by-year'),
    url(r'^direct-expenditures/search/map-table/', 'faads.views.map_data_table', {}, name='faads-search-map-table'),
    url(r'^direct-expenditures/search/map/', 'faads.views.map_data', {}, name='faads-search-map-data'),
    url(r'^direct-expenditures/search/summary/csv/state/', 'faads.views.summary_statistics_csv', {'first_column_label': 'State', 'data_fetcher': '_get_state_summary_data'}, name='faads-search-summary-csv-state'),    
    url(r'^direct-expenditures/search/summary/csv/program/', 'faads.views.summary_statistics_csv', {'first_column_label': 'CFDA Program', 'data_fetcher': '_get_program_summary_data'}, name='faads-search-summary-csv-program'),    
    url(r'^direct-expenditures/search/summary/', 'faads.views.summary_statistics', {}, name='faads-search-summary'),
)