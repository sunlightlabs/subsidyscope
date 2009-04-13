from rcsfield.backends import backend
from django.http import HttpResponse

def get_revision(request):
    if request.method=='GET':        
        key = request.GET['key']
        rev = request.GET['rev']
        text = backend.fetch(key, rev)
        return HttpResponse(text, mimetype='text/plain')
        