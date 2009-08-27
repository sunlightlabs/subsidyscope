from django.conf import settings
from django import forms
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from morsels.models import Page
from tagging.models import TaggedItem, Tag
from cfda.models import ProgramDescription, CFDATag
from faads.models import *
from faads.widgets import *
from sectors.models import Sector, Subsector
from geo.models import State
from haystack.query import SearchQuerySet
from geo.models import State
from cfda.views import buildChart
from decimal import Decimal
import faads.search
import re
from django.core.urlresolvers import reverse
import zlib
import base64
import urllib
import pickle


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_FAADS_SEARCH_RESULTS_PER_PAGE', getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20))

def MakeFAADSSearchFormClass(sector=None, subsectors=[]):
    
    # fill CFDA program list
    cfda_programs = ProgramDescription.objects.all()
    if sector is not None:
        cfda_programs = cfda_programs.filter(sectors=sector)
    cfda_program_choices = []
    initial_cfda_program_choices = []
    for c in cfda_programs:
        cfda_program_choices.append( (c.id, '<span class="cfda-program-details">(<a href="%s">details</a>)</span>%s' % (reverse('transportation-cfda-programpage', None, (c.id,)), c.program_title)) )        
        # if no subsector has been defined, check all boxes
        if len(subsectors)==0:
            initial_cfda_program_choices.append(c.id)
        # if a subsector was defined, only check the programs within it
        else:
            for subsector in c.subsectors.all():
                if subsector in subsectors:
                    initial_cfda_program_choices.append(c.id)
                    break

    # subsectors
    subsector_choices = None
    if sector is not None:
        subsector_choices = map(lambda x: (x.id, x.name), Subsector.objects.filter(parent_sector=sector).order_by('name'))
        
    
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

    tag_choices = []
    cfda_program_tags = CFDATag.objects.all().order_by('tag_name')
    tag_choices = map(lambda x: (x.id, x.tag_name), cfda_program_tags)
    enabled_tags = CFDATag.objects.filter(search_default_enabled=True)
    initial_tag_choices = map(lambda x: x.id, enabled_tags)
    
    class FAADSSearchForm(forms.Form):
      
        # free text query
        text_query = forms.CharField(label='Text Search', required=False, max_length=100)
        text_query_type = forms.TypedChoiceField(label='Text Search Target', widget=forms.RadioSelect, choices=((0, 'Recipient Name'), (1, 'Project Description'), (2, 'Both')), initial=2, coerce=int)
        
        # CFDA programs, subsectors and tags
        cfda_program_selection_choices = (('tag', 'Tag'), ('subsector', 'Subsector'), ('program', 'Program'))
        if not subsector_choices:
            cfda_program_selection_choices = (('tag', 'Tag'), ('program', 'Program'))
        
        cfda_program_selection_method = forms.TypedChoiceField(label="Choose programs by", widget=forms.RadioSelect, choices=cfda_program_selection_choices, initial=(len(subsectors)>0) and 'subsector' or 'tag')

        program_selection_programs = forms.MultipleChoiceField(label="CFDA Program", choices=cfda_program_choices, required=False, initial=initial_cfda_program_choices, widget=CheckboxSelectMultipleMulticolumn(columns=2))
        
        program_selection_tags = forms.MultipleChoiceField(choices=tag_choices, required=False, initial=initial_tag_choices, widget=CheckboxSelectMultipleMulticolumn(columns=3))
        tags_exclude_secondary = forms.BooleanField(label="Only include programs having the selected tag(s) as their primary function?", required=False, initial=True)

        if subsector_choices:
            program_selection_subsector = forms.MultipleChoiceField(choices=subsector_choices, required=False, widget=CheckboxSelectMultipleMulticolumn(columns=3))
        else:
            program_selection_subsector = False

        assistance_type = forms.MultipleChoiceField(label="Assistance Type", choices=assistance_type_options, initial=map(lambda x: x[0], assistance_type_options), widget=forms.CheckboxSelectMultiple)
        action_type = forms.MultipleChoiceField(label="Action Type", choices=action_type_options, initial=map(lambda x: x[0], action_type_options), widget=forms.CheckboxSelectMultiple)
        recipient_type = forms.MultipleChoiceField(label="Recipient Type", choices=recipient_type_options, initial=map(lambda x: x[0], recipient_type_options), widget=forms.CheckboxSelectMultiple)
    
        obligation_date_start = forms.DateField(label="Obligation Date Start", required=False)
        obligation_date_end = forms.DateField(label="Obligation Date End", required=False)
    
        obligation_amount_minimum = forms.DecimalField(label="Obligation Amount Minimum", required=False, decimal_places=2, max_digits=12)
        obligation_amount_maximum = forms.DecimalField(label="Obligation Amount Minimum", required=False, decimal_places=2, max_digits=12)
        
        state_choices = map(lambda x: (x.id, x.name), State.objects.all().order_by('name'))
        location_type = forms.TypedChoiceField(label='Location Type', widget=forms.RadioSelect, choices=((0, 'Recipient Location'), (1, 'Principal Place of Performance')), initial=1, coerce=int)
        location_choices = forms.MultipleChoiceField(label='State', choices=state_choices, initial=map(lambda x: x[0], state_choices), widget=CheckboxSelectMultipleMulticolumn(columns=4))
    
        # TODO: funding type
    
        # TODO: budget_function
    
    
    return FAADSSearchForm

