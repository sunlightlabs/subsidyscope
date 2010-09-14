from django.conf import settings
from django import forms
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.html import strip_tags
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
from usaspending import *
import re
from django.core.urlresolvers import reverse
import zlib
import urllib
import pickle
import hashlib
import csv
from django.contrib.humanize.templatetags.humanize import intcomma


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
        subsector_choices = map(lambda x: (x.id, ("<span class=\"img-wrapper\" id=\"img-wrapper-%s\">%s</span>" % (str(x.name).lower(), x.name))), Subsector.objects.filter(parent_sector=sector).order_by('weight', 'name'))

    # TODO: provide per-sector options. right now categories without transportation FAADS entries have been manually omitted    
    action_type_codes = ('A', 'B', 'C')
    action_type_options = map(lambda x: (x.id, x.name), ActionType.objects.filter(code__in=action_type_codes).order_by('code'))

    re_assistance_type_tidier = re.compile(r'(\,.*$|\s\([a-z]\))', re.I)
    assistance_type_codes = (3,4,5,6)
    assistance_type_options = map(lambda x: (x.id, re_assistance_type_tidier.sub('',x.name)), AssistanceType.objects.filter(code__in=assistance_type_codes).order_by('code'))
    
    recipient_type_codes = (0,1,2,4,5,6,11,12,20,21,22,23,25)
    recipient_type_options = map(lambda x: (x.id, x.name), RecipientType.objects.filter(code__in=recipient_type_codes).order_by('code'))  

    tag_choices = []
    cfda_program_tags = CFDATag.objects.all().order_by('tag_name')
    tag_choices = map(lambda x: (x.id, x.tag_name), cfda_program_tags)
    enabled_tags = CFDATag.objects.filter(search_default_enabled=True)
    initial_tag_choices = map(lambda x: x.id, enabled_tags)
    
    SUBSECTOR_SYNONYMS = {
        'transportation': 'Mode'
    }
    
    class FAADSSearchForm(forms.Form):
      
        # free text query
        text_query = forms.CharField(label='Text Search', required=False, max_length=100)
        text_query_type = forms.TypedChoiceField(label='Text Search Target', widget=forms.RadioSelect, choices=((0, 'Recipient Name'), (1, 'Project Description'), (2, 'Both')), initial=2, coerce=int)
        
        # CFDA programs, subsectors
        cfda_program_selection_choices = [('program-selection-subsidy_programs','Subsidy Programs')]
        if subsector_choices:
            cfda_program_selection_choices.append(('program-selection-subsector', 'Programs by ' + SUBSECTOR_SYNONYMS.get(sector.name.lower(), 'Subsector')))
        if len(cfda_program_choices)>0:
            cfda_program_selection_choices.append(('program-selection-program', 'All Programs'))
            
        if len(cfda_program_selection_choices)==1:
            cfda_program_selection_method = False       
            program_selection_programs = False
        else:                
            cfda_program_selection_method = forms.TypedChoiceField(label="Choose programs by", widget=TabbedSelectWidget, choices=cfda_program_selection_choices, initial=(len(subsectors)>0) and 'program-selection-subsector' or 'program-selection-subsidy_programs')
            program_selection_programs = forms.MultipleChoiceField(label="CFDA Program", choices=cfda_program_choices, required=False, initial=initial_cfda_program_choices, widget=CheckboxSelectMultipleMulticolumn(columns=2))
        
        if subsector_choices:
            program_selection_subsector = forms.MultipleChoiceField(choices=subsector_choices, required=False, widget=CheckboxSelectMultipleMulticolumn(columns=3))
        else:
            program_selection_subsector = False

        assistance_type = forms.MultipleChoiceField(label="Assistance Type", required=False, choices=assistance_type_options, initial=map(lambda x: x[0], assistance_type_options), widget=forms.CheckboxSelectMultiple)
        action_type = forms.MultipleChoiceField(label="Action Type", required=False, choices=action_type_options, initial=map(lambda x: x[0], action_type_options), widget=forms.CheckboxSelectMultiple)
        recipient_type = forms.MultipleChoiceField(label="Recipient Type", required=False, choices=recipient_type_options, initial=map(lambda x: x[0], recipient_type_options), widget=CheckboxSelectMultipleMulticolumn(columns=2))
    
        obligation_date_start = forms.DateField(label="Obligation Date Start", required=False)
        obligation_date_end = forms.DateField(label="Obligation Date End", required=False)
    
        obligation_amount_minimum = USDecimalHumanizedField(label="Obligation Amount Minimum", required=False, decimal_places=2, max_digits=12)
        obligation_amount_maximum = USDecimalHumanizedField(label="Obligation Amount Maximum", required=False, decimal_places=2, max_digits=12)
        
        state_choices = map(lambda x: (x.id, x.name), State.objects.all())
        location_type = forms.TypedChoiceField(label='Location Type', widget=forms.RadioSelect, choices=((0, 'Recipient Location'), (1, 'Principal Place of Performance'), (2, 'Both')), initial=1, coerce=int)
        location_choices = forms.MultipleChoiceField(label='State', required=False, choices=state_choices, initial=map(lambda x: x[0], state_choices), widget=CheckboxSelectMultipleMulticolumn(columns=4))
    
        sector_name = forms.CharField(label='Sector', required=False, initial=((sector is not None) and sector.name.lower() or ''), max_length=100, widget=forms.HiddenInput)
    
    
    return FAADSSearchForm



