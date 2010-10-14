
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Avg, Sum
from django.db.models.query import QuerySet
from django.db import connection 
from transit.models import *
from geo.models import *
from simplejson import * 
from math import *
import csv
from django import forms
from copy import deepcopy
from django.db.models import Q
from haystack.query import SearchQuerySet

metrics_selected = ['cap_expense', 'op_expense', 'PMT', 'UPT', 'recovery_ratio', 'op_expense_pmt', 'cap_expense_pmt', 'op_expense_upt', 'cap_expense_upt'] 

mode_hash = {'AG':'Automated Guideway', 'AR': 'Alaska Railroad', 'MB':'Bus', 'CC':'Cable Car', 'CR':'Commuter Rail', 'DR':'Demand Response', 'FB':'Ferry Boat', 'HR':'Heavy Rail', 'IP':'Inclined Plane', 'JT':'Jitney', 'LR':'Light Rail', 'MO':'Monorail', 'PB':'Publico', 'TB':'Trolley Bus', 'TR':'Aerial Tramway', 'VP':'Vanpool'}

#view functions

def index(request):

    states = State.objects.all()
    uza = UrbanizedArea.objects.all().order_by('name')
    systems, data, name, modes, size, metrics, sort, order = get_search_results(request)
    if systems:
        paginator = Paginator(systems, 20)
        try:
            page = int(request.POST.get('page', '1'))

        except ValueError:
            page = 1

        try:
            systems = paginator.page(page)
        except (EmptyPage, InvalidPage):
            systems = paginator.page(paginator.num_pages)
        
        if len(systems.object_list) > 0: 
            return render_to_response('transportation/transit/transit_index.html', 
                                        {'states': states, 
                                        'uza': uza, 
                                        'results': systems, 
                                        'modes': mode_constants ,
                                        'paginator': systems, 
                                        'num_pages':paginator.num_pages, 
                                        'form':data, 
                                        'metrics': metrics_selected,
                                        'has_searched': True })   

    return render_to_response('transportation/transit/transit_index.html', 
                             {'states': states, 
                              'uza': uza, 
                              'modes': mode_constants, 
                              'has_searched': False,
                              })

def get_system_ridership_csv(request, trs_id):
    system = TransitSystem.objects.get(trs_id=trs_id)
    operations = OperationStats.objects.filter(transit_system=system).order_by('mode')
    response = HttpResponse(mimetype="text/csv")
    response['Content-Disposition'] = 'attachment; filename=%s_ridership_stats.csv' % system.name.replace(' ', '_')
    writer = csv.writer(response)
    writer.writerow([  'mode', 'year', 'passenger miles travelled', 'unlinked passenger trips', 'vehicle revenue miles', 'vehicle revenue hours', 'directional route miles', 'fares', 'operating expense'])
    for o in operations:
        writer.writerow((o.get_mode_display(), o.year, o.passenger_miles_traveled, o.unlinked_passenger_trips, o.vehicle_revenue_miles, o.vehicle_revenue_hours, o.directional_route_miles, o.fares, o.operating_expense ))

    response.close()
    return response

def get_csv_from_search(request):

    systems, data, name, modes, size, metrics, sort, order = get_search_results(request)
    response = HttpResponse(mimetype="text/csv")
    response['Content-Disposition'] = 'attachment; filename=transit_search_results.csv'
    writer = csv.writer(response)
    #headers
    writer.writerow([   "System Name", "Mode", "City", "State", "Urbanized Area",
                        "Avg Capital Expenses", "Avg Operating Expenses", "Passenger Miles Travelled (PMT)",
                        "Unlinked Passenger Trips (UPT)", "Recovery Ratio", "Operating Expense per PMT", 
                        "Capital Expense per PMT", "Operating Expense per UPT", "Capital Expense per UPT"
                    ])
    #write the data out
    for sys in systems:
        writer.writerow([   sys.name, sys.mode, sys.city, sys.state.name, 
                            sys.urbanized_area.name, sys.avg_capital_expenses,
                            sys.avg_operating_expenses, sys.total_PMT, sys.total_UPT,
                            sys.recovery_ratio, sys.avg_operating_PMT, sys.avg_capital_PMT,
                            sys.avg_operating_UPT, sys.avg_capital_UPT
                       ])

    response.close()
    return response

    
    
        