def compress_querydict(obj):
    return urllib.quote(base64.b64encode(zlib.compress(pickle.dumps(obj))))

def decompress_querydict(s):
    return pickle.loads(zlib.decompress(base64.b64decode(urllib.unquote(s))))

def get_sector_by_name(sector_name=None):
    if sector_name is not None:
        sector = Sector.objects.filter(name__icontains=sector_name)
        if len(sector)==1:
            sector = sector[0]
        else:
            sector = None
    return sector


def construct_form_and_query_from_querydict(sector_name, querydict_as_compressed_string):
    """ Returns a form object and a FAADSSearch object that have been constructed from a search key (a compressed POST querydict) """

    # retrieve the sector and create an appropriate form object to handle validation of the querydict
    sector = get_sector_by_name(sector_name)
    formclass = MakeFAADSSearchFormClass(sector=sector)            
    form = formclass(decompress_querydict(querydict_as_compressed_string))

    # validate querydict -- no monkey business!
    if form.is_valid():
    
        faads_search_query = faads.search.FAADSSearch()
    
        # handle text search
        if form.cleaned_data['text_query'] is not None and len(form.cleaned_data['text_query'].strip())>0:
            if form.cleaned_data['text_query_type']==2:
                faads_search_query = faads_search_query.filter('recipient', form.cleaned_data['text_query']).filter('text', form.cleaned_data['text_query'], faads.search.FAADSSearch.CONJUNCTION_OR)
            elif form.cleaned_data['text_query_type']==1:
                faads_search_query = faads_search_query.filter('text', form.cleaned_data['text_query'])
            elif form.cleaned_data['text_query_type']==0:
                faads_search_query = faads_search_query.filter('recipient', form.cleaned_data['text_query'])
    
        
        # handle program selection
        # by tag
        if form.cleaned_data['cfda_program_selection_method']=='tag':
            if form.cleaned_data['tags_exclude_secondary']:
                programs_with_tag = ProgramDescription.objects.filter(primary_tag__id__in=form.cleaned_data['program_selection_tags'])
            else:
                programs_with_tag = ProgramDescription.objects.filter(Q(primary_tag__id__in=form.cleaned_data['program_selection_tags']) | Q(secondary_tags__id__in=form.cleaned_data['program_selection_tags']))

            if len(programs_with_tag):
                faads_search_query = faads_search_query.filter('cfda_program', map(lambda x: x.id, programs_with_tag))
        # by subsector
        elif form.cleaned_data['cfda_program_selection_method']=='subsector':
            programs_in_subsector = ProgramDescription.objects.filter(subsectors__id__in=(form.cleaned_data['program_selection_subsectors']))
            if len(programs_in_subsector):
                faads_search_query = faads_search_query.filter('cfda_program', map(lambda x: x.id, programs_in_subsector))
        # by CFDA program 
        elif form.cleaned_data['cfda_program_selection_method']=='program':
            selected_programs = form.cleaned_data['program_selection_programs']
            if len(selected_programs):
                faads_search_query = faads_search_query.filter('cfda_program', form.cleaned_data['program_selection_programs'])
            
        # handle assistance type
        if len(form.cleaned_data['assistance_type'])<len(form.fields['assistance_type'].choices):
            faads_search_query = faads_search_query.filter('assistance_type', form.cleaned_data['assistance_type'])
        
        # handle recipient type
        if len(form.cleaned_data['recipient_type'])<len(form.fields['recipient_type'].choices):
            faads_search_query = faads_search_query.filter('recipient_type', form.cleaned_data['recipient_type'])

        # handle action type
        if len(form.cleaned_data['action_type'])<len(form.fields['action_type'].choices):
            faads_search_query = faads_search_query.filter('action_type', form.cleaned_data['action_type'])
        
        # handle obligation date range
        if form.cleaned_data['obligation_date_start'] is not None or form.cleaned_data['obligation_date_end'] is not None:
            faads_search_query = faads_search_query.filter('obligation_action_date', (form.cleaned_data['obligation_date_start'], form.cleaned_data['obligation_date_end']))

        # handle obligation amount range
        if form.cleaned_data['obligation_amount_minimum'] is not None or form.cleaned_data['obligation_amount_maximum'] is not None:
            faads_search_query = faads_search_query.filter('total_funding_amount', (form.cleaned_data['obligation_amount_minimum'], form.cleaned_data['obligation_amount_maximum']))

        # handle location
        if len(form.cleaned_data['location_choices'])>0 and len(form.cleaned_data['location_choices'])<State.objects.all().count():
            if form.cleaned_data['location_type']==0:
                print 'filtering by recipient state against IDs like %s' % ', '.join(form.cleaned_data['location_choices'])
                faads_search_query = faads_search_query.filter('recipient_state', form.cleaned_data['location_choices'])
            elif form.cleaned_data['location_type']==1:
                print 'filtering by principal place of performance against IDs like %s' % ', '.join(form.cleaned_data['location_choices'])
                faads_search_query = faads_search_query.filter('principal_place_state', form.cleaned_data['location_choices'])
            # elif form.cleaned_data['location_type']==2:
            #     faads_search_query = faads_search_query.filter('recipient_state', form.cleaned_data['location_choices'])
            #     faads_search_query = faads_search_query.filter('principal_place_state', form.cleaned_data['location_choices'], faads_search_query.CONJUNCTION_OR)

        return (form, faads_search_query)

    else:
        raise(Exception("Data in querydict did not pass form validation"))


