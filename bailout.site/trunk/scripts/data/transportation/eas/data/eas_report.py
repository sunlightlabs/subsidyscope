import os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from eas.models import * 

carriers = {}

for route in EASRoute.objects.all():
    
    
    flights, passengers, time, distance = route.calculateSubsidy()
    
    if flights > 0:
        
        total_subsidy = float(flights) * float(route.eas_flight_subsidy)
        passenger_subsidy = total_subsidy / float(passengers)
        passenger_mile_subsidy = passenger_subsidy / (float(distance) / float(flights))
        
        if not carriers.has_key(route.carrier):
            
            carriers[route.carrier] = {}
            carriers[route.carrier]['total'] = 0
            carriers[route.carrier]['flights'] = 0
            carriers[route.carrier]['passengers'] = 0
            carriers[route.carrier]['distance'] = 0
            
        carriers[route.carrier]['total'] += total_subsidy
        carriers[route.carrier]['flights'] += flights    
        carriers[route.carrier]['passengers'] += passengers
        carriers[route.carrier]['distance'] += distance
        
        print '%s (%s)|%s|%.2f|%d|%d|%.2f|%.2f' % (route.eas_airport.location, route.eas_airport.code, route.carrier.name, total_subsidy, flights, passengers, passenger_subsidy, passenger_mile_subsidy)

for carrier in carriers:
    
    passenger_subsidy = float(carriers[carrier]['total']) / float(carriers[carrier]['passengers'])
    
    avg_distance = float(carriers[carrier]['distance']) / float(carriers[carrier]['flights'])
    
    passenger_mile_subsidy = passenger_subsidy / avg_distance
    
    #print '%s|%d|%d|%d|%.2f|%.2f|%.2f' % (carrier, carriers[carrier]['total'], carriers[carrier]['flights'], carriers[carrier]['passengers'], avg_distance, passenger_subsidy, passenger_mile_subsidy)