def get_search_results(request):

    states = State.objects.all()
    uza = UrbanizedArea.objects.all().order_by('name')
    systems = TransitSystemMode.objects.all()
    operations = OperationStats.objects.filter(transit_system=systems[0])

    if request.method =="POST":
        form = TransitQuery(request.POST) 
        if form.is_valid():
            data = form.cleaned_data
            name = data['system_name']
            modes = data['modes_selected']
            size = data['size_select']
            state = data['state_select']
            uzas = data['uza_select']
            metrics = data['metrics_selected']
            sort = data["sort"]
            order = data["order"]

            if name:
                #added a more sophisticated solr search query on the free text field
                systems = systems.filter(transit_system__in=[x.pk for x in SearchQuerySet().models(TransitSystem).filter(content=name)] )
                
                #systems = systems.filter(Q(name__icontains=name) | Q(common_name__icontains=name))
            if modes:
                systems = systems.filter(mode__in=modes)
            if size:
                by_size = None
                if size == '50_100':
                    by_size = UrbanizedArea.objects.filter(population__lte=100000)

                elif size == '100_1mil':
                    by_size = UrbanizedArea.objects.filter(population__gte=100000, population__lte=1000000)
                elif size == '1_10mil':
                    by_size = UrbanizedArea.objects.filter(population__gte=1000000, population__lte=10000000)
                elif size == '10_20mil':
                    by_size = UrbanizedArea.objects.filter(population__gte=10000000)

                if by_size: systems = systems.filter(urbanized_area__in=by_size); 

            if state:
                systems = systems.filter(state=State.objects.get(abbreviation=state))
            
            if uzas:
                systems = systems.filter(urbanized_area=uzas)


            if sort and order=="desc":
                tester = order + ' in order'
                systems = systems.order_by('-'+sort)

            elif (sort and order=="asc") or sort:
                systems = systems.order_by(sort)
                tester = sort 
            
            else:
                systems = systems.order_by('name')

            return [ systems, data, name, modes, size, metrics, sort, order ]

    return [None, None, None, None, None, None, None, None]
            #else: tester = "no objects returned" 
                 
def transitSystem(request, trs_id):
    
    try:
        #Get general data for this system
        transit_system = TransitSystem.objects.get(trs_id=trs_id)
        system_mode = TransitSystemMode.objects.filter(transit_system=transit_system)
        funding = FundingStats.objects.filter(transit_system=transit_system)
        operations = OperationStats.objects.filter(transit_system=transit_system)

        #aggregate all the operation stats for presentation
        mode_operations = operations.values('mode').annotate(op_exp=Avg('operating_expense'), 
                                                             cap_exp=Avg('capital_expense'), 
                                                             vrh=Avg('vehicle_revenue_hours'), 
                                                             vrm=Avg('vehicle_revenue_miles'), 
                                                             pmt=Avg('passenger_miles_traveled'), 
                                                             upt=Avg('unlinked_passenger_trips'))

        #replace mode abbrev with name
        for x in mode_operations: x['mode'] = mode_hash[x['mode']] 

        #Fare data for bar chart

        mode_data = buildModePieChart(transit_system)
        
        #gather data for funding matrix in template
        funding_percent = buildMatrix(trs_id, 2008)
        
        #Get pie chart json data
        fund_json = buildFundingLineChart(funding)
        #reduce funding to most recent year, 2008, for pie charts
        fund_source_capital_json = buildSourcesPieChart(funding.filter(year=2008), 'capital')
        fund_source_operating_json = buildSourcesPieChart(funding.filter(year=2008), 'operating')
        fund_mode = mode_data['expenses']

        upt_data = mode_data['upt_mode']
        pmt_data = mode_data['pmt_mode']

        #year list for reference in template
        year_list = []
        for x in range(1991, 2009): year_list.append(x)

        return render_to_response('transportation/transit/transit_system.html', 
                                 {'system': transit_system, 
                                  'funding': funding, 
                                  'operations': operations, 
                                  'year_list': year_list, 
                                  'matrix_data': funding_percent, 
                                  'mode_operations': mode_operations, 
                                  'fund_line_data': dumps(fund_json), 
                                  'fund_pie_data_capital': dumps(fund_source_capital_json), 
                                  'fund_pie_data_operating': dumps(fund_source_operating_json), 
                                  'mode_hash': mode_hash})

    except TransitSystem.DoesNotExist:
        return HttpResponseRedirect('/transportation/transit/') 



