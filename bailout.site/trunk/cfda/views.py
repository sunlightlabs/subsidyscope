# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from cfda.models import *
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
    cfdaseries = {}
    budgetseries = {}
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
                        budgetseries[year] = yearitem[0].annual_amount
                    else: 
                        budgetseries[year] = None
                    
                except ProgramBudgetAnnualEstimate.DoesNotExist:
                    
                    budgetseries[year] = None
                    
                    if count !=length:
                        estimates += ','
                        
                        
            if data.has_key(year):
                cfdaseries[year] = data[year]
            else:
                cfdaseries[year] = None
                            
            labels.append(year)
            
    return {'labels': labels, 'cfdaseries':cfdaseries, 'budgetseries':budgetseries, 'estimateDescription': prog_desc}


def buildChart(cfdaseries, budgetseries=None, labels=None, prog_desc=None):
    
    years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009]
    
    if labels: labels = ["%s" %d  for d in labels]

    temp = []
    labels = []
    
    for y in years:
        
        if cfdaseries.has_key(y) and cfdaseries[y] != None:
            temp.append(int(cfdaseries[y]))
        else:
            temp.append(None)
        labels.append(str(y))

    cfdaseries = temp
    
    
    

    if budgetseries:
    
        temp = []
        
        for y in years:
            
            if budgetseries.has_key(y) and budgetseries[y] != None:
                temp.append(int(budgetseries[y]))
            else:
                temp.append(None)
            labels.append(str(y))
            
        budgetseries = temp
    
    
    cfdamax=0
    budgetmax=0
    json= {"elements":[]}
    
    if cfdaseries:
        
        json["elements"].append({"type": "bar_3d", "tip":"Obligations (from FAADS): $#val#", "text":"Obligations (from FAADS)", "values": cfdaseries})
        cfdamax = max(cfdaseries)
        
    if budgetseries:
        
        data_description = prog_desc.get_data_type_display()
        
        if prog_desc.data_source:
            data_description += ' (from %s)' % (prog_desc.get_data_source_display())
        
        json["elements"].append({"type":"bar_3d","tip": data_description + ": $#val#", "colour": "#088f1b", "text": data_description, "values":budgetseries})
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
    
    return dumps(json) 

def ajaxChart(request, cfda_id):
    program = ProgramDescription.objects.get(id=int(cfda_id))
    data = getDataSeries(cfda_id)
    jsonstring = buildChart(data['cfdaseries'], data['budgetseries'], data['labels'], data['estimateDescription'])
    t = Template("{%autoescape off%}{{jsonstring}}{%endautoescape%}")
    c = Context({"jsonstring":jsonstring})
    html = t.render(c)
    return HttpResponse(html)

def getProgramByCFDANumber(request, cfda_program_number, sector_name):
    program = get_object_or_404(ProgramDescription, program_number=cfda_program_number)
    return getProgram(request, program.id, sector_name)
        

def getProgram(request, cfda_id, sector_name):
    program = ProgramDescription.objects.select_related().get(id=int(cfda_id))
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
    
    return render_to_response('cfda/programs.html', {'program': program, 'objectives': objectives, 'objectives2': objectives2, 'accomps': accomps, 'accomps2': accomps2, 'sector_name': sector_name, 'navname': "includes/"+sector_name+"_nav.html", 'citation': citation, 'url': url})

def getProgramIndex(request, sector_name):
    tags = CFDATag.objects.all()
    try:
        filter = CFDATag.objects.get(id=int(request.GET['tag']))
    except KeyError: 
        filter = None
    sector = Sector.objects.get(name__iexact=sector_name)
    subsectors = Subsector.objects.filter(parent_sector=sector)
    programs = ProgramDescription.objects.filter(sectors=sector)
    return render_to_response('cfda/cfda_programs.html', {'programs': programs, 'filter':filter, 'tags': tags, 'subsectors': subsectors, 'sector_name': sector_name, 'navname': "includes/"+sector_name+"_nav.html"}, context_instance=RequestContext(request), )

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
