from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    url(r'^airports/(?P<code>[A-Za-z0-9*+]+)', 'aip.views.portdata', name='aip-airport-data'),
    url(r'^$', 'aip.views.index', name='aip-index')
)
