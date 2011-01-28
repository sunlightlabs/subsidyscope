import os
from datetime import date
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from eas.models import *

airports = {}

airport_data = open('data/airports.csv', 'r')

for airport in airport_data.readlines():
    
    airport = {}
    
    line_parts = line.strip().split(',')
    
    code = line_parts[0]
    airport['code'] = code
    
    name_parts = line_parts[1].split(':')

    airport['location'] = name_parts[0].strip(',')
    
    if len(name_parts) > 1:
        airport['location'] = name_parts[0].strip(',')
    else:
        airport['location'] = ''
    
    airport['code'] = code 
    
    airports[code] = airport
    


eas_recipients = {}

recipient_data = open('data/eas_recipients.csv', 'r')

for line in recipient_data.readlines():
    
    line_parts = line.strip().split(',')
    
    code = line_parts[5]
    
    eas_recipients[code] = {}
    
    eas_recipients[code]['amount'] = line_parts[0]
    eas_recipients[code]['order'] = line_parts[4]
    
    eas_recipients[code]['city'] = line_parts[2]
    eas_recipients[code]['state'] = line_parts[1].title()
    eas_recipients[code]['code'] = code
    
    eas_recipients[code]['passengers'] = 0
    eas_recipients[code]['freight'] = 0
    eas_recipients[code]['mail'] = 0
    
    
    eas_recipients[code]['routes'] = {}
    eas_recipients[code]['carriers'] = {}


recipient_data.close()

destinations = {}

route_data = open('data/eas_routes.csv', 'r')    

for line in route_data.readlines():

    line_parts = line.strip().split('|')
        
    passengers = int(line_parts[0])
    freight = int(line_parts[1])
    mail = int(line_parts[2])
    distance = int(line_parts[3])
    
    carrier = line_parts[4]
    
    if eas_recipients.has_key(line_parts[5]):
        recipient = line_parts[5]
        destination = line_parts[7]
        city = line_parts[8]
        
    if eas_recipients.has_key(line_parts[7]):
        recipient = line_parts[7]
        destination = line_parts[5]
        city = line_parts[6]
        
    if not eas_recipients[recipient]['routes'].has_key(destination):
        eas_recipients[recipient]['routes'][destination] = {}
        eas_recipients[recipient]['routes'][destination]['carriers'] = {}
        eas_recipients[recipient]['routes'][destination]['passengers'] = 0 
        eas_recipients[recipient]['routes'][destination]['freight'] = 0 
        eas_recipients[recipient]['routes'][destination]['mail'] = 0
        
        
        destinations[destination] = {}
        
        destinations[destination] = city
        
    if not eas_recipients[recipient]['carriers'].has_key(carrier):
        eas_recipients[recipient]['carriers'][carrier] = {}
        eas_recipients[recipient]['carriers'][carrier]['passengers'] = 0 
        eas_recipients[recipient]['carriers'][carrier]['freight'] = 0 
        eas_recipients[recipient]['carriers'][carrier]['mail'] = 0
        
        
        destinations[destination] = {}
        
        destinations[destination] = city

    
    if not eas_recipients[recipient]['routes'][destination]['carriers'].has_key(carrier):
        eas_recipients[recipient]['routes'][destination]['carriers'][carrier] = {}
        eas_recipients[recipient]['routes'][destination]['carriers'][carrier]['passengers'] = 0
        eas_recipients[recipient]['routes'][destination]['carriers'][carrier]['freight'] = 0
        eas_recipients[recipient]['routes'][destination]['carriers'][carrier]['mail'] = 0
        eas_recipients[recipient]['routes'][destination]['carriers'][carrier]['distance'] = distance
    
    eas_recipients[recipient]['routes'][destination]['carriers'][carrier]['passengers'] += passengers
    eas_recipients[recipient]['routes'][destination]['carriers'][carrier]['freight'] += freight
    eas_recipients[recipient]['routes'][destination]['carriers'][carrier]['mail'] += mail
    
    eas_recipients[recipient]['routes'][destination]['passengers'] += passengers
    eas_recipients[recipient]['routes'][destination]['freight'] += freight
    eas_recipients[recipient]['routes'][destination]['mail'] += mail
    
    eas_recipients[recipient]['carriers'][carrier]['passengers'] += passengers
    eas_recipients[recipient]['carriers'][carrier]['freight'] += freight
    eas_recipients[recipient]['carriers'][carrier]['mail'] += mail
    
    eas_recipients[recipient]['passengers'] += passengers
    eas_recipients[recipient]['freight'] += freight
    eas_recipients[recipient]['mail'] += mail
    
        
for recipient in eas_recipients:
    
    print '%s, %s (%s) - %s' % (eas_recipients[recipient]['city'], eas_recipients[recipient]['state'], recipient, eas_recipients[recipient]['order'])   
    print '%d, %d, %d' % (eas_recipients[recipient]['passengers'], eas_recipients[recipient]['freight'], eas_recipients[recipient]['mail'])
    
    
    for carrier in eas_recipients[recipient]['carriers']:
        if eas_recipients[recipient]['carriers'][carrier]['passengers'] > 0:
            passenger_percent = float(eas_recipients[recipient]['carriers'][carrier]['passengers']) / float(eas_recipients[recipient]['passengers']) 
        else:
            passenger_percent = 0
        
        if passenger_percent > 0.05:
        
            print '\t%s' % (carrier) 
            print '\t%d (%f), %d, %d' % (eas_recipients[recipient]['carriers'][carrier]['passengers'],  passenger_percent,
                                      eas_recipients[recipient]['carriers'][carrier]['freight'],
                                      eas_recipients[recipient]['carriers'][carrier]['mail'])
            


    
    for destination in eas_recipients[recipient]['routes']:
        
        if eas_recipients[recipient]['routes'][destination]['passengers'] > 0:
            passenger_percent = float(eas_recipients[recipient]['routes'][destination]['passengers']) / float(eas_recipients[recipient]['passengers']) 
        else:
            passenger_percent = 0
        
        if passenger_percent > 0.05:
        
            print '\t%s (%s)' % (destinations[destination], destination) 
            print '\t%d (%f), %d, %d' % (eas_recipients[recipient]['routes'][destination]['passengers'],  passenger_percent,
                                      eas_recipients[recipient]['routes'][destination]['freight'],
                                      eas_recipients[recipient]['routes'][destination]['mail'])
            
            for carrier in eas_recipients[recipient]['routes'][destination]['carriers']:
                
                print '\t\t%s' % (carrier)
                print '\t\t%d, %d, %d' % (eas_recipients[recipient]['routes'][destination]['carriers'][carrier]['passengers'], 
                                  eas_recipients[recipient]['routes'][destination]['carriers'][carrier]['freight'],
                                  eas_recipients[recipient]['routes'][destination]['carriers'][carrier]['mail'])
