from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    url(r'^airports/(?P<code>[A-Za-z0-9@*+]+)', 'aip.views.portdata', name='aip-airport-data'),
    url(r'^search/$', 'aip.views.index', name='aip-index'),
    url(r'results/csv', 'aip.views.get_csv_from_search', name='aip-csv-download'),
    url(r'$', direct_to_template, {'template': 'aip/story.html'}, name='aip-story')

)
