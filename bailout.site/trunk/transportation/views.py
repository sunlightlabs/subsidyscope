from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from cfda.models import ProgramDescription
from tagging.models import Tag
from sectors.models import Sector
from faads.search import *

def getProgram(request, cfda_id):

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
        chartdata = '{"elements":[{ "type": "bar_3d", "on-show": {"type:":"grow-up"}, "values": ['
        xaxis = '"x_axis": {"tick-height": 20, "labels": {"labels":['
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
        if min > 1000:
            min = min - (min % 1000)
        if max > 1000:
            max = max - (max % 1000)
        chartdata += ']}], "title": {"text": ""}, "bg_colour": "#FFFFFF", '+ xaxis + ', "y_axis": {"min": %s, "max": %s}, "x_legend": {"text": "Years", "style": "{font-size:12px;}"}, "y_legend":{"text": "US Dollars ($)", "style":"{font-size:12px;}"}}' % (min, max)   
    else: 
        chartdata = ""
    return render_to_response('transportation/programs.html', {'program': program, 'primarytag': tag, 'objectives': objectives, 'objectives2': objectives2, 'accomps': accomps, 'accomps2': accomps2, 'chartdata':chartdata})

def getProgramIndex(request):
    tags = Tag.objects.all()
    sector = Sector.objects.get(id=2)
    programs = ProgramDescription.objects.filter(sectors=sector)
    return render_to_response('transportation/cfda_programs.html', {'programs': programs, 'tags': tags}, context_instance=RequestContext(request))



