#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from bailout.models import * 
from geo.models import * 
from django.core.exceptions import ObjectDoesNotExist

states = StateMatcher()

data_dir = 'data/'

counties = open(data_dir + 'counties.csv', 'r')

first_line = True

for county in counties.readlines():
    
    if not first_line:
    
        county_parts = county.strip().split(',')
        
        state = states.matchFips(int(county_parts[0]))
        
        if state:
            
            try:
                county_fips = int(county_parts[1])
                full_fips = int('%s%s' % (county_parts[0], county_parts[1]))
                
                if county_parts[5] != '':
                    csa_code = int(county_parts[5]) 
                else:
                    csa_code = None
                    
                if county_parts[6] != '':
                    cbsa_code = int(county_parts[6]) 
                else:
                    cbsa_code = None
                    
                    
                if county_parts[7] != '':
                    mdiv_code = int(county_parts[7]) 
                else:
                    mdiv_code = None
                
                County.objects.create(state=state, fips_county_code=county_fips, fips_full_code=full_fips, 
                                      name=county_parts[2], name_complete=county_parts[3], 
                                      lsad_code=int(county_parts[4]),
                                      csa_code=csa_code, cbsa_code=cbsa_code, mdiv_code=mdiv_code)
            except:
                
                print "bad county: %s" % str(county_parts)
            
        else:
            print "bad state: %s" % str(county_parts)
    
    else:
        first_line = False
    