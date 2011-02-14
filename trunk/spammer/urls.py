from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('spammer.views',
    url(r'^subscribe/$', 'subscribe', name="mailinglist_subscribe"),
    url(r'^unsubscribe/(?P<hashcode>\w+)/$', 'unsubscribe', name="mailinglist_unsubscribe"),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^subscribed/$', 'direct_to_template', {'template': 'spammer/subscribed.html'}, name="mailinglist_subscribed"),
)

if getattr(settings, 'SPAMMER_EXPOSE_LIST', False):
    urlpatterns += patterns('spammer.views',
        url(r'^export/$', 'export_csv', name='subscribers_csv')
)