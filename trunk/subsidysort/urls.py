from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from bailout.models import *
from django.views.generic.simple import direct_to_template, redirect_to
import bailout_pdfs
  
urlpatterns = patterns('',
    url(r'^$', 'subsidysort.views.main', name='subsidysort-main'),
    url(r'^sector/(?P<sector_id>[0-9]+)/edit/$', 'subsidysort.views.sector_edit', name='subsidysort-sector-edit'),
    url(r'^sector/(?P<sector_id>[0-9]+)/search/(?P<cfda>[0-9.]+)/$', 'subsidysort.views.sector_search', name='subsidysort-sector-search'),
    url(r'^sector/(?P<sector_id>[0-9]+)/delete/(?P<program_id>[0-9]+)/$', 'subsidysort.views.sector_delete', name='subsidysort-sector-delete'),
    url(r'^sector/(?P<sector_id>[0-9]+)/add/(?P<program_id>[0-9]+)/$', 'subsidysort.views.sector_add', name='subsidysort-sector-add'),
    url(r'^sector/(?P<sector_id>[0-9]+)/$', 'subsidysort.views.sector', name='subsidysort-sector'),
    url(r'^cfda/(?P<program_id>[0-9]+)/save/comment/$', 'subsidysort.views.cfda_save_comment', name='subsidysort-cfda-save-comment'),
    url(r'^cfda/(?P<program_id>[0-9]+)/$', 'subsidysort.views.cfda', name='subsidysort-cfda'),
    url(r'^login/$', 'subsidysort.views.login', name='subsidysort-login'),
    url(r'^logout/$', 'subsidysort.views.logout', name='subsidysort-logout'),
)