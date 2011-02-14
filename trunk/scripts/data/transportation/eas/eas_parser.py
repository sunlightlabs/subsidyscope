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

    

eas_recipients = {}

recipient_data = open('data/eas_recipients.csv', 'r')

for line in recipient_data.readlines():
    
    line_parts = line.strip().split(',')
    
    code = line_parts[5]
    
    airport_data = airports[code]
    
    airport = Airport.objects.create(code=airport_data['code'], name=airport_data['name'], location=airport_data['location'], eas=True, hub=Airport.NON_HUB)
    

