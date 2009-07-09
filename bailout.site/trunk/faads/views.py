from django.conf import settings
from django import forms
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from morsels.models import Page
from cfda.models import ProgramDescription
from faads.models import *
from sectors.models import Sector
from haystack.query import SearchQuerySet
from decimal import Decimal

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


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
        text_query_type = forms.TypedChoiceField(label='Text Search Target', widget=forms.RadioSelect, choices=((0, 'Recipient'), (1, 'Description'), (2, 'Both')), coerce=int)
        
        # CFDA programs and tags
        cfda_program = forms.MultipleChoiceField(label="CFDA Program", choices=cfda_program_choices, required=False)
        tags = forms.MultipleChoiceField(choices=(('tag1', 'Tag 1'), ('tag2', 'Tag 2')), required=False)

        assistance_type = forms.MultipleChoiceField(label="Assistance Type", choices=assistance_type_options)
        action_type = forms.MultipleChoiceField(label="Action Type", choices=action_type_options)        
        recipient_type = forms.MultipleChoiceField(label="Recipient Type", choices=recipient_type_options)
    
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
            
    
    
    if request.method == 'GET' and request.GET.has_key('query'):
        
        formclass = MakeFAADSSearchFormClass(sector=sector)
        form = formclass(request.GET)
        
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
        formclass = MakeFAADSSearchFormClass(sector=sector)
        form = formclass(request.GET, initial={'text_query':'xyz'})
        
    return render_to_response('faads/search/search.html', {'page_result_set':page_result_set, 'cfda_result_set':cfda_result_set, 'form':form})


