# From http://www.djangosnippets.org/snippets/540/
print "Loading Django models..."
from django.db.models.loading import get_models
for m in get_models():
    exec "from %s import %s" % (m.__module__, m.__name__)
print "Django models loaded."
