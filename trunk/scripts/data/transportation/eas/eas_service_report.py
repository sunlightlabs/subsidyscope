import os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.db.models import Q
from eas.models import * 

carriers = {}

for route in EASRoute.objects.filter(intermediate_airport=None):
    
    route_months = []
    
    if route.eas_start_date.year < 2008:
        if route.eas_end_date.year > 2008:
            route_months = range(1,12+1)
        else:
            route_months = range(1,route.eas_end_date.month+1)
    
    else:
        if route.eas_end_date.year > 2008:
            route_months = range(route.eas_start_date.month,12+1)
        else:
            route_months = range(route.eas_start_date.month,route.eas_end_date.month+1)
            
    print route.carrier.name, route.eas_airport.name, route.eas_weekly_flights
    
    departures_scheduled = 0 
    departures_performed = 0
    
    for route_stats in RouteStatistics.objects.filter((Q(carrier=route.carrier) & Q(month__in=route_months) & ((Q(destination_airport__in=route.hub_airport.all()) & Q(origin_airport=route.eas_airport)) | (Q(destination_airport=route.eas_airport) & Q(origin_airport__in=route.hub_airport.all()))))).order_by('month'):
        print '\t%d: %d/%d' % (route_stats.month, route_stats.departures_scheduled, route_stats.departures_performed)
        departures_scheduled += route_stats.departures_scheduled
        departures_performed += route_stats.departures_performed
        
    print '+:',route.eas_weekly_flights*4.25*len(route_months),departures_performed,departures_scheduled
        
        
     