def get_excluded_subsidy_program_ids(sector=None):
    excluded_program_ids = []
    
    # there may be an entirely different methodology for each sector
    if sector.name.lower().strip()=='transportation':
        excluded_tag_names = ('safety', 'intergovernmental transfer', 'regulatory enforcement')
        excluded_tags = []
        for tag in excluded_tag_names:
            excluded_tags.extend(CFDATag.objects.filter(tag_name__icontains=tag))        
        programs_with_excluded_primary_tag = ProgramDescription.objects.filter(primary_tag__id__in=map(lambda x:x.id, excluded_tags))
        programs_with_excluded_secondary_tag = ProgramDescription.objects.filter(secondary_tags__id__in=map(lambda x:x.id, excluded_tags))
        excluded_primary = set(map(lambda x: x.id, programs_with_excluded_primary_tag))
        excluded_secondary = set(map(lambda x: x.id, programs_with_excluded_secondary_tag))
        excluded_program_ids = excluded_primary.intersection(excluded_secondary)
        
    return list(excluded_program_ids)



def get_included_subsidy_program_ids(sector=None):
    """ Returns false if all programs should be included """
    excluded_program_ids = set(get_excluded_subsidy_program_ids(sector))
    programs = ProgramDescription.objects.all()
    if sector is not None:
        programs = ProgramDescription.objects.filter(sectors=sector)
    if len(programs)==0:
        return False
    else:
        programs_in_sector_ids = set(map(lambda x: x.id, programs))
        return list(programs_in_sector_ids - excluded_program_ids)
       
       
        
