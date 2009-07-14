import os
from datetime import date
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from eas.models import *

airports = {}

airport_data = open('data/airports.csv', 'r')

for line in airport_data.readlines():
    
    airport = {}
    
    line_parts = line.strip().split('|')
    
    code = line_parts[0]
    airport['code'] = code
    
    if len(line_parts) > 1:
        name_parts = line_parts[1].split(':')
    
        airport['location'] = name_parts[0].strip().strip(',')
        
        if len(name_parts) > 1:
            airport['name'] = name_parts[1].strip().strip(',')
        else:
            airport['name'] = ''
        
        airport['code'] = code 
        
        airports[code] = airport


route_data = open('data/eas_routes.csv', 'r')

for route in route_data.readlines()[1:]:
    
    route_parts = route.strip().split('|')
    
    try:
        carrier_code = route_parts[10]
        carrier = Carrier.objects.get(code=carrier_code)
    except Carrier.DoesNotExist:
        carrier_code = route_parts[10]
        carrier_name = route_parts[11]
        carrier = Carrier.objects.create(code=carrier_code, name=carrier_name)
        
    try:
        origin_code = route_parts[12]
        origin = Airport.objects.get(code=origin_code)
    except Airport.DoesNotExist:
        print origin_code
        airport_data = airports[origin_code]
        origin = Airport.objects.create(code=airport_data['code'], name=airport_data['name'], location=airport_data['location'], eas=False, hub=Airport.NON_HUB)

    try:
        destination_code = route_parts[14]
        destination = Airport.objects.get(code=destination_code)
    except Airport.DoesNotExist:
        print destination_code
        airport_data = airports[destination_code]
        destination = Airport.objects.create(code=airport_data['code'], name=airport_data['name'], location=airport_data['location'], eas=False, hub=Airport.NON_HUB)

    departures_scheduled = int(route_parts[0])
    departures_performed = int(route_parts[1])
    
    seats = int(route_parts[2])
    payload = int(route_parts[3])
    
    passengers = int(route_parts[4])
    freight = int(route_parts[5])
    mail = int(route_parts[6])
    
    distance = int(route_parts[7])
    
    ramp_time = int(route_parts[8])
    air_time = int(route_parts[9])
     
    year = int(route_parts[16])
    month = int(route_parts[17])
    
    route_statistics = RouteStatistics.objects.create(carrier=carrier,
                                                       origin_airport=origin,
                                                       destination_airport=destination,
                                                       departures_scheduled=departures_scheduled, 
                                                       departures_performed=departures_performed, 
                                                       seats=seats, 
                                                       payload=payload, 
                                                       passengers=passengers, 
                                                       freight=freight, 
                                                       mail=mail, 
                                                       distance=distance, 
                                                       ramp_time=ramp_time, 
                                                       flight_time=air_time, 
                                                       year=year, 
                                                       month=month)
    
    