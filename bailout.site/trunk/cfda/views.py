# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from cfda.models import ProgramDescription
from tagging.models import Tag
from sectors.models import Sector
from faads.search import *
from faads.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import *

def getProgram(request, cfda_id, sector_name):
    program = ProgramDescription.objects.get(id=int(cfda_id))
    tag = Tag.objects.get(id=program.primary_tag_id)
    objectives = program.objectives
    objectives2 = ''
    accomps = program.program_accomplishments
    accomps2 = ''
    if len(objectives) > 800:
        objectives2 =  objectives[800:]
        objectives = objectives[:800] 
    if len(accomps) > 800:
        accomps2 = accomps[800:]
        accomps = accomps[:800]
    data = FAADSSearch().filter('cfda_program', program.program_number).aggregate('fiscal_year')
    length = len(data)
    if length > 0:
        chartdata = '{"elements":[{"type":"bar_3d", "colour": "#088F1b","text":"CFDA Estimate", "tip": "CFDA #val#", "values":[null, null, null, null, null, 36924964306, 37933741690, 40248148610, 41620631862, 41772990045]}, { "tip": "FAADS #val#","type": "bar_3d", "on-show": {"type:":"grow-up"}, "text": "FAADs Data", "values": ['
        xaxis = '"x_axis": {"3d": 5, "colour": "#909090", "tick-height": 20, "labels": {"labels":['
        count = 1
        min = -1
        max = 10
        years = data.keys()
        years.sort()
        for point in years:
            xaxis += '"%s"' % point
            chartdata += '%s' % data[point]
            if data[point] > max:
                max = data[point]
            if min == -1:
                min = data[point]
            elif data[point] < min:
                min = data[point]
            if count != length:
                xaxis +=', '
                chartdata += ', '
            count += 1
        xaxis += ']}}'
        modnum = min 
        if max > 1000:
            modnum = 1000;
        if max > 100000:
            modnum = 100000
        if max > 1000000:
            modnum = 1000000
        if max > 10000000:
            modnum = 10000000
        if max > 100000000:
            modnum = 100000000
        if max > 1000000000:
            modnum = 1000000000
        if max > 10000000000:
            modnum = 10000000000
        max = max + (modnum-(max % modnum))
        min = 0
        chartdata += ']}], "title": {"text": ""}, "bg_colour": "#FFFFFF", '+ xaxis + ', "y_axis": {"colour": "#909090", "min": %s, "max": %s}, "x_legend": {"text": "Years", "style": "{font-size:12px;}"}, "y_legend":{"text": "US Dollars ($)", "style":"{font-size:12px;}"}}' % (min, max)   
    else: 
        chartdata = ""
    return render_to_response('cfda/programs.html', {'program': program, 'primarytag': tag, 'objectives': objectives, 'objectives2': objectives2, 'accomps': accomps, 'accomps2': accomps2, 'chartdata':chartdata, 'sector_name': sector_name, 'navname': "includes/"+sector_name+"_nav.html"})

def getProgramIndex(request, sector_name):
    tags = Tag.objects.all()
    sector = Sector.objects.get(name__iexact=sector_name)
    programs = ProgramDescription.objects.filter(sectors=sector)
    return render_to_response('cfda/cfda_programs.html', {'programs': programs, 'tags': tags, 'sector_name': sector_name, 'navname': "includes/"+sector_name+"_nav.html"}, context_instance=RequestContext(request), )

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
