
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns( '', 
    url(r'^systems/', 'transit.views.index', name='transit-search'),
    url(r'^system/(?P<trs_id>[0-9]+)/$', 'transit.views.transitSystem', name='transit-system'),
    url(r'^system/(?P<trs_id>[0-9]+)/matrix/(?P<year>[0-9]+)/$', 'transit.views.matrixReloader', name='matrix-reloader'),
    url(r'^system/(?P<trs_id>[0-9]+)/(?P<category>\w+)/(?P<year>\w+)/$', 'transit.views.chartReloader', name='chart-reloader'),
    url(r'$', direct_to_template, {'template': 'transportation/mode_page.html', 'extra_context':{'subsector': 5}}, name='transportation-transit'),
)
