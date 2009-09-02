# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response, get_object_or_404
from aip.models import *

def index(request):
    ports = None
    grants = None
    error = None
    type = None
    blockgs = 0
    if request.method == 'GET' and request.GET:
        if request.GET.__contains__('portname') and request.GET['portname'] != '':
            ports = Airport.objects.filter(name__icontains=(request.GET['portname'].strip(' ')))
            type="name"
        elif request.GET.__contains__('state'):
            ports = Airport.objects.filter(state__iexact=request.GET['state'])
            type = "state"
            bgrants = BlockGrant.objects.filter(state__iexact=request.GET['state'])
            for b in bgrants:
                blockgs += b.amount
        if ports and len(ports) >= 1:
            grants = []
            total = 0
            for p in ports:
                pgrants = GrantRecord.objects.filter(airport=p)
                sgrants = StateGrant.objects.filter(airport=p)
                money = 0
                for m in pgrants:
                    money += m.amount
                total += money
                grants.append((p, money))
            total += blockgs
            return render_to_response('aip/index.html', {'ports':ports, 'grants': grants, 'total': total, 'type': type, 'blockgrants': blockgs})
        elif request.GET.__contains__('portcode'):
            try:
                ports = Airport.objects.get(code__iexact=request.GET['portcode'])
                if ports:
                    grants = []
                    pgrants = GrantRecord.objects.filter(airport=ports)
                    money = 0
                    for m in pgrants:
                        money += m.amount
                    grants.append((ports, money))
                    return render_to_response('aip/index.html', {'port':ports, 'grants': grants, 'params':[request.GET['portname'], request.GET['portcode']]})
            except Airport.DoesNotExist:
                error = "No airport matched the code you specified"

        else:
            error = "Must specify and airport name or airport code"
        if error:
            return render_to_response('aip/index.html', {'error': error, 'params': [request.GET['portname'], request.GET['portcode']]})
    else: 
        return render_to_response('aip/index.html')

def portdetail(request):
    if request.GET.__contains__('code'):
        port = Airport.objects.get(code__iexact=request.GET['code'])
        if port:
            portgrants = GrantRecord.objects.filter(airport=port)   
            enplanements = Enplanements.objects.filter(airport=port)
            data = []
            total =[]
            counter = 0
            grants = 0
            enps = 0
            for e in enplanements:
                for p in portgrants.filter(fiscal_year=e.year): 
                    if len(total) >counter:
                        total[counter] = total[counter] + p.amount
                    else: total.append(p.amount)
                    grants += p.amount
                if len(total) > counter:
                    if e.amount > 0:
                        total[counter] = total[counter] / e.amount
                else: total.append(0)
                enps += e.amount
                data.append((e, total[counter]))
                counter += 1
            if enps > 0:grants = grants/enps
            else: grants = "N/A"
        return render_to_response('aip/detail.html', {"grants":portgrants, "port": port, "data": data, "avg":grants})
