from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from sectors.models import Sector
from agency.models import Agency

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