def search(request, sector_name=None):
    
    # default values, for safety's sake
    form = None
    query = ''
    encoded_querystring = ''
    ran_search = False
    faads_results_page = None
    
    # retrieve the sector object based on the passed name
    sector = get_sector_by_name(sector_name)
    
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
                    
            (form, faads_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            
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
    
            query = urllib.quote(request.GET['q'])

        
        # we just wandered into the search without a prior submission        
        else:
        
            subsectors = []
            if sector is not None and request.GET.has_key('subsectors'):
                re_sanitize = re.compile(u'[^\,\d]')
                querystring_input = re_sanitize.sub('', request.GET['subsectors']) # sanitize querystring input, because why not?
                subsector_ids = []
                try:
                    subsector_ids = querystring_input.split(",")
                except:
                    pass
                subsectors = Subsector.objects.filter(parent_sector=sector).filter(id__in=subsector_ids)        
        
            ran_search = False
            query = ''
            faads_results_page = None
            formclass = MakeFAADSSearchFormClass(sector=sector, subsectors=subsectors)
            form = formclass()
        
    return render_to_response('faads/search/search.html', {'faads_results':faads_results_page, 'form':form, 'ran_search': ran_search, 'query': query}, context_instance=RequestContext(request))

def annual_chart_data(request, sector_name=None):

    
    if request.method == 'GET':
        if request.GET.has_key('q'):
        
            (form, faads_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            
                   
            faads_results = faads_search_query.aggregate('fiscal_year')
    
            chart_json = buildChart(faads_results)
            
            return HttpResponse(chart_json, mimetype="text/plain")

    return Http404()


def map_data(request, sector_name=None):
    

        
    # need to translate the state_id back to FIPS codes for the map and normalize by population 
    # grabbing a complete list of state objects and building a table for translation
    states = {}
    
    for state in State.objects.all():
    
        states[state.id] = state
        
    
    if request.method == 'GET':
        if request.GET.has_key('q'):
        
            (form, faads_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            
                   
            faads_results = faads_search_query.aggregate('recipient_state')

            max_state_total = 0
            max_per_capital_total = 0
            
            per_capita_totals = {}
            
            for state_id in faads_results:
                if states.has_key(state_id) and states[state_id].population:
                    per_capita_totals[state_id] =  faads_results[state_id] / states[state_id].population
                    
                    if per_capita_totals[state_id] > max_per_capital_total:
                        max_per_capital_total = per_capita_totals[state_id]
                    
                    if faads_results[state_id] > max_state_total:
                        max_state_total = faads_results[state_id]
                    
        
            results = []
            
            for state_id in per_capita_totals:
                if states.has_key(state_id):
                    line = '%d,%.02f,%.03f,%.02f,%.03f' % (states[state_id].fips_state_code, 
                                                           faads_results[state_id], 
                                                           faads_results[state_id] / max_state_total, 
                                                           per_capita_totals[state_id],
                                                           per_capita_totals[state_id] / max_per_capital_total)

                    results.append(line)
                
            
            return HttpResponse('\n'.join(results), mimetype="text/plain")
                
    return Http404()

