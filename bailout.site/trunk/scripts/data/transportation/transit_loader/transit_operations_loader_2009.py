import os, re
from decimal import Decimal
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from transit.models import *

import csv

uza_list = {}
system_list = {}

operation_stats_list = {}
 

def get_system(trs_id, name, state):
    
    if system_list.has_key(trs_id):
        return system_list[trs_id]
    
    else:
        system, created = TransitSystem.objects.get_or_create(trs_id=trs_id)
        
        if created:
            
            system.name = name
            try:
                system.state = State.objects.matchState(state)
            except:
                print state
                system.state = None
            system.save()
         
        system_list[system.id] = system
         
        return system   
    

def parse_int_field(field):
    
    return int(float(field.replace('(', '').replace(')', '').replace(',', '').replace('$', '')))
    

    
reader = csv.reader(open('2009_data/operations_expense_fares.csv'))

for line in reader:
    
    try:
        trs_state = line[0]
        trs_name = line[1]
        trs_id = int(line[2]) 
        
    except:
        print line
        
    if len(trs_state) != 2:
        continue
        
    system = get_system(trs_id, trs_name, trs_state)
    
    mode = line[4]
    
    if not operation_stats_list.has_key(system.id):
        operation_stats_list[system.id] = {}
    
    if not operation_stats_list[system.id].has_key(mode):
        operation_stats_list[system.id][mode] = {}
    
    if not operation_stats_list[system.id][mode].has_key('operating_expense'):
        operation_stats_list[system.id][mode]['operating_expense'] = 0
        operation_stats_list[system.id][mode]['fares'] = 0

    try:
        operation_stats_list[system.id][mode]['operating_expense'] += parse_int_field(line[9])
    except:
        pass

    try:
        operation_stats_list[system.id][mode]['fares'] += parse_int_field(line[7]) 
    except:
        pass



reader = csv.reader(open('2009_data/capital_expense.csv'))

for line in reader:
    
    try:
        trs_state = line[0]
        trs_name = line[1]
        trs_id = int(line[2]) 
        
    except:
        print line
        
    if len(trs_state) != 2:
        continue
        
    system = get_system(trs_id, trs_name, trs_state)
    
    mode = line[4]
    
    if len(trs_state) != 2:
        continue
    
    if not operation_stats_list.has_key(system.id):
        operation_stats_list[system.id] = {}
    
    if not operation_stats_list[system.id].has_key(mode):
        operation_stats_list[system.id][mode] = {}
        
    if not operation_stats_list[system.id][mode].has_key('capital_expense'):
        operation_stats_list[system.id][mode]['capital_expense'] = 0

    try:
        operation_stats_list[system.id][mode]['capital_expense'] += parse_int_field(line[26]) * 1000
    except:
        pass
    

reader = csv.reader(open('2009_data/operations_stats.csv'))

for line in reader:
    
    try:
        trs_state = line[0]
        trs_name = line[1]
        trs_id = int(line[2]) 
        
    except:
        print line

    system = get_system(trs_id, trs_name, trs_state)
    
    mode = line[4]
    
    if len(trs_state) != 2:
        continue
    
    if not operation_stats_list.has_key(system.id):
        operation_stats_list[system.id] = {}
    
    if not operation_stats_list[system.id].has_key(mode):
        operation_stats_list[system.id][mode] = {}
        
    if not operation_stats_list[system.id][mode].has_key('vehicle_revenue_miles'):
        operation_stats_list[system.id][mode]['vehicle_revenue_miles'] = 0
        operation_stats_list[system.id][mode]['vehicle_revenue_hours'] = 0
        operation_stats_list[system.id][mode]['directional_route_miles'] = None
        operation_stats_list[system.id][mode]['unlinked_passenger_trips'] = 0
        operation_stats_list[system.id][mode]['passenger_miles_traveled'] = 0
        
    
    try:
        operation_stats_list[system.id][mode]['vehicle_revenue_miles'] += (parse_int_field(line[13]) * 1000)
    except:
        pass
    
    try:
        operation_stats_list[system.id][mode]['vehicle_revenue_hours'] += (parse_int_field(line[17]) * 1000)
    except:
        pass

    
    try:
        operation_stats_list[system.id][mode]['unlinked_passenger_trips'] += (parse_int_field(line[19]) * 1000)
    except:
        pass
    
    try:
        operation_stats_list[system.id][mode]['passenger_miles_traveled'] += (parse_int_field(line[21]) * 1000)
    except:
        pass
        
    
        
for system_id in operation_stats_list:
    
    system = system_list[system_id]
    
    for mode in operation_stats_list[system_id]:
    
        stats = OperationStats.objects.create(transit_system=system, year=2008, mode=mode)
        
        if operation_stats_list[system_id][mode].has_key('operating_expense'):
            stats.operating_expense = operation_stats_list[system_id][mode]['operating_expense']
            
        if operation_stats_list[system_id][mode].has_key('capital_expense'):
            stats.capital_expense = operation_stats_list[system_id][mode]['capital_expense']
            
        if operation_stats_list[system_id][mode].has_key('fares'):
            stats.fares = operation_stats_list[system_id][mode]['fares']
            
        if operation_stats_list[system_id][mode].has_key('vehicle_revenue_miles'):
            stats.vehicle_revenue_miles = operation_stats_list[system_id][mode]['vehicle_revenue_miles']
        
        if operation_stats_list[system_id][mode].has_key('vehicle_revenue_hours'):
            stats.vehicle_revenue_hours = operation_stats_list[system_id][mode]['vehicle_revenue_hours']
            
        if operation_stats_list[system_id][mode].has_key('directional_route_miles'):
            stats.directional_route_miles = operation_stats_list[system_id][mode]['directional_route_miles']
            
        if operation_stats_list[system_id][mode].has_key('unlinked_passenger_trips'):
            stats.unlinked_passenger_trips = operation_stats_list[system_id][mode]['unlinked_passenger_trips']
            
        if operation_stats_list[system_id][mode].has_key('passenger_miles_traveled'):
            stats.passenger_miles_traveled = operation_stats_list[system_id][mode]['passenger_miles_traveled']
        
        stats.save()        
    





