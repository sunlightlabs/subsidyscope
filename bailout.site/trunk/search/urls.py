from django.conf.urls.defaults import *
from haystack.views import SearchView


urlpatterns = patterns('search.views',
    url(r'^test/((?P<id>[0-9]*))/$', 'template_test', name='haystack_search_test'),
    url(r'^$', 'main_search_view', name='haystack_search_view')
)