def chartReloader(request, trs_id, category, year):

    system = TransitSystem.objects.get(trs_id=trs_id)
    
    if year != "all":
        funding = FundingStats.objects.filter(transit_system=system, year=year)
    else:
        funding = FundingStats.objects.filter(transit_system=system)

    json = buildSourcesPieChart(funding, category)
    
    return HttpResponse(dumps(json))

def matrixReloader(request, trs_id, year):
    
    system = TransitSystem.objects.get(trs_id=trs_id)

    data = buildMatrix(trs_id, year)

    return render_to_response("transportation/transit/matrix.html", {'system':system, 'matrix_data': data})


#Helper functions for the views

def chartMax(data_max, mod=1000):
    maximum = data_max
    while maximum % mod != maximum:
        mod = mod * 10
        
    maximum = maximum + (mod-(maximum % mod))
    mod = maximum / 5
    ymax = mod
    while data_max > ymax:   # x10 can be a big factor, so we take our neat slices and pare it down
        ymax += mod
    
    return ymax

def buildMatrix(trs_id, year=None):

    transit_system = TransitSystem.objects.get(trs_id=trs_id)
    funding = FundingStats.objects.filter(transit_system=transit_system)
    
    #gather data for funding matrix in template
    funding_percent = []
    fund_types = ('federal', 'state', 'local', 'other')
    same_uza = FundingStats.objects.filter(transit_system__in = TransitSystem.objects.filter(urbanized_area=transit_system.urbanized_area))
#    same_state = FundingStats.objects.filter(transit_system__in = TransitSystem.objects.filter(state=transit_system.state))

    all_fund = FundingStats.objects.all()

    if year and year != "all":
        funding = funding.filter(year=year)
        same_uza = same_uza.filter(year=year)
        all_fund = all_fund.filter(year=year)
    
    fund_subsets = (funding, same_uza, all_fund)

    for f in fund_types:
        temp_list = [f]
            
        for s in fund_subsets:
            temp_list.append(sum(filter(None, s.aggregate(Sum('capital_'+f), Sum('operating_'+f)).values())) or 'n/a')   
             
        funding_percent.append(temp_list)
    
    #if year==None or (year > 2001):
    funding_percent.append(["fares", int(funding.aggregate(Sum('operating_fares'))['operating_fares__sum']) or 'n/a', same_uza.aggregate(Sum('operating_fares'))['operating_fares__sum'] or 'n/a', all_fund.aggregate(Sum('operating_fares'))['operating_fares__sum'] or 'n/a'])
    

    return funding_percent    

def urbanArea(request, uza_id):
    try:
        urban_area = UrbanizedArea.objects.get(fips_id=uza_id)
        
        return render_to_response('/transit/uza.html', {'uza': urban_area})
    except UrbanizedArea.DoesNotExist:
        return HttpResponseRedirect('/transportation/transit/')

