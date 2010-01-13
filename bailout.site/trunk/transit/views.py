
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext, loader, Template, Context
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Avg, Sum
from django.db import connection 
from transit.models import *
from geo.models import *
from simplejson import * 
from math import *
from django import forms
from copy import deepcopy
from django.db.models import Q

metrics_selected = ['cap_expense', 'op_expense', 'PMT', 'UPT', 'recovery_ratio', 'op_expense_pmt', 'cap_expense_pmt', 'op_expense_upt', 'cap_expense_upt'] 

mode_hash = {'AG':'Automated Guideway', 'AR': 'Alaska Railroad', 'MB':'Bus', 'CC':'Cable Car', 'CR':'Commuter Rail', 'DR':'Demand Response', 'FB':'Ferry Boat', 'HR':'Heavy Rail', 'IP':'Inclined Plane', 'JT':'Jitney', 'LR':'Light Rail', 'MO':'Monorail', 'PB':'Publico', 'TB':'Trolley Bus', 'TR':'Aerial Tramway', 'VP':'Vanpool'}

def index(request):
    states = State.objects.all()
    uza = UrbanizedArea.objects.all().order_by('name')
    systems = TransitSystemMode.objects.all()
    operations = OperationStats.objects.filter(transit_system=systems[0])
    
    tester = None
     
    tester = "test"
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
                systems = systems.filter(Q(name__icontains=name) | Q(common_name__icontains=name))
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
                return render_to_response('transportation/transit/transit_index.html', {'states': states, 'uza': uza, 'results': systems, 'modes': mode_constants ,'paginator': systems, 'num_pages':paginator.num_pages, 'form':data, 'by_mode': tester, 'metrics': metrics_selected})  
            else: tester = "no objects returned" 
                 
    return render_to_response('transportation/transit/transit_index.html', {'states': states, 'uza': uza, 'modes': mode_constants, 'by_mode':tester})


def transitSystem(request, trs_id):
    try:
        transit_system = TransitSystem.objects.get(trs_id=trs_id)
        system_mode = TransitSystemMode.objects.filter(transit_system=transit_system)
        funding = FundingStats.objects.filter(transit_system=transit_system)
        operations = OperationStats.objects.filter(transit_system=transit_system)

        mode_operations = operations.values('mode').annotate(op_exp=Avg('operating_expense'), cap_exp=Avg('capital_expense'), vrh=Avg('vehicle_revenue_hours'), vrm=Avg('vehicle_revenue_miles'), pmt=Avg('passenger_miles_traveled'), upt=Avg('unlinked_passenger_trips'))

        for x in mode_operations: x['mode'] = mode_hash[x['mode']] #replace mode abbrev with name

        fares_data = {}
        fares_data['elements'], fares_data['bg_colour'], fares_data['x_axis'] = [{'type':'bar', "values":[]}], '#FFFFFF', {"labels":{"labels": []}}
        fare_max = 0
                
        for f in system_mode:
            fares_data['x_axis']['labels']['labels'].append(mode_hash[f.mode])
            fares_data['elements'][0]["values"].append(int(f.total_fares)) 

        mod = 1000
        maximum = max(fares_data['elements'][0]['values'])
        while maximum % mod != maximum:
            mod = mod * 10
        
        maximum = maximum + (mod-(maximum % mod))
        mod = maximum / 5
        ymax = mod
        true_max = max(fares_data['elements'][0]['values'] )
        while true_max > ymax:   # x10 can be a big factor, so we take our neat slices and pare it down
            ymax += mod
        fares_data["y_axis"] = {"max": int(ymax), "min": 0}

        mode_data = buildModePieChart(transit_system)
        
        #gather data for funding matrix in template
        funding_percent = []
        fund_types = ('federal', 'state', 'local', 'other')
        same_uza = FundingStats.objects.filter(transit_system__in = TransitSystem.objects.filter(urbanized_area=transit_system.urbanized_area))
        same_state = FundingStats.objects.filter(transit_system__in = TransitSystem.objects.filter(state=transit_system.state))
        fund_subsets = (funding, same_uza, same_state, FundingStats.objects.all())
        for f in fund_types:
            temp_list = [f]
            
            for s in fund_subsets:
                temp_list.append(sum(filter(None, s.aggregate(Sum('capital_'+f), Sum('operating_'+f)).values())) or 'n/a')    

            funding_percent.append(temp_list)
        
        #Get pie chart json data
        fund_json = buildFundingLineChart(funding)
        fund_type_json = buildSourcesPieChart(funding)
        fund_mode = mode_data['expenses']

        upt_data = mode_data['upt_mode']
        pmt_data = mode_data['pmt_mode']

        return render_to_response('transportation/transit/transit_system.html', {'system': transit_system, 'funding': funding, 'operations': operations, 'matrix_data': funding_percent, 'mode_operations': mode_operations, 'fares_data': dumps(fares_data), 'fund_line_data': dumps(fund_json), 'fund_pie_data': dumps(fund_type_json), 'mode_hash': mode_hash})

    except TransitSystem.DoesNotExist:
        return HttpResponseRedirect('/transportation/transit/') 

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
    expenses_json['elements'] = [{'type':'pie', 'alpha':.8, "start-angle":50, "radius_padding":3, "tip": "$#val#", "colours":["#007EEA", "#00B492", "#4869E1", "#BF5004"], "values":[] }]
    
    #clone json structure for ridership pie
    pmt_json = deepcopy(expenses_json)
    upt_json = deepcopy(expenses_json)

    #add expenses values
    for o in operating:
        expenses_json['elements'][0]['values'].append({"value":float(o.total_operating_expenses), "label": o.mode +'(#percent#)'})  #add the total expenses for each mode
        pmt_json['elements'][0]['values'].append({"value":float("%s" % (o.total_PMT or 0)), "label": o.mode +'(#percent#)'}) #add the total ridership (pmt) per mode 
        upt_json['elements'][0]['values'].append({"value":float("%s" % (o.total_UPT or 0)), "label": o.mode +'(#percent#)'})  #add the total upt per mode
        
    return {'expenses':expenses_json, 'pmt_mode': pmt_json, 'upt_mode':upt_json }


