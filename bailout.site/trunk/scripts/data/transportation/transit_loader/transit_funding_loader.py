import os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from transit.models import *

import csv

uza_list = {}
system_list = {}

funding_stats_list = {}
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
        
        uza_list[uza.fta_id] = uza
         
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
    
    
    
def parse_funding_line(line, funding_type):
    
    try:
        trs_id = int(line[1]) 
        trs_name = line[2]
        trs_city = line[3]
        trs_state = line[4]
        uza_name = line[5]
        uza_id = int(line[6])
        area = int(line[7].replace(',', ''))
        pop = int(line[8].replace(',', ''))
        
    except:
        print line
        
    system = get_system(trs_id, trs_name, trs_city, trs_state, uza_id, uza_name, pop, area)
    
    if not funding_stats_list.has_key(system.id):
        funding_stats_list[system.id] = {}
    
    
    i = 9 
    
    for year in range(1991, 2009):
        
        if not funding_stats_list[system.id].has_key(year):
            funding_stats_list[system.id][year] = {}
            
        try:
            funding_stats_list[system.id][year][funding_type] = int(line[i].replace('(', '').replace(')', '').replace(',', '').replace('$', ''))
        except:
            funding_stats_list[system.id][year][funding_type] = None
        
        i += 1
    

reader = csv.reader(open('funding_data/cap_fed.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'capital_federal')
        
    
    
reader = csv.reader(open('funding_data/cap_local.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'capital_local')



reader = csv.reader(open('funding_data/cap_other.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'capital_other')



reader = csv.reader(open('funding_data/cap_state.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'capital_state')



reader = csv.reader(open('funding_data/cap_local.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'capital_local')
    
    
    
reader = csv.reader(open('funding_data/op_fare.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'operating_fares')



reader = csv.reader(open('funding_data/op_fed.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'operating_federal')



reader = csv.reader(open('funding_data/op_local.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'operating_local')



reader = csv.reader(open('funding_data/op_other.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'operating_other')



reader = csv.reader(open('funding_data/op_local.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'operating_local')



reader = csv.reader(open('funding_data/op_other.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'operating_other')



reader = csv.reader(open('funding_data/op_reconciliation.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'operating_reconciliation')



reader = csv.reader(open('funding_data/op_state.csv'))

reader.next()

for line in reader:
    
    parse_funding_line(line, 'operating_state')



for system_id in funding_stats_list:
    
    system = system_list[system_id]
    
    for year in funding_stats_list[system_id]:
        
        stats = FundingStats.objects.create(transit_system=system, year=year)
        
        if funding_stats_list[system_id][year].has_key('capital_federal'):
            stats.capital_federal = funding_stats_list[system_id][year]['capital_federal']
        if funding_stats_list[system_id][year].has_key('capital_state'):    
            stats.capital_state = funding_stats_list[system_id][year]['capital_state']
        if funding_stats_list[system_id][year].has_key('capital_local'):
            stats.capital_local = funding_stats_list[system_id][year]['capital_local']
        if funding_stats_list[system_id][year].has_key('capital_other'):
            stats.capital_other = funding_stats_list[system_id][year]['capital_other']
    
        if funding_stats_list[system_id][year].has_key('operating_fares'):
            stats.operating_fares = funding_stats_list[system_id][year]['operating_fares']
        if funding_stats_list[system_id][year].has_key('operating_federal'):
            stats.operating_federal = funding_stats_list[system_id][year]['operating_federal']
        if funding_stats_list[system_id][year].has_key('operating_state'):
            stats.operating_state = funding_stats_list[system_id][year]['operating_state']
        if funding_stats_list[system_id][year].has_key('operating_local'):
            stats.operating_local = funding_stats_list[system_id][year]['operating_local']
        if funding_stats_list[system_id][year].has_key('operating_other'):
            stats.operating_other = funding_stats_list[system_id][year]['operating_other']
        if funding_stats_list[system_id][year].has_key('operating_reconciliation'):
            stats.operating_reconciliation = funding_stats_list[system_id][year]['operating_reconciliation']
    
        stats.save()
        
        
        
        
    




