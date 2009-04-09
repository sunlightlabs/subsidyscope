from django.db import models
from django.conf import settings

if 'sites' in settings.INSTALLED_APPS:
    SITES = True
    from django.contrib.flatpages.models import Site
else:
    SITES = False

class MorselManager(models.Manager):
    def get_for_current(self, context, name, inherit=False):
        if not context.has_key('request'):
            return None

        url = context['request'].path
        page = context.get('page', None)
        if page is not None:
            ix = url.rfind('%d/' % page)
            if ix != -1:
                url = url[:ix]
    
        path = url[:-1].split('/')
        urls = ['/'.join(path + [name])]
        while inherit is True and len(path) > 1:
            path = path[:-1]
            urls.append('/'.join(path + [name]))
    
        qs = self.get_query_set()
        if SITES:
            qs = qs.filter(sites=Site.objects.get_current())
        try:
            return qs.filter(url__in=urls).order_by('-url')[0]
        except IndexError:
            return None
