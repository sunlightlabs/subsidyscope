# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response, get_object_or_404
from aip.models import *

def index(request):
    ports = None
    grants = None
    error = None
    if request.method == 'GET' and request.GET:
        if request.GET.__contains__('portname') and request.GET['portname'] != '':
            ports = Airport.objects.filter(name__icontains=request.GET['portname'])
            if ports and len(ports) > 1:
                grants = []
                for p in ports:
                    pgrants = GrantRecord.objects.filter(airport=p)
                    money = 0
                    for m in pgrants:
                        money += m.amount
                    grants.append((p, money))
                return render_to_response('aip/index.html', {'ports':ports, 'grants': grants})
            else:
                error = "<span>No airport matched the name provided</span>"
        elif request.GET.__contains__('portcode'):
            ports = Airport.objects.get(code__iexact=request.GET['portcode'])
            if ports:
                grants = []
                pgrants = GrantRecord.objects.filter(airport=ports)
                money = 0
                for m in pgrants:
                    money += m.amount
                grants.append((ports, money))
                return render_to_response('aip/index.html', {'port':ports, 'grants': grants, 'params':[request.GET['portname'], request.GET['portcode']]})
            else:
                error = "<span>No airport matched the code you specified</span>"
        else:
            error = "<span>Must specify and airport name or airport code</span>"
        if error:
            return render_to_response('aip/index.html', {'error': error, 'params': [request.GET['portname'], request.GET['portcode']]})
    else: 
        return render_to_response('aip/index.html', {'error': 'not a get'})
