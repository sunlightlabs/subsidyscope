from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from sectors.models import Sector
from django.views.generic.simple import direct_to_template, redirect_to


urlpatterns = patterns('', 
    # url(r'^direct-expenditures/search/by-year/', 'faads.views.annual_chart_data', {'sector_name': 'transportation'}, name='transportation-faads-search-by-year'),
)
