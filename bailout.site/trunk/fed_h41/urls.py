from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^\.xml$', 'fed_h41.views.h41_xml', name="h41_snapshot_xml"),        
)