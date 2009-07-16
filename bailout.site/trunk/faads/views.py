from django.conf import settings
from django import forms
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from morsels.models import Page
from cfda.models import ProgramDescription
from faads.models import *
from sectors.models import Sector
from haystack.query import SearchQuerySet
from decimal import Decimal
import faads.search
import re
from django.core.urlresolvers import reverse
import zlib
import base64
import urllib
import pickle


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_FAADS_SEARCH_RESULTS_PER_PAGE', getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20))

def MakeFAADSSearchFormClass(sector=None):
    
    cfda_programs = ProgramDescription.objects.all()
    if sector is not None:
        cfda_programs = cfda_programs.filter(sectors=sector)
    cfda_program_choices = []
    for c in cfda_programs:
        cfda_program_choices.append( (str(c.program_number), c.program_title) )
    
    action_type_options = (
        ("A", "New assistance action"),
        ("B", "Continuation"),
        ("C", "Revision"),
    )

    # TODO: provide per-sector options. right now categories without transportation FAADS entries have been manually omitted
    assistance_type_options = (
        (3, "Formula grant"),
        (4, "Project grant"),
        (5, "Cooperative agreement"),
        (6, "Direct payment"),
        (7, "Direct loan"),
        (8, "Guaranteed/insured loan"),
    )
    
    recipient_type_options = (
        (0, "State government"),
        (1, "County government"),
        (2, "City or township government"),
        (4, "Special district government"),
        (5, "Independent school district"),
        (6, "State controlled institution of higher education"),
        (11, "Indian tribe"),
        (12, "Other nonprofit"),
        (20, "Private higher education"),
        (21, "Individual"),
        (22, "Profit organization"),
        (23, "Small business"),
        (25, "All other")
    )
    
    class FAADSSearchForm(forms.Form):
      
        # free text query
        text_query = forms.CharField(label='Text Search', required=False, max_length=100)
        text_query_type = forms.TypedChoiceField(label='Text Search Target', widget=forms.RadioSelect, choices=((0, 'Recipient Name'), (1, 'Project Description'), (2, 'Both')), initial=2, coerce=int)
        
        # CFDA programs and tags
        cfda_programs = forms.MultipleChoiceField(label="CFDA Program", choices=cfda_program_choices, required=False, initial=map(lambda x: x[0], cfda_program_choices), widget=forms.SelectMultiple(attrs={'class':'fieldwidth-230px'}))
        tags = forms.ChoiceField(choices=(('-', 'Select CFDA Programs by Function'), ('tag1', 'Tag 1'), ('tag2', 'Tag 2')), initial=('-'), required=False, widget=forms.Select(attrs={'class':'fieldwidth-230px'}))

        assistance_type = forms.MultipleChoiceField(label="Assistance Type", choices=assistance_type_options, initial=map(lambda x: x[0], assistance_type_options))
        action_type = forms.MultipleChoiceField(label="Action Type", choices=action_type_options, initial=map(lambda x: x[0], action_type_options))        
        recipient_type = forms.MultipleChoiceField(label="Recipient Type", choices=recipient_type_options, initial=map(lambda x: x[0], recipient_type_options))
    
        obligation_date_start = forms.DateField(label="Obligation Date Start", required=False)
        obligation_date_end = forms.DateField(label="Obligation Date End", required=False)
    
        obligation_amount_minimum = forms.DecimalField(label="Obligation Amount Minimum", required=False, decimal_places=2, max_digits=12)
        obligation_amount_maximum = forms.DecimalField(label="Obligation Amount Minimum", required=False, decimal_places=2, max_digits=12)
    
        # TODO: recipient state
    
        # TODO: principal place state
    
        # TODO: funding type
    
        # TODO: budget_function
    
    
    return FAADSSearchForm


