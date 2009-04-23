from rcsfield.backends import backend
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def get_revision(request):
    if request.method=='GET':        
        key = request.GET['key']
        rev = request.GET['rev']
        text = backend.fetch(key, rev)
        return HttpResponse(text, mimetype='text/plain')
<<<<<<< HEAD:bailout.site/trunk/rcsfield/views.py
        
=======
        
>>>>>>> afe5d271c43b310d7523a47c284081afb4ccc0c0:bailout.site/trunk/rcsfield/views.py
