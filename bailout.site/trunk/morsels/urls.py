from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^save-revision\/(?P<morsel_path>.*?)$', 'morsels.views.save_revision', name="morsels_save_revision"),
)