# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response, get_object_or_404
from aip.models import *
from django.db.models import Avg, Sum
import logging
import logging.handlers

def portdata (request, code):
    airport = None
    total = 0
    count = 0
    try:
        airport = Airport.objects.get(code=code)
    except Airport.DoesNotExist:
        pass
    if airport:
        enplanements = Enplanements.objects.filter(airport=code)
        operations = Operations.objects.filter(airport=code)
        grants = GrantRecord.objects.filter(airport=code)
        projects = Project.objects.filter(airport=code)
        stimulus = projects.filter(stimulus__gt=0)
        avgenps = enplanements.aggregate(Avg('amount'))
        avgops = operations.aggregate(Avg('operations'))
        avggrant = grants.aggregate(Avg('total'))
        totalfunding = grants.aggregate(Sum('total'))
        return render_to_response('aip/airports.html', {'airport': airport,'enplanements': enplanements, 'operations':operations, 'grants':grants, 'projects':projects, 'stimulus': stimulus, 'totalfunding':totalfunding['total__sum'], 'avggrant':avggrant['total__avg'], 'avgops':avgops['operations__avg'], 'avgenps':avgenps['amount__avg']})


def index(request):
    ports = None
    grants = None
    error = None
    type = None
    #blockgs = 0
    if request.method == 'GET' and request.GET:
        if request.GET.__contains__('portname') and request.GET['portname'] != '':
            ports = Airport.objects.filter(name__icontains=(request.GET['portname'].strip(' ')))
            type="name"
        elif request.GET.__contains__('state'):
            stateabbrev = request.GET['state']
            if stateabbrev == 'FSM':
                ports = Airport.objects.filter(state__in=['FM', 'MH', 'PW'])
            else:
                ports = Airport.objects.filter(state__iexact=stateabbrev)
            type = "state"
     #       bgrants = BlockGrant.objects.filter(state__iexact=request.GET['state'])
      #      for b in bgrants:
       #         blockgs += b.amount
        if ports and len(ports) >= 1:
            grants = []
            total = 0
            for p in ports:
                pgrants = GrantRecord.objects.filter(airport=p)
                sgrants = StateGrant.objects.filter(airport=p)
                enps = Enplanements.objects.filter(airport=p)
                money = 0
                enplanements = 0
                for e in enps:
                    enplanements += e.amount
                for m in pgrants:
                    money += m.total
                total += money
                grants.append((p, money, enplanements))
      #      total += blockgs
            return render_to_response('aip/index.html', {'ports':ports, 'grants': grants, 'total': total, 'type': type})
        elif request.GET.__contains__('portcode'):
            try:
                ports = Airport.objects.get(code__iexact=request.GET['portcode'])
                if ports:
                    grants = []
                    pgrants = GrantRecord.objects.filter(airport=ports)
                    enps = Enplanements.objects.filter(airport=ports)
                    money = 0
                    enplanements = 0
                    for m in pgrants:
                        money += m.total
                    for e in enps:
                        enplanements += e.amount
                    grants.append((ports, money, enplanements))
                    return render_to_response('aip/index.html', {'port':ports, 'grants': grants, 'params':[request.GET['portname'], request.GET['portcode']]})
            except Airport.DoesNotExist:
                error = 'No airport matched the parameters you specified'

        else:
            error = 'You must specify and airport name or airport code'
        if error:
            return render_to_response('aip/index.html', {'error': error})
    else: 
        return render_to_response('aip/index.html')

