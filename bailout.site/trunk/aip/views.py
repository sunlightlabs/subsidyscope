# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext, loader, Template, Context
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from aip.models import *
from django.db.models import Avg, Sum
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import logging
import logging.handlers
import csv

def portdata (request, code):
    airport = None
    total = 0
    count = 0
    service = {'P': 'Primary', 'CS': 'Commercial Service', 'GA':'General Aviation', 'R':'Reliever'}
    try:
        airport = Airport.objects.get(code=code)
    except Airport.DoesNotExist:
        return HttpResponseRedirect('/projects/transportation/aip/')
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
        try:
            service_level = service[airport.service_level]
        except KeyError:
            service_level = 'Unknown'
        return render_to_response('aip/airports.html', {'airport': airport,'enplanements': enplanements, 'operations':operations, 'grants':grants, 'projects':projects, 'stimulus': stimulus, 'totalfunding':totalfunding['total__sum'], 'avggrant':avggrant['total__avg'], 'avgops':avgops['operations__avg'], 'avgenps':avgenps['amount__avg'], 'service_level': service_level })

def get_districts():
    from django.db import connection, transaction
    cursor=connection.cursor()
    cursor.execute("select distinct state, district from aip_airport order by state")
    rows = cursor.fetchall()
    districts = []
    for r in rows:
        if r[1]:
            districts.append("%s-%s" % (r[0], r[1]))
    return districts

def get_years():
    from django.db import connection, transaction
    cursor=connection.cursor()
    cursor.execute("select distinct fiscal_year from aip_grantrecord")
    rows = cursor.fetchall()
    years = []
    for r in rows:
        years.append(r[0])
    return years
def get_matching_airports(get):
    ports = []
    subtype = None
    parameter = None 
    if get.__contains__('portcode') and get['portcode'] != '':
        portcode = get['portcode']
        try:
            ports.append(Airport.objects.get(code__iexact=portcode))
            subtype = 'code'
        except Airport.DoesNotExist:
            error = 'No airport matched the parameters you specified'
    elif get.__contains__('portname') and get['portname'] != '':
        subtype = 'name'
        portname = get['portname']
        parameter = portname
        ports = Airport.objects.filter(name__icontains=(portname.strip(' ')))

    elif get.__contains__('state') and get['state'] != '':
        subtype='state'
        stateabbrev = get['state']
        parameter = stateabbrev
        if stateabbrev == 'FSM':
            ports = Airport.objects.filter(state__in=['FM', 'MH', 'PW'])
        else:
            ports = Airport.objects.filter(state__iexact=stateabbrev)
    elif get.__contains__('district') and get['district'] != '':
        dist = get['district']
        subtype="district"
        parameter = dist
        state = dist.split('-')[0]
        dnum = dist.split('-')[1]
        ports = Airport.objects.filter(state__iexact=state, district=dnum)

    return {'ports': ports, 'subtype':subtype, 'parameter': parameter}

def get_matching_projects(get):
    projects = Project.objects.all()
        
    if get['district_filter'] != '':
        state = get['district_filter'].split('-')[0]
        dnum = get['district_filter'].split('-')[1]
        portset = Airport.objects.filter(state__iexact=state, district=dnum)
        projects = Project.objects.filter(airport__in=portset)
    if get['year_range_first'] != 2005 or get['year_range_last'] != 2009:
        projects = projects.filter(fiscal_year__gte=get['year_range_first'], fiscal_year__lte=get['year_range_last'])
    if get['npr_range_first'] !=0 or get['npr_range_last'] != 100:
        projects = projects.filter(npr__gte=get['npr_range_first'], npr__lte=get['npr_range_last'])
    if get.__contains__('stimulus'):
        projects = projects.filter(stimulus__gt=0)

    return projects

def get_csv_from_search(request):
    get = request.GET
    if get.__contains__('searchtype'):
        if get['searchtype'] == 'project':
            projects = get_matching_projects(get)
            response = HttpResponse(mimetype="text/csv")
            response['Content-Disposition'] = 'attachment; filename=grantsearch'
            writer = csv.writer(response)
            writer.writerow(["FY", "NPR", "Airport", "Description", "total", "discretionary", "entitlement", "stimulus"])
            for p in projects:
                writer.writerow([p.fiscal_year, p.npr, p.airport.name, p.description, p.total, p.discretionary, p.entitlement, p.stimulus])
            response.close()
            
            return response
    return Http404()

def index(request):
    ports = []
    grants = None
    error = None
    parameter = None
    get = request.GET
    subtype = None
    districts = get_districts()
    years = get_years()
    nprs = []
    for n in range(101):
        nprs.append(n)
    if get.__contains__('searchtype'):
        type = get['searchtype']
    else: 
        return render_to_response('aip/index.html', {'districts':districts, 'years':years, 'nprs':nprs}, context_instance=RequestContext(request))

    if type=='airport':
        portmap = get_matching_airports(get)
        ports = portmap['ports']
        subtype = portmap['subtype']
        parameter = portmap['parameter']
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
            
            return render_to_response('aip/index.html', {subtype: parameter, 'ports':ports, 'grants': grants, 'total': total, 'type': type, 'districts': districts, 'years':years, 'nprs':nprs, 'error':error}, context_instance=RequestContext(request))
        
        else: 
            error = "No Airports found for your search" 
       
    elif type=="project":
        year_first = get['year_range_first']
        year_last = get['year_range_last']
        npr_first = get['npr_range_first']
        npr_last = get['npr_range_last']
        dist_filter = get['district_filter']
    
        if get.__contains__('stimulus'):
            stimulus = True
        else: stimulus = False
        
        filters = {'year_first': int(year_first), 'year_last':int(year_last), 'npr_first':int(npr_first), 'npr_last': int(npr_last), 'dist_filter':dist_filter, 'stimulus':stimulus}
    
        projects = get_matching_projects(get)

        if get['fysort'] == 'asc': projects = projects.order_by('fiscal_year')
        elif get['fysort'] == 'desc': projects = projects.order_by('-fiscal_year')
        if get['nprsort'] == 'asc': projects = projects.order_by('npr')
        elif get['nprsort'] == 'desc': projects = projects.order_by('-npr')
        if get['airportsort'] == 'asc': projects = projects.order_by('airport')
        elif get['airportsort'] == 'desc': projects = projects.order_by('-airport')
        if get['totalsort'] == 'asc': projects = projects.order_by('total')
        elif get['totalsort'] == 'desc': projects = projects.order_by('-total')
        
        sorts = {'fysort': get['fysort'], 'nprsort':get['nprsort'], 'airportsort':get['airportsort'], 'totalsort':get['totalsort']}

        paginator = Paginator(projects, 25)
        try:
            page = int(get.get('page', '1'))
        except ValueError:
            page = 1

        try:
            projects = paginator.page(page)
        except (EmptyPage, InvalidPage):
            projects = paginator.page(paginator.num_pages)
        

        return render_to_response('aip/index.html', {subtype: parameter, 'projects':projects, 'districts': districts, 'years':years, 'nprs':nprs, 'querystring':request.META['QUERY_STRING'], 'sorts':sorts, 'filters':filters, 'numpages': paginator.num_pages, 'page':page, 'type': type, 'error': 'No results found for your search'}, context_instance=RequestContext(request))
        
    if not error:
        error = 'You must specify and airport name or airport code'
    return render_to_response('aip/index.html', {'error': error, 'districts':districts, 'years':years, 'nprs':nprs}, context_instance=RequestContext(request))

