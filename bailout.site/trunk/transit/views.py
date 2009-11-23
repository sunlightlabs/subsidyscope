
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext, loader, Template, Context
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Avg, Sum
from transit.models import *
from geo.models import *
from simplejson import * 
from math import *
from django import forms

def index(request):
    states = State.objects.all()
    uza = UrbanizedArea.objects.all().order_by('name')
    systems = TransitSystem.objects.all()
    
    if request.GET:
        
        context = request.GET.values()

        if request.GET.__contains__('system_name') and request.GET['system_name'] != '':  
              
            context[1] = ""  # set the state and uza parameters to null,
            context[2] = ""  # so it doesn't indicate that those are filters

            return render_to_response('transportation/transit/transit_index.html', {'context': context, 'states': states, 'uza': uza, 'systems':systems, 'results': TransitSystem.objects.filter(name__icontains=request.GET['system_name'])})

        elif request.GET.__contains__('state') and request.GET['state'] != "":

            return render_to_response('transportation/transit/transit_index.html', {'context':context, 'states': states, 'uza': uza, 'systems':systems, 'results': TransitSystem.objects.filter(state=State.objects.get(abbreviation__iexact=request.GET['state']))})

        elif request.GET.__contains__('uza') and request.GET['uza'] != "":

            return render_to_response('transportation/transit/transit_index.html', {'context': context, 'states': states, 'uza': uza, 'systems':systems, 'results': TransitSystem.objects.filter(urbanized_area=UrbanizedArea.objects.get(fta_id=request.GET['uza']))})
    
    
    return render_to_response('transportation/transit/transit_index.html', {'states': states, 'uza': uza, 'systems': systems})


def transitSystem(request, trs_id):
    try:
        transit_system = TransitSystem.objects.get(trs_id=trs_id)
        funding = FundingStats.objects.filter(transit_system=transit_system)
        operations = OperationStats.objects.filter(transit_system=transit_system)
        
        mode_data = transit_system.total_expense_ridership_by_mode()
        #op_data = [] 
        #for o in operations:
        #    op_data.append({"x": int(o.year), "y": float(o.passenger_miles_traveled)})

        fund_json = buildFundingLineChart(funding)
        fund_type_json = buildSourcesPieChart(funding)


        #op_json = buildLineChart(op_data)

        return render_to_response('transportation/transit/transit_system.html', {'system': transit_system, 'funding': funding, 'operations': operations, 'mode_data': mode_data, 'fund_line_data': dumps(fund_json), 'fund_pie_data': dumps(fund_type_json)})

    except TransitSystem.DoesNotExist:
        return HttpResponseRedirect('/transportation/transit/') 

def urbanArea(request, uza_id):
    try:
        urban_area = UrbanizedArea.objects.get(fips_id=uza_id)
        
        return render_to_response('/transit/uza.html', {'uza': urban_area})
    except UrbanizedArea.DoesNotExist:
        return HttpResponseRedirect('/transportation/transit/')

def buildModePieChart(operatingObj):
    json = {}


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
    json['elements'] = [{"type": "line", "values": fund_data, "width": 4, "text":"Total Funding", "dot-style":{"type": "dot", "tip":"Total Funding:$#val#"} }]
    if fund_capital_data and max(fund_capital_data) > 0:
        json["elements"].append({"type":"line", "colour": "#BF5004", "values": fund_capital_data, "text":"Total Capital Funding",  "dot-style":{"type":"dot", "tip":"Total Capital Funding: $#val#"}})
    if fund_oper_data and max(fund_oper_data) > 0:
        json["elements"].append({"type":"line", "colour": "#008B62", "values": fund_oper_data, "text":"Total Operating Funding",  "dot-style":{"type":"dot", "tip":"Total Operating Funding: $#val#"}})

    json["y_axis"] = {"min": 0, "max": num}
    json["x_axis"] = {"labels": {"labels":fund_labels}}

    return json
     
