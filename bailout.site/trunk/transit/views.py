
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

def index(request):
    states = State.objects.all()
    uza = UrbanizedArea.objects.all().order_by('name')
    systems = TransitSystem.objects.all()
    operations = OperationStats.objects.filter(transit_system=systems[0])
    
    tester = None
     
    if request.method =="POST":
        form = TransitQuery(request.POST) 
        if form.is_valid():
            data = form.cleaned_data
            
            name = data['system_name']
            modes = data['modes_selected']
            size = data['size_select']
            state = data['state_select']
            uzas = data['uza_select']
            opm_start = data['ofppm_start']
            opm_end = data['ofppm_end']
            cpm_start = data['cfppm_start']
            cpm_end = data['cfppm_end']
            oupt_start = data['ofpupt_start']
            oupt_end = data['ofpupt_end']
            cupt_start = data['cfpupt_start']
            cupt_end = data['cfpupt_end']

            if name:
                systems = systems.filter(name__icontains=name)
            if modes:
                by_mode = OperationStats.objects.filter(mode__in=modes).values('transit_system').distinct()
                systems = systems.filter(id__in=by_mode)
            if size:
                by_size = None
                if size == 'rural':
                    by_size = UrbanizedArea.objects.filter(population__lte=50000)

                elif size == 'urban':
                    by_size = UrbanizedArea.objects.filter(population__gte=50000)

                if by_size: systems = systems.filter(urbanized_area__in=by_size)
                elif size != "both" and size != "on": systems = None

            if state:
                systems = systems.filter(state=State.objects.get(abbreviation=state))
            
            if uzas:
                systems = systems.filter(urbanized_area=uzas)
                tester = uzas

            if opm_start:
                set = []
                cursor = connection.cursor()
                cursor.execute("SELECT transit_system_id from transit_operationstats group by transit_system_id, mode having SUM(operating_expense)/SUM(passenger_miles_traveled) > %s", [opm_start])
                opm_start_set = cursor.fetchall()
                for x in opm_start_set:
                    set.append(x[0])
                systems = systems.filter(trs_id__in=set)

            if opm_end:
                set = []
                cursor = connection.cursor()
                cursor.execute("SELECT transit_system_id from transit_operationstats group by transit_system_id, mode having SUM(operating_expense)/SUM(passenger_miles_traveled) < %s", [opm_end])
                opm_end_set = cursor.fetchall()
                for x in opm_end_set:
                    set.append(x[0])
                systems = systems.filter(trs_id__in=set)

            if cpm_start:
                set = []
                cursor = connection.cursor()
                cursor.execute("SELECT transit_system_id from transit_operationstats group by transit_system_id, mode having SUM(capital_expense)/SUM(passenger_miles_traveled) > %s", [cpm_start])
                cpm_start_set = cursor.fetchall()
                for x in cpm_start_set:
                    set.append(x[0])
                systems = systems.filter(trs_id__in=set)

            if cpm_end:
                set = []
                cursor = connection.cursor()
                cursor.execute("SELECT transit_system_id from transit_operationstats group by transit_system_id, mode having SUM(capital_expense)/SUM(passenger_miles_traveled) < %s", [cpm_end])
                cpm_end_set = cursor.fetchall()
                for x in cpm_end_set:
                    set.append(x[0])
                systems = systems.filter(trs_id__in=set)

            if oupt_start:
                set = []
                cursor = connection.cursor()
                cursor.execute("SELECT transit_system_id from transit_operationstats group by transit_system_id, mode having SUM(operating_expense)/SUM(unlinked_passenger_trips) > %s", [oupt_start])
                oupt_start_set = cursor.fetchall()
                for x in oupt_start_set:
                    set.append(x[0])
                systems = systems.filter(trs_id__in=set)

            if oupt_end:
                set = []
                cursor = connection.cursor()
                cursor.execute("SELECT transit_system_id from transit_operationstats group by transit_system_id, mode having SUM(operating_expense)/SUM(unlinked_passenger_trips) < %s", [oupt_end])
                oupt_end_set = cursor.fetchall()
                for x in oupt_end_set:
                    set.append(x[0])
                systems = systems.filter(trs_id__in=set)

            if cupt_start:
                set = []
                cursor = connection.cursor()
                cursor.execute("SELECT transit_system_id from transit_operationstats group by transit_system_id, mode having SUM(capital_expense)/SUM(unlinked_passenger_trips) > %s", [cupt_start])
                cupt_start_set = cursor.fetchall()
                for x in cupt_start_set:
                    set.append(x[0])
                systems = systems.filter(trs_id__in=set)

            if cupt_end:
                set = []
                cursor = connection.cursor()
                cursor.execute("SELECT transit_system_id from transit_operationstats group by transit_system_id, mode having SUM(capital_expense)/SUM(unlinked_passenger_trips) < %s", [cupt_end])
                cupt_end_set = cursor.fetchall()
                for x in cupt_end_set:
                    set.append(x[0])
                systems = systems.filter(trs_id__in=set)

            paginator = Paginator(systems, 20)
            try:
                page = int(request.POST.get('page', '1'))

            except ValueError:
                page = 1

            try:
                systems = paginator.page(page)
            except (EmptyPage, InvalidPage):
                systems = paginator.page(paginator.num_pages)
            results = []
            for sys in systems.object_list:
                cursor = connection.cursor()
                cursor.execute("SELECT DISTINCT mode from transit_operationstats where transit_system_id = %s", [sys.id])
                all_modes = cursor.fetchall()
                for mo in all_modes:
                    if modes:
                        if mo[0] in modes:
                            results.append((sys, get_mode(mo[0])))        
                    else:
                        results.append((sys, get_mode(mo[0])))
            tester = paginator.num_pages
            
            return render_to_response('transportation/transit/transit_index.html', {'states': states, 'uza': uza, 'results': results, 'modes': operations[0].MODE_CHOICES ,'paginator': systems, 'num_pages':paginator.num_pages, 'form':data, 'by_mode': tester})
             
        
    return render_to_response('transportation/transit/transit_index.html', {'states': states, 'uza': uza, 'systems': systems, 'modes': operations[0].MODE_CHOICES, 'form': None})


