import unittest
import csv
import fpds.tests
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from fpds.search import *
from faads.widgets import *
from cfda.views import buildChart
import django.test.simple
from django.template import RequestContext
from django.test.utils import setup_test_environment, teardown_test_environment
from django.http import Http404, HttpResponseRedirect, HttpResponse
from fpds.models import ExtentCompetedMapper
import settings




RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_FPDS_SEARCH_RESULTS_PER_PAGE', getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20))


def strip_clean_tags(x):
    
    if x:
        return strip_tags(unicode(x).encode('ascii','ignore'))
    else:
        return ''
    


def MakeFPDSSearchFormClass(sector=None, subsectors=[]):

   # subsectors
    subsector_choices = None
 
    SUBSECTOR_SYNONYMS = {
        'transportation': 'Mode'
    }

    class FPDSSearchForm(forms.Form):

        sector_id_choices = [('', 'All Sectors')] + [(s.id, s.name) 
                                                     for s in Sector.objects.all()
                                                     if s.id != 1] # Hack alert! The Sector model
                                                                   # should really have a fpds flag.
        sector_id = forms.ChoiceField(
            label='Economic Sector',
            choices=sector_id_choices,
            required=False,
            initial=sector.id if sector else '')
            
        # free text query
        text_query = forms.CharField(label='Text Search', required=False, max_length=100)
        text_query_type = forms.TypedChoiceField(label='Text Search Target', widget=forms.RadioSelect, choices=((0, 'Vendor Name'), (1, 'Description of Contract Requirement'), (2, 'Both')), initial=2, coerce=int)

        # recipient types
        # recipient_type_choices = (('nonprofit', 'Nonprofits'), ('education', 'Higher Education'), ('all', 'Either'))
        # recipient_type = forms.TypedChoiceField(label="Include recipients classified as", widget=forms.RadioSelect, choices=recipient_type_choices, initial='all')

        vendor_type = forms.TypedChoiceField(label='Vendor Type', widget=forms.RadioSelect, choices=((0, 'Nonprofits'), (1, 'Educational Institutions'), (2, 'Any')), initial=2, coerce=int)

        extent_competed_choices = []
        for (code, name, description, include) in ExtentCompetedMapper.CODES:
            if include:
                extent_competed_choices.append( (code, name) )                
        extent_competed = forms.MultipleChoiceField(label='Extent Competed', required=False, choices=extent_competed_choices, initial=map(lambda x: x[0], extent_competed_choices), widget=CheckboxSelectMultipleMulticolumn(columns=2))

        obligation_date_start = forms.DateField(label="Effective Date Start", required=False)
        obligation_date_end = forms.DateField(label="Effective Date End", required=False)

        obligation_amount_minimum = USDecimalHumanizedField(label="Obligated Amount Minimum", required=False, decimal_places=2, max_digits=12)
        obligation_amount_maximum = USDecimalHumanizedField(label="Obligated Amount Maximum", required=False, decimal_places=2, max_digits=12)

        state_choices = map(lambda x: (x.id, x.name), State.objects.all())
        location_type = forms.TypedChoiceField(label='Location Type', widget=forms.RadioSelect, choices=((0, 'Recipient Location'), (1, 'Principal Place of Performance'), (2, 'Both')), initial=1, coerce=int)
        location_choices = forms.MultipleChoiceField(label='State', required=False, choices=state_choices, initial=map(lambda x: x[0], state_choices), widget=CheckboxSelectMultipleMulticolumn(columns=4))

        sector_name = forms.CharField(label='Sector', required=False, initial=((sector is not None) and sector.name.lower() or ''), max_length=100, widget=forms.HiddenInput)


    return FPDSSearchForm

