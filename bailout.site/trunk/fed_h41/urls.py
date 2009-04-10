from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^\.xml$', 'fed_h41.views.h41_xml', name="h41_snapshot_xml"),      
    url(r'^\.csv$', 'fed_h41.views.h41_csv', name="h41_snapshot_csv"),
    url(r'^\/news\.xml$', 'fed_h41.views.fed_news_xml', name="fed_news_xml"),        
)