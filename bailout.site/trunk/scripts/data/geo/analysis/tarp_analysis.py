#!/usr/bin/env python
import os
from decimal import Decimal
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from bailout.models import * 
from geo.models import * 

tarp_participation = {}

for institution in Institution.objects.all():
    
   tarp_participation[institution.id] = institution.getParentTARPParticipation()
    

total_deposits = Decimal('0')
tarp_deposits = Decimal('0')

total_branches = Decimal('0')
tarp_branches = Decimal('0')

for county in County.objects.all().order_by('state__name', 'name'):
 
    county_total_deposits = Decimal('0')
    county_tarp_deposits = Decimal('0')
    tarp_deposits_percentage = Decimal('0')
    
    county_total_branches = Decimal('0')
    county_tarp_branches = Decimal('0')
    tarp_branches_percentage = Decimal('0')
    
    try:
        county_total_lending = Decimal(county.countysummary.loans)
    except:
        county_total_lending = Decimal('0')
        
    county_tarp_lending = Decimal('0')
    tarp_lending_percentage = Decimal('0')
    
    for county_summary in county.institutioncountysummary_set.all():
        
        if county_summary.institution_branches != None:
            total_branches += county_summary.institution_branches
            county_total_branches += county_summary.institution_branches
        
            total_deposits += county_summary.institution_deposits
            county_total_deposits += county_summary.institution_deposits
         
        if tarp_participation[county_summary.institution.id]:
            
            if county_summary.institution_branches != None:
                county_tarp_branches += county_summary.institution_branches
                county_tarp_deposits += county_summary.institution_deposits
                
                tarp_deposits_percentage += county_summary.deposits_county_percent
                tarp_branches_percentage += county_summary.branches_county_percent
            
            if county_summary.institution_loans != None:
                county_tarp_lending += county_summary.institution_loans
                tarp_lending_percentage += county_summary.loans_county_percent
                

    print '%s,%s,%05d,%02d,%03d,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (county.name_complete, county.state.name, county.fips_full_code,
                                                    county.state.fips_state_code,
                                                    county.fips_county_code,
                                                    county_total_deposits.quantize(Decimal('0')),
                                                    county_tarp_deposits.quantize(Decimal('0')),
                                                    tarp_deposits_percentage.quantize(Decimal('0.0001')),
                                                    county_total_branches,
                                                    county_tarp_branches,
                                                    tarp_branches_percentage.quantize(Decimal('0.0001')),
                                                    county_total_lending,
                                                    county_tarp_lending,
                                                    tarp_lending_percentage.quantize(Decimal('0.0001')))