def construct_form_and_query_from_querydict(sector_name, querydict_as_compressed_string):
    """ Returns a form object and a FPDSSearch object that have been constructed from a search key (a compressed POST querydict) """

    # retrieve the sector and create an appropriate form object to handle validation of the querydict
    querydict = decompress_querydict(querydict_as_compressed_string)
    sector = get_sector_from_querydict(querydict) or get_sector_by_name(sector_name)

    formclass = MakeFPDSSearchFormClass(sector=sector)            
    form = formclass(querydict)

    # validate querydict -- no monkey business!
    if form.is_valid():

        fpds_search_query = fpds.search.FPDSSearch()
        if sector is not None:
            fpds_search_query = fpds_search_query.set_sectors(sector)

        # handle text search
        if form.cleaned_data['text_query'] is not None and len(form.cleaned_data['text_query'].strip())>0:
            if form.cleaned_data['text_query_type']==2:
                fpds_search_query = fpds_search_query.filter('all_text', form.cleaned_data['text_query'])
            elif form.cleaned_data['text_query_type']==1:
                fpds_search_query = fpds_search_query.filter('text', form.cleaned_data['text_query'])
            elif form.cleaned_data['text_query_type']==0:
                fpds_search_query = fpds_search_query.filter('recipient', form.cleaned_data['text_query'])
       
        # handle vendor type
        if form.cleaned_data['vendor_type'] is not None:           
            if form.cleaned_data['vendor_type']==0: # 0 = nonprofits only
                fpds_search_query = fpds_search_query.filter('nonprofit_organization_flag', 1).filter('educational_institution_flag', 0)
            elif form.cleaned_data['vendor_type']==1: # 1 = educational orgs only
                fpds_search_query = fpds_search_query.filter('nonprofit_organization_flag', 0).filter('educational_institution_flag', 1)

        # handle extent competed
        if form.cleaned_data['extent_competed'] is not None:
            fpds_search_query = fpds_search_query.filter('extent_competed', form.cleaned_data['extent_competed'])

        # handle obligation date range
        if form.cleaned_data['obligation_date_start'] is not None or form.cleaned_data['obligation_date_end'] is not None:
            fpds_search_query = fpds_search_query.filter('obligation_action_date', (form.cleaned_data['obligation_date_start'], form.cleaned_data['obligation_date_end']))

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

            fpds_search_query = fpds_search_query.filter('obligated_amount', (obligation_minimum, obligation_maximum))

        # handle location
        if len(form.cleaned_data['location_choices'])<State.objects.all().count():
            if form.cleaned_data['location_type']==0:                
                fpds_search_query = fpds_search_query.filter('recipient_state', form.cleaned_data['location_choices'])
            elif form.cleaned_data['location_type']==1:
                fpds_search_query = fpds_search_query.filter('principal_place_state', form.cleaned_data['location_choices'])
            elif form.cleaned_data['location_type']==2:
                fpds_search_query = fpds_search_query.filter('all_states', form.cleaned_data['location_choices'])

        return (form, fpds_search_query)

    else:
        raise(Exception("Data in querydict did not pass form validation"))


def get_sector_from_querydict(querydict):
    sector_id = querydict.get('sector_id', u'')
    if sector_id != u'':
        return get_object_or_404(Sector, pk=sector_id)
    elif querydict.has_key('sector_name'):
        sector_name = querydict.get('sector_name')
        return get_sector_by_name(sector_name)
    else:
        return None


