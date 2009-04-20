from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^get-revision\/$', 'rcsfield.views.get_revision', name="rcsfield_get_revision"),
)