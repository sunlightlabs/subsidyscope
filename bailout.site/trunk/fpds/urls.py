from django.conf import settings
from django.conf.urls.defaults import *
from sectors.models import Sector
from django.views.generic.simple import direct_to_template, redirect_to
from django.core.urlresolvers import reverse


urlpatterns = patterns('', 
    url(r'^contracts/search/by-year/', 'fpds.views.annual_chart_data', {}, name='fpds-search-by-year'),
    url(r'^contracts/search/map/', 'fpds.views.map_data', {}, name='fpds-search-map-data'),
    url(r'^contracts/search/summary/csv/state/', 'fpds.views.summary_statistics_csv', {'first_column_label': 'State', 'data_fetcher': '_get_state_summary_data'}, name='fpds-search-summary-csv-state'),    
    url(r'^contracts/search/summary/csv/program/', 'fpds.views.summary_statistics_csv', {'first_column_label': 'CFDA Program', 'data_fetcher': '_get_program_summary_data'}, name='fpds-search-summary-csv-program'),    
    url(r'^contracts/search/summary/', 'fpds.views.summary_statistics', {}, name='fpds-search-summary')
)


if settings.DEBUG:
    urlpatterns += patterns('', url(r'^test/', 'fpds.views.run_tests', {}, name='fpds-tests'))