def buildSourcesPieChart(fundingObj):
    json = {}
    fed = []
    state = []
    local = []
    other = []
    for f in fundingObj:
        fed.append(f.total_funding_by_type('federal'))
        state.append(f.total_funding_by_type('state'))
        local.append(f.total_funding_by_type('local'))
        other.append(f.total_funding_by_type('other'))

    json["bg_colour"] = "#FFFFFF"
    json['elements'] = [{"type": "pie","alpha":.8, "start-angle":50,  "radius_padding": 3, "tip": "$#val#", "colours": [ "#007EEA", "#00B492", "#4869E1", "#BF5004"], "title": { "text": "Funding Breakdown" }, "values": [] }]
    
    if max(state) > 0:
        json['elements'][0]['values'].append({ "value": sum(state), "label": "State (#percent#)", "font-size": 10, 'font-weight': 'bold'})
    if max(fed) > 0: 
        json['elements'][0]['values'].append({"value": sum(fed), "label": "Federal (#percent#)", "font-size": 10, 'font-weight': 'bold'}) 
    if max(local) > 0:
        json['elements'][0]['values'].append({"value": sum(local), "label": "Local (#percent#)", "font-size":10, 'font-weight': 'bold'})
    if max(other) > 0:
        json['elements'][0]['values'].append({ "value": sum(other), "label": "Other (#percent#)", "font-size":10, 'font-weight':'bold'}) 

    return json

def buildFundingLineChart(funding):
    json = {}
    fund_data = []
    fund_capital_data = []
    fund_oper_data = []
    fund_labels = []
    fund_max = 0

    for f in funding:
        if f.total_funding() > fund_max: fund_max = f.total_funding()
        fund_data.append( f.total_funding())
        fund_capital_data.append( f.total_funding('capital'))
        fund_oper_data.append( f.total_funding('operating'))
        fund_labels.append(str(f.year))
       
    # really hacky way of finding the most appropriate max on the graph 
    digits = len(str(int(fund_max/5)))
    num = str(int(str(fund_max/5)[:2]) + 1)
    for d in range(digits-2): num += '0'
    num = int(num) * 5

    json["bg_colour"] = "#FFFFFF" 
    json['elements'] = [{"type": "line", "values": fund_data, "width": 4, "text":"Total Funding", "dot-style":{"type": "dot","tip":"Total Funding:$#val#"} }]
    if fund_capital_data and max(fund_capital_data) > 0:
        json["elements"].append({"type":"line", "colour": "#BF5004", "values": fund_capital_data, "text":"Total Capital Funding",  "dot-style":{"type":"dot", "tip":"Total Capital Funding: $#val#"}})
    if fund_oper_data and max(fund_oper_data) > 0:
        json["elements"].append({"type":"line", "colour": "#008B62", "values": fund_oper_data, "text":"Total Operating Funding",  "dot-style":{"type":"dot", "tip":"Total Operating Funding: $#val#"}})

    json["y_axis"] = {"min": 0, "max": num}
    json["x_axis"] = {"labels": {"labels":fund_labels} }

    return json
     
