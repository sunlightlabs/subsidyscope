from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from morsels.models import Page

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)

def template_test(request, id):
    
    page = Page.objects.get(id=id)
    
    return render_to_response('search/indexes/morsels/page_text.txt', {'object':page})