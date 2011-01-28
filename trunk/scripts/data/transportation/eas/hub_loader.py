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


hub_data = open('data/small_hubs.txt', 'r')

for line in hub_data.readlines():
    
    line_parts = line.strip().split('\t')
    
    code = line_parts[0]
    
    airport_data = airports[code]
    
    airport = Airport.objects.create(code=airport_data['code'], name=airport_data['name'], location=airport_data['location'], eas=False, hub=Airport.SMALL_HUB)


hub_data = open('data/medium_hubs.txt', 'r')

for line in hub_data.readlines():
    
    line_parts = line.strip().split('\t')
    
    code = line_parts[0]
    
    airport_data = airports[code]
    
    airport = Airport.objects.create(code=airport_data['code'], name=airport_data['name'], location=airport_data['location'], eas=False, hub=Airport.MEDIUM_HUB)
    
    
hub_data = open('data/large_hubs.txt', 'r')

for line in hub_data.readlines():
    
    line_parts = line.strip().split('\t')
    
    code = line_parts[0]
    
    airport_data = airports[code]
    
    airport = Airport.objects.create(code=airport_data['code'], name=airport_data['name'], location=airport_data['location'], eas=False, hub=Airport.LARGE_HUB)
    
    