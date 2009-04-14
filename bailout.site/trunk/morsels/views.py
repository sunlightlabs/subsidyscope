from rcsfield.backends import backend
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from morsels.models import Morsel

@login_required
def save_revision(request, morsel_path):
    """
    Save a POSTed revision to a jEditable textarea
    """
    if request.method=='POST':        
        key = request.POST['id']
        content = request.POST['value']        
        m = Morsel.objects.get_for_url(url=morsel_path, name=key)
        m.content = content
        m.save()
        
        return HttpResponse(content, mimetype='text/plain')