def search(request, sector_name=None):

    # default values, for safety's sake
    form = None
    query = ''
    encoded_querystring = ''
    ran_search = False
    fpds_results_page = None
    found_some_results = False
    page_range = None
    year_range_text = None
    sort_column = 'obligation_date'
    sort_order = 'asc'

    # if this is a POSTback, package the request into a querystring and redirect
    if request.method == 'POST':
        if request.POST.has_key('text_query'):
            sector = get_sector_from_querydict(request.POST)
            formclass = MakeFPDSSearchFormClass(sector=sector)            
            form = formclass(request.POST)

            if form.is_valid():
                url_name_prefix = sector_name or 'all'
                redirect_url = reverse('%s-fpds-search' % url_name_prefix) + ('?q=%s' % compress_querydict(request.POST))
                return HttpResponseRedirect(redirect_url)


        else:
            return HttpResponseRedirect(reverse('%s-fpds-search') % sector_name)


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

                elif request.GET['s'] == 'recipient':

                    order_by += 'vendor_name'
                    sort_column = 'vendor_name'

                elif request.GET['s'] == 'amount':

                    order_by += 'obligated_amount'
                    sort_column = 'amount'

                else:

                    order_by = '-obligation_date'

                    sort = 'obligation_date'
                    sort_order = 'desc'


            (form, fpds_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            


            fpds_results = fpds_search_query.get_haystack_queryset(order_by)


            paginator = Paginator(fpds_results, RESULTS_PER_PAGE)

            try:
                page = int(request.GET.get('page','1'))
            except Exception, e:
                page = 1

            try:
                fpds_results_page = paginator.page(page)
            except (EmptyPage, InvalidPage):
                fpds_results_page = paginator.page(paginator.num_pages)        

            found_some_results = len(fpds_results)>0

            page_range = range(max(1, fpds_results_page.number - 10),
                               min(paginator.num_pages,
                                   fpds_results_page.number + 10))

            ran_search = True

            # display date range on map
            if form.cleaned_data['obligation_date_start'] is not None or form.cleaned_data['obligation_date_end'] is not None:
                year_range_text = re.sub(r'(\s)0(\d)', r'\1\2', "Cumulative Dollars, %s &ndash; %s" % (form.cleaned_data['obligation_date_start'].strftime("%B %d, %Y"), form.cleaned_data['obligation_date_end'].strftime("%B %d, %Y")) )
            else:
                year_range = fpds_search_query.get_year_range()
                year_range_text = "Cumulative Dollar Values, FY%s &ndash; FY%s" % (str(year_range[0]), str(year_range[-1]))

            query = urllib.quote(request.GET['q'])                        


        # we just wandered into the search without a prior submission        
        else:

            sector = get_sector_by_name(sector_name)

            # no subsectors in FPDS (yet) -- ignore for now
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
            fpds_results_page = None
            found_some_results = False
            formclass = MakeFPDSSearchFormClass(sector=sector, subsectors=subsectors)
            form = formclass()


    return render_to_response('fpds/search/search.html', {
                'year_range_text': year_range_text, 
                'fpds_results': fpds_results_page, 
                'page_range': page_range,
                'sector': sector_name, 
                'form': form, 
                'ran_search': ran_search,
                'found_some_results': found_some_results, 
                'query': query, 
                'sort_column': sort_column, 
                'sort_order': sort_order, 
                'page_path': request.path
            }, 
            context_instance=RequestContext(request))



def annual_chart_data(request, sector_name=None):

    if request.method == 'GET':
        if request.GET.has_key('q'):

            (form, fpds_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            

            fpds_results = fpds_search_query.aggregate('fiscal_year')

            positive_results = {}

            for year in fpds_results:
                if fpds_results[year] > 0:
                    positive_results[year] = fpds_results[year]

            chart_json = buildChart(positive_results, data_src="Obligations (from FPDS)")

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

    state_data.sort(key=lambda x: x[0])
    state_data = map(lambda x: x[1:], state_data)

    
    totals = []
    
    for year in year_range:
        totals.append(totals_dict[year])

    return state_data, totals



def summary_statistics_csv(request, sector_name=None, first_column_label='', data_fetcher=''):

    data_fetcher = globals().get(data_fetcher) # we take a string instead of the function itself so that the urlconf can call it directly

    assert len(str(first_column_label))>0 # column must have a label ('state' or 'program')
    assert callable(data_fetcher) # data-fetching function must be passed (returns list of lists containing either state- or program-indexed numbers)

    if request.method == 'GET':
        if request.GET.has_key('q'):

            (form, fpds_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            

            results = fpds_search_query.get_summary_statistics()
            year_range = fpds_search_query.get_year_range()

            data = data_fetcher(results, year_range)

            response = HttpResponse(mimetype="text/csv")
            response['Content-Disposition'] = "attachment; filename=%s-%s.csv" % (request.GET['q'], first_column_label.replace(" ", "_").lower())
            writer = csv.writer(response)
            writer.writerow([str(first_column_label)] + year_range)
            for row in data[0]:
                striped_row = map(lambda x: strip_clean_tags(x), row)
                writer.writerow(striped_row)
            response.close()

            return response

    return Http404()


def summary_statistics(request, sector_name=None):
    # need to translate the state_id back to FIPS codes for the map and normalize by population 
    # grabbing a complete list of state objects and building a table for translation    

    if request.method == 'GET':
        if request.GET.has_key('q'):

            (form, fpds_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            

            results = fpds_search_query.get_summary_statistics()
            year_range = fpds_search_query.get_year_range()
            
            state_data, state_totals = _get_state_summary_data(results, year_range)                        

            return render_to_response('fpds/search/summary_table.html', {'state_data':state_data, 'state_totals':state_totals, 'year_range':year_range, 'query': request.GET['q']}, context_instance=RequestContext(request))

    return Http404()


def map_data_table(request, sector_name=None):



    # need to translate the state_id back to FIPS codes for the map and normalize by population 
    # grabbing a complete list of state objects and building a table for translation
    states = {}

    for state in State.objects.all():

        states[state.id] = state


    if request.method == 'GET':
        if request.GET.has_key('q'):

            (form, fpds_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            

            fpds_results = fpds_search_query.aggregate('recipient_state')

            max_state_total = 0
            max_per_capital_total = 0

            per_capita_totals = {}

            for state_id in fpds_results:
                if states.has_key(state_id) and states[state_id].population and fpds_results[state_id] > 0:

                    per_capita_totals[state_id] =  fpds_results[state_id] / states[state_id].population

                    if per_capita_totals[state_id] > max_per_capital_total:
                        max_per_capital_total = per_capita_totals[state_id]

                    if fpds_results[state_id] > max_state_total:
                        max_state_total = fpds_results[state_id]


            results = []

            for state_id in per_capita_totals:
                if states.has_key(state_id):

                    line = {'name':states[state_id].name, 'total':fpds_results[state_id], 'per_capita':per_capita_totals[state_id]}

                    results.append(line)
                
            
            return render_to_response('fpds/search/state_table.html', {'results':results, 'query': request.GET['q']}, context_instance=RequestContext(request))
          

    return Http404()


def map_data_csv(request, sector_name=None):



    # need to translate the state_id back to FIPS codes for the map and normalize by population 
    # grabbing a complete list of state objects and building a table for translation
    states = {}

    for state in State.objects.all():

        states[state.id] = state


    if request.method == 'GET':
        if request.GET.has_key('q'):

            (form, fpds_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            

            fpds_results = fpds_search_query.aggregate('recipient_state')

            max_state_total = 0
            max_per_capital_total = 0

            per_capita_totals = {}


            for state_id in fpds_results:
                if states.has_key(state_id) and states[state_id].population and fpds_results[state_id] > 0:

                    per_capita_totals[state_id] =  fpds_results[state_id] / states[state_id].population

                    if per_capita_totals[state_id] > max_per_capital_total:
                        max_per_capital_total = per_capita_totals[state_id]

                    if fpds_results[state_id] > max_state_total:
                        max_state_total = fpds_results[state_id]


            results = []

            for state_id in per_capita_totals:
                if states.has_key(state_id):
                    
                    line = '%s,%f,%f' % (states[state_id].name, 
                                                           fpds_results[state_id], 
                                                           per_capita_totals[state_id])
                    
                    results.append(line)
                
            
            resp = HttpResponse('\n'.join(results), mimetype="text/csv")
            resp['Content-Disposition'] = "attachment; filename=%s.csv" % ('contracts-by-location')
            return resp
    
    return Http404()


def map_data(request, sector_name=None):



    # need to translate the state_id back to FIPS codes for the map and normalize by population 
    # grabbing a complete list of state objects and building a table for translation
    states = {}

    for state in State.objects.all():

        states[state.id] = state


    if request.method == 'GET':
        if request.GET.has_key('q'):

            (form, fpds_search_query) = construct_form_and_query_from_querydict(sector_name, request.GET['q'])            

            fpds_results = fpds_search_query.aggregate('recipient_state')

            max_state_total = 0
            max_per_capital_total = 0

            per_capita_totals = {}

            for state_id in fpds_results:
                if states.has_key(state_id) and states[state_id].population and fpds_results[state_id] > 0:

                    per_capita_totals[state_id] =  fpds_results[state_id] / states[state_id].population

                    if per_capita_totals[state_id] > max_per_capital_total:
                        max_per_capital_total = per_capita_totals[state_id]

                    if fpds_results[state_id] > max_state_total:
                        max_state_total = fpds_results[state_id]


            results = []

            for state_id in per_capita_totals:
                if states.has_key(state_id):

                    state_percent = fpds_results[state_id] / max_state_total
                    if state_percent > 0 and state_percent < Decimal('0.001'):
                        state_percent = 0.001

                    state_per_capita_percent = per_capita_totals[state_id] / max_per_capital_total
                    if state_per_capita_percent > 0 and state_per_capita_percent < Decimal('0.001'):
                        state_per_capita_percent = 0.001


                    line = '%d,%f,%.03f,%f,%.03f' % (states[state_id].fips_state_code, 
                                                           fpds_results[state_id], 
                                                           state_percent, 
                                                           per_capita_totals[state_id],
                                                           state_per_capita_percent)

                    results.append(line)


            return HttpResponse('\n'.join(results), mimetype="text/plain")

    return Http404()
        
        
        
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
    
    






