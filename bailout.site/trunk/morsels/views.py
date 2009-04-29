from rcsfield.backends import backend
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from morsels.models import Morsel
import urllib

@login_required
def ajax_save_morsel(request, morsel_path):
    """
    Save a POSTed revision to a jEditable textarea
    """
    if request.method=='POST':
        
        if not morsel_path.startswith('/'):
            morsel_path = '/' + morsel_path 
        key = request.POST['id']
        content = request.POST['value']
        m = Morsel.objects.get_for_url(url=urllib.unquote(morsel_path), name=key)        
        
        if m:
            # only bother saving it if something has changed -- otherwise the rcsfield integration will throw a git error
            if m.content!=content:
                m.content = content
                m.save()
            return HttpResponse(content, mimetype='text/html')
        else:
            print "key: %s" % key
            print "morsel_path: %s" % morsel_path
            error_msg = """
            <p style="color:red; font-weight: bold">Save failed. Please copy your work to a safe location and then reload the page.</p>
            
            <!-- ### YOUR WORK BEGINS BELOW THIS LINE ### -->
            
            %s
            """ % content            
            return HttpResponse(error_msg, mimetype='text/html')
