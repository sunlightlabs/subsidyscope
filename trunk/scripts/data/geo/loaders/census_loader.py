import os, re, sys

sys.path.append('/root/subsidyscope/bailout.site/trunk/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from faads.models import *

from django.db import connection

from geo.models import *


census_file = open('../data/2008_census_data.csv', 'r')

for line in census_file.readlines()[1:]:
    
    line_parts = line.strip().split(',')
    
    state_fips = int(line_parts[3])
    county_fips = int(line_parts[4])
    
    pop = int(line_parts[17])
    
    if county_fips == 0:
        state = State.objects.get(fips_state_code=state_fips)
        state.population = pop
        state.save()
        
    else:
        county = County.objects.get(fips_county_code=county_fips, state__fips_state_code=state_fips)
        county.population = pop
        county.save()
        