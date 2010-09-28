import os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from transit.models import *
from inflation.models import InflationIndex
import csv

CURRENT_YEAR = 2008
cpi = InflationIndex.objects.get(name="CPI")

uza_list = {}
system_list = {}

operation_stats_list = {}


def get_uza(uza_id, name, pop, area):
    
    if uza_list.has_key(uza_id):
        
        return uza_list[uza_id]

    else:
        uza, created = UrbanizedArea.objects.get_or_create(fta_id=uza_id)
    
        if created:
            uza.name = name
            uza.population = pop
            uza.area = area
            uza.save()
        
        uza_list[uza.id] = uza
         
        return uza
    
    
    
def get_system(trs_id, name, city, state, uza_id, uza_name, pop, area):
    
    if system_list.has_key(trs_id):
        return system_list[trs_id]
    
    else:
        system, created = TransitSystem.objects.get_or_create(trs_id=trs_id)
        
        if created:
            system.urbanized_area = get_uza(uza_id, uza_name, pop, area)
            system.name = name
            system.city = city 
            try:
                system.state = State.objects.matchState(state)
            except:
                print state
                system.state = None
            system.save()
         
        system_list[system.id] = system
         
        return system   
    

def parse_operation_line(line, operation_type):
    
    try:
        
        trs_id = int(line[1]) 
        trs_name = line[2]
        trs_city = line[3]
        trs_state = line[4]
        uza_name = line[5]
        uza_id = int(line[6])
        area = int(line[7].replace(',', ''))
        pop = int(line[8].replace(',', ''))
        
        mode = line[9]
        type_of_service = line[10]
        
    except:
        print line

    
    system = get_system(trs_id, trs_name, trs_city, trs_state, uza_id, uza_name, pop, area)

    
    if not operation_stats_list.has_key(system.id):
        operation_stats_list[system.id] = {}


    i = 11 
    
    
    for year in range(1991, 2009):
        
        if not operation_stats_list[system.id].has_key(year):
            operation_stats_list[system.id][year] = {}
            
        if not operation_stats_list[system.id][year].has_key(mode):
            operation_stats_list[system.id][year][mode] = {}
            
        if not operation_stats_list[system.id][year][mode].has_key(operation_type):
            operation_stats_list[system.id][year][mode][operation_type] = 0
            
        try:
            if operation_type in ['operating_expense', 'capital_expense', 'fares']:
                operation_stats_list[system.id][year][mode][operation_type] += cpi.convertValue(int(line[i].replace('(', '').replace(')', '').replace(',', '').replace('$', '')), CURRENT_YEAR, year)

            operation_stats_list[system.id][year][mode][operation_type] += int(line[i].replace('(', '').replace(')', '').replace(',', '').replace('$', ''))
            
        except:
            pass
            # how to handle nulls?
            #operation_stats_list[system.id][year][mode][operation_type] = None
            
            
        i += 1
        
        


reader = csv.reader(open('operations_data/op_expense.csv'))

reader.next()

for line in reader:
    
    parse_operation_line(line, 'operating_expense')

    
    
reader = csv.reader(open('operations_data/cap_expense.csv', 'rU'))

reader.next()

for line in reader:
    
    parse_operation_line(line, 'capital_expense')
   
 
    
reader = csv.reader(open('operations_data/op_fares.csv'))

reader.next()

for line in reader:
    
    parse_operation_line(line, 'fares')
    
    

reader = csv.reader(open('operations_data/op_drm.csv'))

reader.next()

for line in reader:
    
    parse_operation_line(line, 'directional_route_miles')
    
    
    
reader = csv.reader(open('operations_data/op_vrh.csv'))

reader.next()

for line in reader:
    
    parse_operation_line(line, 'vehicle_revenue_hours')
    
    
    
reader = csv.reader(open('operations_data/op_vrm.csv'))

reader.next()

for line in reader:
    
    parse_operation_line(line, 'vehicle_revenue_miles')
    
    
reader = csv.reader(open('operations_data/op_pmt.csv'))

reader.next()

for line in reader:
    
    parse_operation_line(line, 'passenger_miles_traveled')
    

reader = csv.reader(open('operations_data/op_upt.csv'))

reader.next()

for line in reader:
    
    parse_operation_line(line, 'unlinked_passenger_trips')


for system_id in operation_stats_list:
    
    system = system_list[system_id]
    
    for year in operation_stats_list[system_id]:
        
        for mode in operation_stats_list[system_id][year]:
        
            stats = OperationStats.objects.create(transit_system=system, year=year, mode=mode)
            
            if operation_stats_list[system_id][year][mode].has_key('operating_expense'):
                stats.operating_expense = operation_stats_list[system_id][year][mode]['operating_expense']
                
            if operation_stats_list[system_id][year][mode].has_key('capital_expense'):
                stats.capital_expense = operation_stats_list[system_id][year][mode]['capital_expense']
                
            if operation_stats_list[system_id][year][mode].has_key('fares'):
                stats.fares = operation_stats_list[system_id][year][mode]['fares']
                
            if operation_stats_list[system_id][year][mode].has_key('vehicle_revenue_miles'):
                stats.vehicle_revenue_miles = operation_stats_list[system_id][year][mode]['vehicle_revenue_miles']
            
            if operation_stats_list[system_id][year][mode].has_key('vehicle_revenue_hours'):
                stats.vehicle_revenue_hours = operation_stats_list[system_id][year][mode]['vehicle_revenue_hours']
                
            if operation_stats_list[system_id][year][mode].has_key('directional_route_miles'):
                stats.directional_route_miles = operation_stats_list[system_id][year][mode]['directional_route_miles']
                
            if operation_stats_list[system_id][year][mode].has_key('unlinked_passenger_trips'):
                stats.unlinked_passenger_trips = operation_stats_list[system_id][year][mode]['unlinked_passenger_trips']
                
            if operation_stats_list[system_id][year][mode].has_key('passenger_miles_traveled'):
                stats.passenger_miles_traveled = operation_stats_list[system_id][year][mode]['passenger_miles_traveled']
            
            stats.save()