def buildModePieChart(systemObj):
    expenses_json = {}
    operating = TransitSystemMode.objects.filter(transit_system=systemObj)
    expenses_json['bg_colour'] = "#FFFFFF"
    expenses_json['elements'] = [{'type':'pie', 
                                  'alpha':.8, 
                                  'start-angle':50, 
                                  'radius_padding':3, 
                                  'tip': '$#val#', 
                                  'colours':["#007EEA", "#00B492", "#4869E1", "#BF5004"],
                                  'values':[] }]
    
    #clone json structure for ridership pie
    pmt_json = deepcopy(expenses_json)
    upt_json = deepcopy(expenses_json)

    #add expenses values
    for o in operating: 
        
        #add the total expenses for each mode
        expenses_json['elements'][0]['values'].append({"value":float(o.total_operating_expenses), "label": o.mode +'(#percent#)'}) 
        
        #add the total ridership (pmt) per mode 
        pmt_json['elements'][0]['values'].append({"value":float("%s" % (o.total_PMT or 0)), "label": o.mode +'(#percent#)'})

        #add the total upt per mode 
        upt_json['elements'][0]['values'].append({"value":float("%s" % (o.total_UPT or 0)), "label": o.mode +'(#percent#)'})  
        
    return {'expenses':expenses_json, 'pmt_mode': pmt_json, 'upt_mode':upt_json }


def buildSourcesPieChart(fundingObj, category=None):
    json = {}

    data = {'Federal':[], 'State':[], 'Local':[], 'Other':[], 'Fares': []}
    
    for f in fundingObj:
        
        for key in data.keys():
            if key == 'Fares' and category != 'capital' and f.operating_fares: data[key].append(int(f.operating_fares))
            else: data[key].append(f.total_funding_by_type(key.lower(), category))

    #set up initial chart elements
    json["bg_colour"] = "#FFFFFF"
    json['elements'] = [{'type': 'pie',
                         'alpha':.8, 
                         'start-angle':50,  
                         'radius_padding': 3, 
                         'tip': '$#val#', 
                         'colours': [ "#007EEA", "#E18859", "#00B492", "#4869E1", "#BF5004"], 
                         'title': { "text": "Funding Breakdown" }, 
                         'values': [] }]
    
    for key in data.keys():
        if key == 'Fares' and category == 'capital': continue
        json['elements'][0]['values'].append({ "value": sum(data[key]) or 0, "label": key + " (#percent#)", "font-size": 10, 'font-weight': 'bold'})

    return json

def buildFundingLineChart(funding):
    json = {}
    fund_labels = []

    data = {'Total': [], 'Federal':[], 'State':[], 'Local':[], 'Other':[], 'Fares': []}
    colors = {'Total': '#3030D0', 'Federal': '#BF5004', 'State': '#008B62', 'Local': '#9197F0','Other': '#ECC6B4', 'Fares':'#00B492'}

    for f in funding:

        for key in data.keys():
            if key == 'Total': data[key].append(int(f.total_funding()))
            
            elif key == 'Fares':
                if f.operating_fares: 
                    data['Fares'].append(int(f.operating_fares))
                else:
                    data['Fares'].append('null')
            else:
                data[key].append( int(f.total_funding_by_type(key.lower()) ))

        fund_labels.append(str(f.year))
    
    #basic chart setup
    json["bg_colour"] = "#FFFFFF" 
    json['elements'] = []
   
    
    for text in data.keys():
        if text == 'Total': width = 4
        else: width = 2

        json['elements'].append({'type': 'line', 
                         'values': data[text], 
                         'width': width, 
                         'colour': colors[text],
                         'text': '%s Funding' % text, 
                         'dot-style':{'type': 'dot','tip':('%s Funding:$#val#' % text)} })

    json["y_axis"] = {"min": 0, "max": chartMax(max(data['Total']))}
    json["x_axis"] = {"labels": {"labels":fund_labels} }

    return json
     
