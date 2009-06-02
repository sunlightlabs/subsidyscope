from django.conf.urls.defaults import *
from haystack.views import SearchView


urlpatterns = patterns('search.views',
    url(r'^$', SearchView(), name='haystack_search'),
    url(r'^test/((?P<id>[0-9]*))/$', 'template_test', name='haystack_search'),
)
