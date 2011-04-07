from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'contractsort.views.main', name='contractsort-main'),
    url(r'^sector/(?P<sector_id>[0-9]+)/$', 'contractsort.views.sector', name='contractsort-sector'),
    url(r'^sector/(?P<sector_id>[0-9]+)/updateagencies', 'contractsort.views.update_agency', name='contractsort-update-agency'),
    url(r'setcodes/(?P<sector>[0-9]+)', 'contractsort.views.setcodes'),
    url(r'getcode', 'contractsort.views.getcode'),
    url(r'^login/$', 'contractsort.views.login', name='contractsort-login'),
    url(r'^logout/$', 'contractsort.views.logout', name='contractsort-logout'),
    )