def transitSystem(request, trs_id):
    try:
        transit_system = TransitSystem.objects.get(trs_id=trs_id)
        funding = FundingStats.objects.filter(transit_system=transit_system)
        operations = OperationStats.objects.filter(transit_system=transit_system)
        mode_data = buildModePieChart(transit_system)
        
        #op_data = [] 
        #for o in operations:
        #    op_data.append({"x": int(o.year), "y": float(o.passenger_miles_traveled)})

        fund_json = buildFundingLineChart(funding)
        fund_type_json = buildSourcesPieChart(funding)
        fund_mode = mode_data['expenses']
        upt_data = mode_data['upt_mode']
        pmt_data = mode_data['pmt_mode']

        #op_json = buildLineChart(op_data)

        return render_to_response('transportation/transit/transit_system.html', {'system': transit_system, 'funding': funding, 'operations': operations, 'fund_line_data': dumps(fund_json), 'fund_pie_data': dumps(fund_type_json), 'fund_mode_data': dumps(fund_mode), 'upt_data': dumps(upt_data), 'pmt_data': dumps(pmt_data)})

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
    operating = systemObj.total_expense_ridership_by_mode()
    expenses_json['bg_colour'] = "#FFFFFF"
    expenses_json['elements'] = [{'type':'pie', 'alpha':.8, "start-angle":50, "radius_padding":3, "tip": "$#val#", "colours":["#007EEA", "#00B492", "#4869E1", "#BF5004"], "values":[] }]
    
    #clone json structure for ridership pie
    pmt_json = deepcopy(expenses_json)
    upt_json = deepcopy(expenses_json)

    #add expenses values
    for o in operating:
        expenses_json['elements'][0]['values'].append({"value":float(o[0][1]), "label": o[0][0]+'(#percent#)'})  #add the total expenses for each mode
        pmt_json['elements'][0]['values'].append({"value":float(o[1][2]), "label": o[0][0]+'(#percent#)'}) #add the total ridership (pmt) per mode 
        upt_json['elements'][0]['values'].append({"value":float(o[1][3]), "label": o[0][0]+'(#percent#)'})  #add the total upt per mode
        
    return {'expenses':expenses_json, 'pmt_mode': pmt_json, 'upt_mode':upt_json }

def buildPMTLineChart(operatingObj):
    #a quicky line chart for the pew meeting
    pmt_line_json["bg_colour"] = "#FFFFFF" 
    pmt_line_json['elements'] = [{"type": "line", "values": fund_data, "width": 4, "text":"Total Funding", "dot-style":{"type": "dot", "tip":"Total PMT:$#val#"} }]
    pmt_line_values = []

    #for o in operatingObj:
        

    pmt_line_json["elements"].append({"type":"line", "colour": "#BF5004", "values": fund_capital_data, "text":"Total Capital Funding",  "dot-style":{"type":"dot", "tip":"Total Capital Funding: $#val#"}})



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
     
