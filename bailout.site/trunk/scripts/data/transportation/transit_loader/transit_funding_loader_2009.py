import os, re
from decimal import Decimal
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from transit.models import *

import csv

uza_list = {}
system_list = {}

funding_stats_list = {}
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
    
    return int(float(field.replace('(', '').replace(')', '').replace(',', '').replace('$', '')) * 1000)
    
    
    
reader = csv.reader(open('2009_data/operations_funds.csv'))

for line in reader:
    
    try:
        trs_state = line[0]
        trs_name = line[1]
        trs_id = int(line[2]) 
        
    except:
        print line
        
    system = get_system(trs_id, trs_name, trs_state)
    
    if not funding_stats_list.has_key(system.id):
        funding_stats_list[system.id] = {}
    
    try:
        funding_stats_list[system.id]['operating_fares'] =  parse_int_field(line[5]) + parse_int_field(line[7]) 
    except:
        funding_stats_list[system.id]['operating_fares'] = None
        
        
    try:
        funding_stats_list[system.id]['operating_other'] =  parse_int_field(line[9]) + parse_int_field(line[11]) 
    except:
        funding_stats_list[system.id]['operating_other'] = None
    
    
    try:
        funding_stats_list[system.id]['operating_federal'] =  parse_int_field(line[13]) + parse_int_field(line[15]) 
    except:
        funding_stats_list[system.id]['operating_federal'] = None
    
    
    try:
        funding_stats_list[system.id]['operating_state'] =  parse_int_field(line[17]) + parse_int_field(line[19]) 
    except:
        funding_stats_list[system.id]['operating_state'] = None
        
    try:
        funding_stats_list[system.id]['operating_local'] =  parse_int_field(line[21]) + parse_int_field(line[23]) 
    except:
        funding_stats_list[system.id]['operating_local'] = None

    
    funding_stats_list[system.id]['operating_reconciliation'] = None



reader = csv.reader(open('2009_data/capital_funds.csv'))

for line in reader:
    
    try:
        trs_state = line[0]
        trs_name = line[1]
        trs_id = int(line[2]) 
        
    except:
        print line
        
    system = get_system(trs_id, trs_name, trs_state)
    
    if not funding_stats_list.has_key(system.id):
        funding_stats_list[system.id] = {}
        
        
    try:
        funding_stats_list[system.id]['capital_other'] =  parse_int_field(line[5]) + parse_int_field(line[6]) 
    except:
        funding_stats_list[system.id]['capital_other'] = None
        
    try:
        funding_stats_list[system.id]['capital_state'] =  parse_int_field(line[7]) + parse_int_field(line[9]) 
    except:
        funding_stats_list[system.id]['capital_state'] = None
        
    try:
        funding_stats_list[system.id]['capital_local'] =  parse_int_field(line[10]) + parse_int_field(line[12]) 
    except:
        funding_stats_list[system.id]['capital_local'] = None

    try:
        funding_stats_list[system.id]['capital_federal'] =  parse_int_field(line[13]) + parse_int_field(line[15]) + parse_int_field(line[17]) + parse_int_field(line[19]) + parse_int_field(line[21])
    except:
        funding_stats_list[system.id]['capital_federal'] = None

        
for system_id in funding_stats_list:
    
    system = system_list[system_id]
    
    stats = FundingStats.objects.create(transit_system=system, year=2008)
    
    if funding_stats_list[system_id].has_key('capital_federal'):
        stats.capital_federal = funding_stats_list[system_id]['capital_federal']
    if funding_stats_list[system_id].has_key('capital_state'):    
        stats.capital_state = funding_stats_list[system_id]['capital_state']
    if funding_stats_list[system_id].has_key('capital_local'):
        stats.capital_local = funding_stats_list[system_id]['capital_local']
    if funding_stats_list[system_id].has_key('capital_other'):
        stats.capital_other = funding_stats_list[system_id]['capital_other']

    if funding_stats_list[system_id].has_key('operating_fares'):
        stats.operating_fares = funding_stats_list[system_id]['operating_fares']
    if funding_stats_list[system_id].has_key('operating_federal'):
        stats.operating_federal = funding_stats_list[system_id]['operating_federal']
    if funding_stats_list[system_id].has_key('operating_state'):
        stats.operating_state = funding_stats_list[system_id]['operating_state']
    if funding_stats_list[system_id].has_key('operating_local'):
        stats.operating_local = funding_stats_list[system_id]['operating_local']
    if funding_stats_list[system_id].has_key('operating_other'):
        stats.operating_other = funding_stats_list[system_id]['operating_other']
    if funding_stats_list[system_id].has_key('operating_reconciliation'):
        stats.operating_reconciliation = funding_stats_list[system_id]['operating_reconciliation']

    stats.save()
        
        
        
        
    