def search(request, sector_name=None):
    
    page_result_set = None
    cfda_result_set = None
    
    if sector_name is not None:
        sector = Sector.objects.filter(name__icontains=sector_name)
        if len(sector)==1:
            sector = sector[0]
        else:
            sector = None
            
    
    
    if request.method == 'POST' and request.POST.has_key('text_query'):
        
        formclass = MakeFAADSSearchFormClass(sector=sector)            
        form = formclass(request.POST)
        
        if form.is_valid():
            data_string = urllib.quote(base64.b64encode(zlib.compress(pickle.dumps(request.POST))))
            redirect_url = reverse('%s-faads-search' % sector_name) + ('?q=%s' % data_string)
            return HttpResponseRedirect(redirect_url)
            
        
    if request.method == 'GET' and request.GET.has_key('q'):
        
        formclass = MakeFAADSSearchFormClass(sector=sector)            
        form = formclass(pickle.loads(zlib.decompress(base64.b64decode(urllib.unquote(request.GET['q'])))))
        
        if form.is_valid():
            
            faads_search_query = faads.search.FAADSSearch().use_cache(False)
            
            if form.cleaned_data['text_query'] is not None and len(form.cleaned_data['text_query'].strip())>0:
                if form.cleaned_data['text_query_type']==2:
                    faads_search_query = faads_search_query.filter('recipient', form.cleaned_data['text_query']).filter('text', form.cleaned_data['text_query'], faads.search.FAADSSearch.CONJUNCTION_OR)
                elif form.cleaned_data['text_query_type']==1:
                    faads_search_query = faads_search_query.filter('text', form.cleaned_data['text_query'])
                elif form.cleaned_data['text_query_type']==0:
                    faads_search_query = faads_search_query.filter('recipient', form.cleaned_data['text_query'])
            
            if len(form.cleaned_data['cfda_programs'])<len(form.fields['cfda_programs'].choices):
                faads_search_query = faads_search_query.filter('cfda_program', form.cleaned_data['cfda_programs'])
            
            if len(form.cleaned_data['assistance_type'])<len(form.fields['assistance_type'].choices):
                faads_search_query = faads_search_query.filter('assistance_type', form.cleaned_data['assistance_type'])
                
            if len(form.cleaned_data['recipient_type'])<len(form.fields['recipient_type'].choices):
                faads_search_query = faads_search_query.filter('recipient_type', form.cleaned_data['recipient_type'])

            if len(form.cleaned_data['action_type'])<len(form.fields['action_type'].choices):
                faads_search_query = faads_search_query.filter('action_type', form.cleaned_data['action_type'])
                
            if form.cleaned_data['obligation_date_start'] is not None or form.cleaned_data['obligation_date_end'] is not None:
                faads_search_query = faads_search_query.filter('obligation_action_date', (form.cleaned_data['obligation_date_start'], form.cleaned_data['obligation_date_end']))

            if form.cleaned_data['obligation_amount_minimum'] is not None or form.cleaned_data['obligation_amount_maximum'] is not None:
                faads_search_query = faads_search_query.filter('total_funding_amount', (form.cleaned_data['obligation_amount_minimum'], form.cleaned_data['obligation_amount_maximum']))

            faads_results = faads_search_query.get_haystack_queryset()

            # while True:
            #     print "filling cache"
            #     cache_length = len(faads_results._result_cache)
            #     faads_results._fill_cache()                                
            #     new_cache_length = len(faads_results._result_cache)                
            #     if new_cache_length==cache_length or new_cache_length>=RESULTS_PER_PAGE:
            #         break                
                                    
            paginator = Paginator(faads_results, RESULTS_PER_PAGE)

            # print dir(faads_results)
            # print "### %d" % len(faads_results)
            # print dir(paginator)
            # print paginator.count, paginator.per_page, paginator.num_pages
        
            try:
                page = int(request.GET.get('page','1'))
            except Exception, e:
                page = 1
            
            try:
                faads_results_page = paginator.page(page)
            except (EmptyPage, InvalidPage):
                faads_results_page = paginator.page(paginator.num_pages)
            
            # print faads_results_page.object_list
            
            # if faads_results_page:
            #     django_id_list = map(lambda x: int(getattr(x, 'pk', -1)), faads_results_page.object_list)
            #     alt_django_id_list = map(lambda x: int(getattr(x,'id',-1).replace('faads.record.','')), faads_results_page.object_list)
            #     print django_id_list
            #     print '---------------'
            #     print alt_django_id_list
            #     faads_results_page.django_object_list = Record.objects.in_bulk(django_id_list)
        
            ran_search = True
        
            querystring = "&q=%s" % request.GET['q']
        
        
    else:
        ran_search = False
        querystring = ''
        faads_results_page = None
        formclass = MakeFAADSSearchFormClass(sector=sector)
        form = formclass()
        
    return render_to_response('faads/search/search.html', {'faads_results':faads_results_page, 'form':form, 'ran_search': ran_search, 'querystring': querystring})