def construct_form_and_query_from_querydict(sector_name, querydict_as_compressed_string):
    """ Returns a form object and a FAADSSearch object that have been constructed from a search key (a compressed POST querydict) """

    # retrieve the sector and create an appropriate form object to handle validation of the querydict
    sector = get_sector_by_name(sector_name)
    querydict = decompress_querydict(querydict_as_compressed_string)
    if (sector is None):
        sector = get_sector_by_name(querydict.get('sector_name', None))

    formclass = MakeFAADSSearchFormClass(sector=sector)            
    form = formclass(querydict)

    # validate querydict -- no monkey business!
    if form.is_valid():
    
        faads_search_query = faads.search.FAADSSearch()
        if sector is not None:
            faads_search_query = faads_search_query.set_sectors(sector)
    
        # handle text search
        if form.cleaned_data['text_query'] is not None and len(form.cleaned_data['text_query'].strip())>0:
            if form.cleaned_data['text_query_type']==2:
                faads_search_query = faads_search_query.filter('all_text', form.cleaned_data['text_query'])
            elif form.cleaned_data['text_query_type']==1:
                faads_search_query = faads_search_query.filter('text', form.cleaned_data['text_query'])
            elif form.cleaned_data['text_query_type']==0:
                faads_search_query = faads_search_query.filter('recipient', form.cleaned_data['text_query'])
    
        
        # handle program selection
        # by tag
        if form.cleaned_data.has_key('cfda_program_selection_method'):
            if form.cleaned_data['cfda_program_selection_method']=='tag':
                if form.cleaned_data['tags_exclude_secondary']:
                    programs_with_tag = ProgramDescription.objects.filter(primary_tag__id__in=form.cleaned_data['program_selection_tags'])
                else:
                    programs_with_tag = ProgramDescription.objects.filter(Q(primary_tag__id__in=form.cleaned_data['program_selection_tags']) | Q(secondary_tags__id__in=form.cleaned_data['program_selection_tags']))
                faads_search_query = faads_search_query.filter('cfda_program', map(lambda x: x.id, programs_with_tag))


            # using subsidyscope's selection of programs
            if form.cleaned_data['cfda_program_selection_method']=='program-selection-subsidy_programs':
                programs = get_included_subsidy_program_ids(sector)
                if programs is not False:
                    faads_search_query = faads_search_query.filter('cfda_program', programs)            

            # by subsector
            elif form.cleaned_data['cfda_program_selection_method']=='program-selection-subsector':
                programs_in_subsector = ProgramDescription.objects.filter(subsectors__id__in=(form.cleaned_data['program_selection_subsector']))
                faads_search_query = faads_search_query.filter('cfda_program', map(lambda x: x.id, programs_in_subsector))
                
            # by CFDA program 
            elif form.cleaned_data['cfda_program_selection_method']=='program-selection-program':
                selected_programs = form.cleaned_data['program_selection_programs']
                faads_search_query = faads_search_query.filter('cfda_program', form.cleaned_data['program_selection_programs'])

        # handle assistance type
        if len(form.cleaned_data['assistance_type'])<len(form.fields['assistance_type'].choices):
            assistance_filter = form.cleaned_data['assistance_type']
            assistance_filter.append(u'39')
            assistance_filter.append(u'40')
            faads_search_query = faads_search_query.filter('assistance_type', assistance_filter)

        
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
            
            if form.cleaned_data['obligation_amount_minimum'] is not None:
                obligation_minimum = int(Decimal(form.cleaned_data['obligation_amount_minimum']))
            else:
                obligation_minimum = None
                
            if form.cleaned_data['obligation_amount_maximum'] is not None:
                obligation_maximum = int(Decimal(form.cleaned_data['obligation_amount_maximum']))
            else:
                obligation_maximum = None
                     
            faads_search_query = faads_search_query.filter('federal_funding_amount', (obligation_minimum, obligation_maximum))

        # handle location
        if len(form.cleaned_data['location_choices'])<State.objects.all().count():
            if form.cleaned_data['location_type']==0:                
                faads_search_query = faads_search_query.filter('recipient_state', form.cleaned_data['location_choices'])
            elif form.cleaned_data['location_type']==1:
                faads_search_query = faads_search_query.filter('principal_place_state', form.cleaned_data['location_choices'])
            elif form.cleaned_data['location_type']==2:
                faads_search_query = faads_search_query.filter('all_states', form.cleaned_data['location_choices'])

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
    found_some_results = False
    year_range_text = None    
    sort_column = 'obligation_date'
    sort_order = 'asc'
    
    # retrieve the sector object based on the passed name
    sector = get_sector_by_name(sector_name)
    
    # if this is a POSTback, package the request into a querystring and redirect
    if request.method == 'POST':
        if request.POST.has_key('text_query'):        
            formclass = MakeFAADSSearchFormClass(sector=sector)            
            form = formclass(request.POST)
            
            if form.is_valid():
                redirect_url = reverse('%s-faads-search' % sector_name) + ('?q=%s' % compress_querydict(request.POST))
                return HttpResponseRedirect(redirect_url)
            
        
        else:
            return HttpResponseRedirect(reverse('transportation-faads-search'))
        
    # if this is a get w/ a querystring, unpack the form 
    if request.method == 'GET':
        if request.GET.has_key('q'):
            
            order_by = '-obligation_date'
        
            if request.GET.has_key('s'):
                
                if request.GET.has_key('o'):
            
                    if request.GET['o'] == 'desc':
                        order_by = '-'
                        sort_order = 'desc'
                    elif request.GET['o'] == 'asc':
                        order_by = ''
                        sort_order = 'asc'
                
                else:
                    
                    sort_order = 'desc'
                    order_by = '-'
                    
                
                if request.GET['s'] == 'obligation_date':
                    
                    order_by += 'obligation_date'
                    sort_column = 'obligation_date'
                    
                elif request.GET['s'] == 'cfda_program':
                    
                    order_by += 'cfda_program'
                    sort_column = 'cfda_program'
                    
                elif request.GET['s'] == 'recipient':
                    
                    order_by += 'recipient'
                    sort_column = 'recipient'
                    
                elif request.GET['s'] == 'amount':
                    
                    order_by += 'federal_amount'
                    sort_column = 'amount'
                    
                else:
                    
                    order_by = '-obligation_date'
                    
                    sort_column = 'obligation_date'
                    sort_order = 'desc'
                    
                    
            (form, faads_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            
	              
            faads_results = faads_search_query.get_haystack_queryset(order_by)
            
                
            paginator = Paginator(faads_results, RESULTS_PER_PAGE)

            try:
                page = int(request.GET.get('page','1'))
            except Exception, e:
                page = 1
        
            try:
                faads_results_page = paginator.page(page)
            except (EmptyPage, InvalidPage):
                faads_results_page = paginator.page(paginator.num_pages)        
    
            found_some_results = len(faads_results)>0
    
            ran_search = True
            
            # display date range on map
            if form.cleaned_data['obligation_date_start'] is not None or form.cleaned_data['obligation_date_end'] is not None:
                year_range_text = re.sub(r'(\s)0(\d)', r'\1\2', "Cumulative Dollars, %s &ndash; %s" % (form.cleaned_data['obligation_date_start'].strftime("%B %d, %Y"), form.cleaned_data['obligation_date_end'].strftime("%B %d, %Y")) )
            else:
                year_range = faads_search_query.get_year_range()
                year_range_text = "Cumulative Dollar Values, FY%s &ndash; FY%s" % (str(year_range[0]), str(year_range[-1]))

            date_string = faads_search_query
    
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
            found_some_results = False
            formclass = MakeFAADSSearchFormClass(sector=sector, subsectors=subsectors)
            form = formclass()
        

    return render_to_response('faads/search/search.html', {'year_range_text': year_range_text, 'faads_results':faads_results_page, 'sector': sector_name, 'form':form, 'ran_search': ran_search, 'found_some_results': found_some_results, 'query': query, 'sort_column':sort_column, 'sort_order':sort_order, 'page_path': request.path}, context_instance=RequestContext(request))



def annual_chart_data(request, sector_name=None):

    
    if request.method == 'GET':
        if request.GET.has_key('q'):
        
            (form, faads_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            
                   
            faads_results = faads_search_query.aggregate('fiscal_year')
            
            positive_results = {}
            
            for year in faads_results:
                if faads_results[year] > 0:
                    positive_results[year] = faads_results[year]
    
            chart_json = buildChart(positive_results)
            
            return HttpResponse(chart_json, mimetype="text/plain")

    return Http404()


def _get_state_summary_data(results, year_range):
    """ compiles aggregate data for the by-state summary table """
    
    states = {}
    states_order = {}
    
    order_id = 1
    
    for state in State.objects.filter(id__in=results['state'].keys()):
        states[state.id] = state
        states_order[state.id] = order_id
        
        order_id += 1
        

    state_data = []
    
    totals_dict  = {}
    for year in year_range: 
        totals_dict[year] = 0
    
    for (state_id, year_data) in results['state'].items():
        if state_id is None:
            continue
        
        row = [states_order[state_id], states[state_id].name]
        for year in year_range:
            annual_total = year_data.get(year, None)
            row.append(annual_total)
            
            if annual_total:
                totals_dict[year] += annual_total 
            
        state_data.append(row)
    
    totals = []
    
    for year in year_range:
        totals.append(totals_dict[year])

    state_data.sort(key=lambda x: x[0])
    state_data = map(lambda x: x[1:], state_data)
    
    return state_data, totals
    
def _get_program_summary_data(results, year_range):
    """ compiles aggregate data for the by-program summary table """
    
    programs = {}
    for program in ProgramDescription.objects.filter(id__in=results['program'].keys()):
        programs[program.id] = program

        
    program_data = []
    
    totals_dict  = {}
    for year in year_range: 
        totals_dict[year] = 0
    
    for (program_id, year_data) in results['program'].items():
        if program_id is None:
            continue
        row = ["<a href=\"%s\">%s %s</a>" % (reverse('transportation-cfda-programpage', None, (program_id,)), programs[program_id].program_number, programs[program_id].program_title)]
        for year in year_range:
            annual_total = year_data.get(year, None)
            row.append(annual_total)
            
            if annual_total:
                totals_dict[year] += annual_total 
            
        program_data.append(row)
        
    program_data.sort(key=lambda x: x[0])
    
    totals = []
    
    for year in year_range:
        totals.append(totals_dict[year])
    
    return program_data, totals


def summary_statistics_csv(request, sector_name=None, first_column_label='', data_fetcher=''):

    data_fetcher = globals().get(data_fetcher) # we take a string instead of the function itself so that the urlconf can call it directly

    assert len(str(first_column_label))>0 # column must have a label ('state' or 'program')
    assert callable(data_fetcher) # data-fetching function must be passed (returns list of lists containing either state- or program-indexed numbers)

    if request.method == 'GET':
        if request.GET.has_key('q'):
                    
            (form, faads_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            
                   
            results = faads_search_query.get_summary_statistics()
            year_range = faads_search_query.get_year_range()

            data = data_fetcher(results, year_range)
            
            response = HttpResponse(mimetype="text/csv")
            response['Content-Disposition'] = "attachment; filename=%s-%s.csv" % (request.GET['q'], first_column_label.replace(" ", "_").lower())
            writer = csv.writer(response)
            writer.writerow([str(first_column_label)] + year_range)
            for row in data:
                writer.writerow(map(lambda x: strip_tags(x), row))
            response.close()
            
            return response

    return Http404()
    

def summary_statistics(request, sector_name=None):
    # need to translate the state_id back to FIPS codes for the map and normalize by population 
    # grabbing a complete list of state objects and building a table for translation    
    
    
    if request.method == 'GET':
        if request.GET.has_key('q'):
            
            (form, faads_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            
                                      
            results = faads_search_query.get_summary_statistics()
            year_range = faads_search_query.get_year_range()

            state_data, state_totals = _get_state_summary_data(results, year_range)                        
            program_data, program_totals = _get_program_summary_data(results, year_range)
                
            return render_to_response('faads/search/summary_table.html', {'state_data':state_data, 'state_totals':state_totals, 'program_data':program_data, 'program_totals':program_totals, 'year_range':year_range, 'query': request.GET['q']}, context_instance=RequestContext(request))

    return Http404()
    
    
    
def map_data_table(request, sector_name=None):
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
                if states.has_key(state_id) and states[state_id].population and faads_results[state_id] > 0:
                    
                    per_capita_totals[state_id] =  faads_results[state_id] / states[state_id].population
                    
                    if per_capita_totals[state_id] > max_per_capital_total:
                        max_per_capital_total = per_capita_totals[state_id]
                    
                    if faads_results[state_id] > max_state_total:
                        max_state_total = faads_results[state_id]
                    
        
            results = []
            
            for state_id in per_capita_totals:
                if states.has_key(state_id):
                                    
                    line = {'name':states[state_id].name, 'total':faads_results[state_id], 'per_capita':per_capita_totals[state_id]}

                    results.append(line)
                
            
            return render_to_response('faads/search/state_table.html', {'results':results, 'query': request.GET['q']}, context_instance=RequestContext(request))
                
    return Http404()


def map_data_csv(request, sector_name=None):
    

        
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
                if states.has_key(state_id) and states[state_id].population and faads_results[state_id] > 0:
                    
                    per_capita_totals[state_id] =  faads_results[state_id] / states[state_id].population
                    
                    if per_capita_totals[state_id] > max_per_capital_total:
                        max_per_capital_total = per_capita_totals[state_id]
                    
                    if faads_results[state_id] > max_state_total:
                        max_state_total = faads_results[state_id]
                    
        
            results = []
            
            for state_id in per_capita_totals:
                if states.has_key(state_id):
                        
                    
                    line = '%s,%f,%f' % (states[state_id].name, 
                                                           faads_results[state_id], 
                                                           per_capita_totals[state_id])

                    results.append(line)
                
            
            return HttpResponse('\n'.join(results), mimetype="text/csv")
                
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
                if states.has_key(state_id) and states[state_id].population and faads_results[state_id] > 0:
                    
                    per_capita_totals[state_id] =  faads_results[state_id] / states[state_id].population
                    
                    if per_capita_totals[state_id] > max_per_capital_total:
                        max_per_capital_total = per_capita_totals[state_id]
                    
                    if faads_results[state_id] > max_state_total:
                        max_state_total = faads_results[state_id]
                    
        
            results = []
            
            for state_id in per_capita_totals:
                if states.has_key(state_id):
                    
                    state_percent = faads_results[state_id] / max_state_total
                    if state_percent > 0 and state_percent < Decimal('0.001'):
                        state_percent = 0.001
                        
                    state_per_capita_percent = per_capita_totals[state_id] / max_per_capital_total
                    if state_per_capita_percent > 0 and state_per_capita_percent < Decimal('0.001'):
                        state_per_capita_percent = 0.001
                        
                    
                    line = '%d,%f,%.03f,%f,%.03f' % (states[state_id].fips_state_code, 
                                                           faads_results[state_id], 
                                                           state_percent, 
                                                           per_capita_totals[state_id],
                                                           state_per_capita_percent)

                    results.append(line)
                
            
            return HttpResponse('\n'.join(results), mimetype="text/plain")
                
    return Http404()


