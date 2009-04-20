from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^morsel-save\/(?P<morsel_path>.*?)$', 'morsels.views.ajax_save_morsel', name="morsels_ajax_save"),
)