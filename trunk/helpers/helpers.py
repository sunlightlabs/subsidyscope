from django.http import HttpResponse
from django.db import models

import simplejson

def compare_by (fieldname): 
    def compare_two_dicts (a, b):
        return cmp(a[fieldname], b[fieldname])

class JSONHttpResponse(HttpResponse):
    
    def __init__(self, content=''):
        content = simplejson.dumps(content)
        HttpResponse.__init__(self, content, 'application/json')
        
class FileIterWrapper(object):
    def __init__(self, flo, chunk_size = 1024**2):
        self.flo = flo
        self.chunk_size = chunk_size

    def next(self):
        data = self.flo.read(self.chunk_size)
        if data:
            return data 
        else:
            raise StopIteration

    def __iter__(self):
        return self
    
    
# http://djangosnippets.org/snippets/1295/
class ManyToManyField_NoSyncdb(models.ManyToManyField):
    def __init__(self, *args, **kwargs):
        super(ManyToManyField_NoSyncdb, self).__init__(*args, **kwargs)
        self.creates_table = False