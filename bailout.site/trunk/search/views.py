from django.conf import settings
from django import forms
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from morsels.models import Page
from cfda.models import ProgramDescription

from haystack.query import SearchQuerySet

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    #search_scope = forms.ChoiceField(choices=(('all', 'All'),('cfda','CFDA Programs'),('site','Site Pages')))

def template_test(request, id):
    
    cfda = ProgramDescription.objects.get(id=id)
    
    return render_to_response('search/indexes/cfda/programdescription_text.txt', {'object':cfda})

def main_search_view(request):
    
    page_result_set = None
    cfda_result_set = None
    
    if request.method == 'GET' and request.GET.has_key('query'):
        
        form = SearchForm(request.GET)
        
        if form.is_valid():
            query = form.cleaned_data['query']
            page_result_set = SearchQuerySet().auto_query(query).models(Page).highlight()
            
#            if form.cleaned_data.has_key('search_scope'):
#                search_scope = form.cleaned_data['search_scope']
#            else:
#                search_scope = 'all'
#            
#            
#            if search_scope == 'site' or search_scope == 'all':
#                page_result_set = SearchQuerySet().auto_query(query).highlight()
#                
#            if search_scope == 'cfda' or search_scope == 'all':
#                cfda_result_set = SearchQuerySet().models(ProgramDescription).auto_query(query)
        
    else:
        form = SearchForm()
        
    return render_to_response('search/search.html', {'page_result_set':page_result_set, 'cfda_result_set':cfda_result_set, 'form':form})


