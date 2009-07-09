from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from sectors.models import Sector
from django.views.generic.simple import direct_to_template, redirect_to



urlpatterns = patterns('', 
    url(r'^direct-payments/search/', 'faads.views.search', {'sector_name': 'transportation'}, name='transportation-faads-search'),
    url(r'^direct-payments/', direct_to_template, {'template': 'transportation/direct_payments.html'}, name='transportation-direct-payments'),
    url(r'^tax-expenditures/', direct_to_template, {'template': 'transportation/tax_expenditures.html'}, name='transportation-tax-expenditures'),
    url(r'^contracts/', direct_to_template, {'template': 'transportation/contracts.html'}, name='transportation-contracts'),
    url(r'^backgrounders/', direct_to_template, {'template': 'transportation/backgrounders.html'}, name='transportation-backgrounders'),
    url(r'^docs/', direct_to_template, {'template': 'transportation/docs.html'}, name='transportation-docs'),
    url(r'^$', direct_to_template, {'template': 'transportation/index.html'}, name='transportation-index')
)