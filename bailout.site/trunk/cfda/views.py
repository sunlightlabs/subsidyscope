# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from cfda.models import *
from tagging.models import Tag
from sectors.models import Sector
from faads.search import *
from faads.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import *
from simplejson import * 

def getDataSeries(cfda_id):
    program = ProgramDescription.objects.get(id=int(cfda_id))
    
    years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009]
    
    data = FAADSSearch().filter('cfda_program', cfda_id).aggregate('fiscal_year')
    labels = []
    cfdaseries = []
    budgetseries = []
    prog_desc = None
    
    try:
        prog_desc = ProgramBudgetEstimateDescription.objects.get(program=program)
        budget_est = ProgramBudgetAnnualEstimate.objects.filter(budget_estimate=prog_desc) 
    except  ProgramBudgetEstimateDescription.DoesNotExist:
        budget_est = None
    
    
    if len(years) > 0:
        
        years.sort()
        
        for year in years:
            if budget_est:
                try:
                    yearitem = budget_est.filter(fiscal_year=year)
                    if yearitem:
                        budgetseries.append(yearitem[0].annual_amount)
                    else: budgetseries.append(-1)
                except ProgramBudgetAnnualEstimate.DoesNotExist:
                    budgetseries.append(-1)
                    if count !=length:
                        estimates += ','
                        
                        
            if data.has_key(year):
                cfdaseries.append(data[year])
            else:
                cfdaseries.append(-1)
                            
            labels.append(year)
            
    return {'labels': labels, 'cfdaseries':cfdaseries, 'budgetseries':budgetseries, 'estimateDescription': prog_desc}


def buildChart(cfdaseries, budgetseries=None, labels=None, prog_desc=None):
    if labels: labels = ["%s" %d  for d in labels]
    if type(cfdaseries).__name__ == 'dict': 
        sortedyears = cfdaseries.keys()
        sortedyears.sort()
        temp = []
        labels = []
        for y in sortedyears:
            temp.append(int(cfdaseries[y]))
            labels.append(str(y))
        cfdaseries = temp
    elif cfdaseries: cfdaseries = [int(d) for d in cfdaseries]
    if budgetseries: budgetseries = [int(d) for d in budgetseries]
    cfdamax=0
    budgetmax=0
    json= {"elements":[]}
    if cfdaseries:
        json["elements"].append({"type": "bar_3d", "tip":"FAADS: $#val#", "text":"FAADS data", "values": cfdaseries})
        cfdamax = max(cfdaseries)
    if budgetseries:
        json["elements"].append({"type":"bar_3d","tip": ProgramBudgetEstimateDescription.DATA_TYPE_CHOICES[prog_desc.data_type][1]+": $#val#", "colour": "#088f1b", "text": ProgramBudgetEstimateDescription.DATA_TYPE_CHOICES[prog_desc.data_type][1], "values":budgetseries})
        budgetmax = max(budgetseries)
    json["title"] = {"text":""}
    json["bg_colour"] = "#FFFFFF"
    json["x_axis"] = {"3d": 5, "colour":"#909090", "tick-height":20, "labels": {"labels":labels}}
    mod = 1000
    maximum = max(cfdamax, budgetmax)
    while maximum % mod != maximum:
        mod = mod * 10
    maximum = maximum + (mod-(maximum % mod))
    json["y_axis"] = {"colour": "#909090", "min": 0, "max": maximum}
    json["x_legend"] = {"text": "Years", "style": "{font-size:12px;}"}
    json["y_legend"] = {"text": "US Dollars($)", "style": "{font-size: 12px;}"}
    
    return dumps(json).replace('-1', 'null')

def getProgram(request, cfda_id, sector_name):
    program = ProgramDescription.objects.get(id=int(cfda_id))
    tag = Tag.objects.get(id=program.primary_tag_id)
    objectives = program.objectives
    objectives2 = ''
    accomps = program.program_accomplishments
    accomps2 = ''
    citation = ''
    url = ''
    if len(objectives) > 800:
        objectives2 =  objectives[800:]
        objectives = objectives[:800] 
    if len(accomps) > 800:
        accomps2 = accomps[800:]
        accomps = accomps[:800]
    
    data = getDataSeries(cfda_id)
    jsonstring = buildChart(data['cfdaseries'], data['budgetseries'], data['labels'], data['estimateDescription'])
    return render_to_response('cfda/programs.html', {'program': program, 'primarytag': tag, 'objectives': objectives, 'objectives2': objectives2, 'accomps': accomps, 'accomps2': accomps2, 'chartdata': jsonstring, 'sector_name': sector_name, 'navname': "includes/"+sector_name+"_nav.html", 'citation': citation, 'url': url})

def getProgramIndex(request, sector_name):
    tags = CFDATag.objects.all()
    sector = Sector.objects.get(name__iexact=sector_name)
    subsectors = Subsector.objects.filter(parent_sector=sector)
    programs = ProgramDescription.objects.filter(sectors=sector)
    return render_to_response('cfda/cfda_programs.html', {'programs': programs, 'tags': tags, 'subsectors': subsectors, 'sector_name': sector_name, 'navname': "includes/"+sector_name+"_nav.html"}, context_instance=RequestContext(request), )

def getFAADSLineItems(request, cfda_id, sector_name):
    program = ProgramDescription.objects.get(id=cfda_id)
    
    try:
        fy = int(request.GET.get('year', date.today().year))
    except ValueError:
        fy = date.today().year 
    faads = Record.objects.filter(cfda_program=program, fiscal_year=fy)
    years = Record.objects.filter(cfda_program=program).values('fiscal_year').distinct()
    yearlist = []
    for y in years:
        yearlist.append(y['fiscal_year'])
    paginator = Paginator(faads, 50)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1 
    try:
        faads = paginator.page(page)
    except (EmptyPage, InvalidPage):
        faads = paginator.page(paginator.num_pages)
    return render_to_response('cfda/faadslineitems.html', {'page': page, 'year': fy, 'program':program, 'faads': faads, 'fy': fy, 'years': yearlist, 'sector_name': sector_name, 'navname':"includes/"+sector_name+"_nav.html"}, context_instance=RequestContext(request))
