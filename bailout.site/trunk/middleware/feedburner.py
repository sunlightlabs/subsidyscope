from django.http import HttpResponseRedirect
import settings


class FeedburnerMiddleware(object):
    '''
    Redirect the user to a feedburner feed for basic feeds
    '''
    def process_request(self, request):
        r = request.path.split('/')        
        
        # make sure we have some settings and that this is a feeds/* URL
        if not settings.FEEDBURNER or \
            not len(r)>1 or \
            not r[1]=='feeds':
            return None
        
        if len(r[-1])==0: # remove trailing blank, if one exists
            r = r[:-1]   
        
        # ensure we have a mapping for this URL in settings.py
        if not '/'.join(r[1:]) in settings.FEEDBURNER.keys():
            return None
        
        if request.META['HTTP_USER_AGENT'].startswith('FeedBurner'):
            return None
        else:
            return HttpResponseRedirect(settings.FEEDBURNER['/'.join(r[1:])])
