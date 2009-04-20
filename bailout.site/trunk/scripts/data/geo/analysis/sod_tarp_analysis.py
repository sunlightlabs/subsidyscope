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

for county in County.objects.all():
 
    for branch in county.institutionbranch_set.all():
        
        total_branches += 1
        total_deposits += branch.deposits
         
        if tarp_participation[branch.institution.id]:
            tarp_branches += 1
            tarp_deposits += branch.deposits


for county in County.objects.all():
    
    county_total_deposits = Decimal('0')
    county_tarp_deposits = Decimal('0')
    
    county_total_branches = Decimal('0')
    county_tarp_branches = Decimal('0')
 
    for branch in county.institutionbranch_set.all():
        
        county_total_branches += 1
        county_total_deposits += branch.deposits
         
        if tarp_participation[branch.institution.id]:
            county_tarp_branches += 1
            county_tarp_deposits += branch.deposits
    
              
    if tarp_deposits > 0:
        tarp_deposits_percentage = county_tarp_deposits / county_total_deposits
    else:
        tarp_deposits_percentage = Decimal('0')
        
    if tarp_branches > 0:
        tarp_branches_percentage = county_tarp_branches / county_total_branches
    else:
        tarp_branches_percentage = Decimal('0')
    
    print '%05d,%02d,%03d,%s,%s,%s,%s,%s,%s' % (county.fips_full_code,
                                                    county.state.fips_state_code,
                                                    county.fips_county_code,
                                                    county_total_deposits.quantize(Decimal('0')),
                                                    county_tarp_deposits.quantize(Decimal('0')),
                                                    tarp_deposits_percentage.quantize(Decimal('0.0001')),
                                                    county_total_branches,
                                                    county_tarp_branches,
                                                    tarp_branches_percentage.quantize(Decimal('0.0001')))
        
    