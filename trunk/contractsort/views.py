from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from sectors.models import Sector
from agency.models import Agency
from fpds.models import NAICSCode, ProductOrServiceCode, FPDSRecord
from django.http import HttpResponse
from django.template import Template, Context
from django.db import connection

#@login_required
def main(request):
    sectors = Sector.objects.all()
    return render_to_response('contractsort/main.html', {'sectors': sectors})


#@login_required
def sector(request, sector_id):
    sector = Sector.objects.get(pk=int(sector_id))
    sector_naics = NAICSCode.objects.filter(sectors=sector)
    sector_psc = ProductOrServiceCode.objects.filter(sectors=sector)
    agencies = Agency.objects.all()
    selected = sector.related_agencies.all()
    agency_codes = []
    agency_id = []
    for s in selected:
        agency_codes.append(s.fips_code)
        agency_id.append(str(s.id))
    import logging
    if agency_id:
        q = "SELECT principal_naicscode_id, SUM(obligated_amount) as total from fpds_fpdsrecord where maj_agency_cat IN (%s) group by principal_naicscode_id" % ",".join(agency_codes)
        logging.debug(q)
        curs = connection.cursor()
        curs.execute(q)
        naics = curs.fetchall()
        logging.debug(naics)
        naics_list = []
        for n in naics:
            try:
                obj = NAICSCode.objects.get(code=n[0])
                code = n[0]
                name = obj.name
                total = n[1]
                parent_desc = "%s - %s" % (obj.parent_code.code, obj.parent_code.name)
                naics_list.append((code, name, total, parent_desc))
            except Exception as e:
                logging.debug(e)
                pass
        
        q = "SELECT product_or_service_code_id, SUM(obligated_amount) as total from fpds_fpdsrecord where maj_agency_cat IN (%s) GROUP BY product_or_service_code_id" % ",".join(agency_codes)
        logging.debug(q)
        curs.execute(q)
        psc = curs.fetchall()
        logging.debug(psc)
        psc_list = []
        for p in psc:
            try:
                obj = ProductOrServiceCode.objects.get(code=p[0])
                code = p[0]
                name = obj.name
                total = p[1]
                psc_list.append((code, name, total))
            except Exception as e:
                logging.debug(e)
    else:
        naics_list = None
        psc_list = None
#    naicscode_ids = FPDSRecord.objects.filter(agency_id__in=selected).values_list('principal_naicscode').distinct()
 #   logging.debug(naicscode_ids)
  #  naicscodes = NAICSCode.objects.filter(code__in=naicscode_ids)


    return render_to_response('contractsort/sector.html', {'sector': sector, 'agencies': agencies, 'selected': selected, 'naics': naics_list, 'psc': psc_list, 'sector_naics': sector_naics, 'sector_psc': sector_psc, 'size': sector_naics.count() + sector_psc.count()})


#@login_required
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



