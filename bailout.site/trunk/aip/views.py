# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from aip.models import *

def index(request):
   return render_to_response('aip/index.html')
