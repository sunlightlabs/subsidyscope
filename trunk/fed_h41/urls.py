from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    url(r'^\.xml$', 'fed_h41.views.h41_xml', name="h41_snapshot_xml"),      
    url(r'^\.csv$', redirect_to, {'url':'/media/data/bailout/federal_reserve_h41.csv'}, name="h41_snapshot_csv"),
    url(r'^\/news\.xml$', 'fed_h41.views.fed_news_xml', name="fed_news_xml"),        
)