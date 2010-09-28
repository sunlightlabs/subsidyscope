import os
import re
import csv

from decimal import Decimal
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from transit.models import *

reader = csv.reader(open('2009_data/operations_funds.csv'))

re_acronym = re.compile('.*[(](.*)[)]$')

for line in reader:

    match = re_acronym.match(line[1])
    
    if match:
        
        trs_id = int(line[2])
        commmon_name = match.group(1).strip()
        
        try:
            system = TransitSystem.objects.get(trs_id=trs_id)
            system.common_name = commmon_name
            system.save()
            
        except:
            print '%d,%s' % (trs_id, commmon_name)
            
        
        
 