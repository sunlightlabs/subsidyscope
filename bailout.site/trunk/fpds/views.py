import unittest
import fpds.tests
from fpds.search import *
import django.test.simple
from django.test.utils import setup_test_environment, teardown_test_environment
from django.http import Http404, HttpResponseRedirect, HttpResponse
import settings

class FPDSTestWrapper(fpds.tests.search):
    """
    Because the Django test framework is a piece of garbage.
    """
    def __init__(self):
        # intentionally not calling the super -- we just need the test methods
        self.errors = []
     
    def displayerrors(self):
        for e in self.errors:
            print e
    
    def failUnlessEqual(self, a, b):
        if a!=b:
            self.errors.append("%s is not equal to %s" % (a,b))
        return
    
    def run(self):
        for m in dir(self):
            if m[:4]=="test":
                func = getattr(self, m)
                func()

        
  
def run_tests(request):
    
    f = FPDSTestWrapper()
    f.run()    
    
    return HttpResponse("\n".join(f.errors), mimetype='text/plain')
    