from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from sectors.models import Sector
from agency.models import Agency
from fpds.models import NAICSCode, ProductOrServiceCode
from django.http import HttpResponse
from django.template import Template, Context

@login_required
def main(request):
    sectors = Sector.objects.all()
    return render_to_response('contractsort/main.html', {'sectors': sectors})


@login_required
def sector(request, sector_id):
    sector = Sector.objects.get(pk=int(sector_id))
    agencies = Agency.objects.all()
    selected = sector.related_agencies.all()
    agency_codes = []
    for s in selected:
        agency_codes.append(s.fips_code)

    #naics_codes = NAICSCode.objects.filter

    return render_to_response('contractsort/sector.html', {'sector': sector, 'agencies': agencies, 'selected': selected})


@login_required
def update_agency(request, sector_id):
    if request.method == "POST":
        if request.POST:
            sector = Sector.objects.get(pk=int(sector_id))
            sector.related_agencies.clear()
            selected = []
            for a in request.POST.lists()[0][1]:
                agency = Agency.objects.get(id=int(a))
                selected.append(int(a))
                sector.related_agencies.add(agency)
            return HttpResponse(Template('success!: {{selected}}').render(Context({'selected':selected })))
    return HttpResponse(Template('success').render(Context({})))

def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login_auth(request, user)
            return HttpResponseRedirect('/contractsort/')
        
        else:
            return render_to_response('contractsort/login.html', {'invalid':True})
    else:
        return render_to_response('contractsort/login.html')  


def logout(request):
    
    logout_auth(request)
    return render_to_response('contractsort/login.html')



