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

    tag_choices = [('', 'Select CFDA Programs by Function')]
    cfda_program_tags = ProgramDescription.tags.all().order_by('name')
    for tag in cfda_program_tags:
        tag_choices.append( (','.join(map(lambda x: "%2.3f" % x.program_number, ProgramDescription.objects.filter(primary_tag=tag))), tag.name) )
    
    class FAADSSearchForm(forms.Form):
      
        # free text query
        text_query = forms.CharField(label='Text Search', required=False, max_length=100)
        text_query_type = forms.TypedChoiceField(label='Text Search Target', widget=forms.RadioSelect, choices=((0, 'Recipient Name'), (1, 'Project Description'), (2, 'Both')), initial=2, coerce=int)
        
        # CFDA programs and tags
        cfda_programs = forms.MultipleChoiceField(label="CFDA Program", choices=cfda_program_choices, required=False, initial=map(lambda x: x[0], cfda_program_choices), widget=forms.SelectMultiple(attrs={'class':'fieldwidth-230px'}))
        tags = forms.ChoiceField(choices=tag_choices, initial=('-'), required=False, widget=forms.Select(attrs={'class':'fieldwidth-230px'}))

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

def compress_querydict(obj):
    return urllib.quote(base64.b64encode(zlib.compress(pickle.dumps(obj))))

def decompress_querydict(s):
    return pickle.loads(zlib.decompress(base64.b64decode(urllib.unquote(s))))

def search(request, sector_name=None):
    
    # default values, for safety's sake
    form = None
    querystring = ''
    ran_search = False
    faads_results_page = None
    
    # retrieve the sector object based on the passed name
    if sector_name is not None:
        sector = Sector.objects.filter(name__icontains=sector_name)
        if len(sector)==1:
            sector = sector[0]
        else:
            sector = None    
    
    # if this is a POSTback, package the request into a querystring and redirect
    if request.method == 'POST' and request.POST.has_key('text_query'):        
        formclass = MakeFAADSSearchFormClass(sector=sector)            
        form = formclass(request.POST)
        
        if form.is_valid():
            redirect_url = reverse('%s-faads-search' % sector_name) + ('?q=%s' % compress_querydict(request.POST))
            return HttpResponseRedirect(redirect_url)
            
    # if this is a get w/ a querystring, unpack the form 
    if request.method == 'GET':
        if request.GET.has_key('q'):
        
            formclass = MakeFAADSSearchFormClass(sector=sector)            
            form = formclass(decompress_querydict(request.GET['q']))
        
            if form.is_valid():
            
                faads_search_query = faads.search.FAADSSearch()
            
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

          
                paginator = Paginator(faads_results, RESULTS_PER_PAGE)
                try:
                    page = int(request.GET.get('page','1'))
                except Exception, e:
                    page = 1
            
                try:
                    faads_results_page = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    faads_results_page = paginator.page(paginator.num_pages)        
        
                ran_search = True
        
                querystring = "&q=%s" % urllib.quote(request.GET['q'])
        
        # we just wandered into the search without a prior submission        
        else:
            ran_search = False
            querystring = ''
            faads_results_page = None
            formclass = MakeFAADSSearchFormClass(sector=sector)
            form = formclass()
        
    return render_to_response('faads/search/search.html', {'faads_results':faads_results_page, 'form':form, 'ran_search': ran_search, 'querystring': querystring})


