from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    url(r'^$', 'aip.views.index', name='aip-index')


)
