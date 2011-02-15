from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'contractsort.views.main', name='contractsort-main'),
    url(r'^sector/(?P<sector_id>[0-9]+)/$', 'contractsort.views.sector', name='contractsort-sector'),
    url(r'^sector/(?P<sector_id>[0-9]+)/updateagencies', 'contractsort.views.update_agency', name='contractsort-update-agency'),
    )
