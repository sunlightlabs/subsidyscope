import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import re

from bailout.models import *
from geo.models import *

ein_regex = re.compile('\(([0-9]{2,2}-[0-9]{7,7}) ')
hmda_regex = re.compile('\(([0-9]{10,10}) ')

tarp_ids = {}

for institution in Institution.objects.filter(id__lt=600):
    
    if institution.fed_number:
        
        file_2007 = 'data/2007/org/%d.txt' % (institution.fed_number)
        file_2008 = 'data/2008/org/%d.txt' % (institution.fed_number)
        
        if os.path.exists(file_2007):
            
            file = open(file_2007, 'r')
            lines = file.readlines()
            file.close()
            
            for line in lines:
                
                for ein in ein_regex.findall(line):                
                    tarp_ids[ein] = institution.fed_number
                
                for hmda in hmda_regex.findall(line):
                    tarp_ids[hmda] = institution.fed_number
                
        if os.path.exists(file_2008):
            
            file = open(file_2008, 'r')
            lines = file.readlines()
            file.close()
            
            for line in lines:
                
                for ein in ein_regex.findall(line):
                    tarp_ids[ein] = institution.fed_number
                
                for hmda in hmda_regex.findall(line):
                    tarp_ids[hmda] = institution.fed_number
                

inst_file = open('data/2007/2007HMDAInstitutionRecords.TXT', 'r')
institutions = inst_file.readlines() 
inst_file.close()

institution_names = {}

for institution in institutions:
    
    institution_parts = institution.strip().split('\t')
    
    id = int(institution_parts[1].replace('-', ''))
    
    name = institution_parts[9] 
    
    if not name == '':
            
        city = institution_parts[11]
        state = institution_parts[12]
        
        name_place = '%s_%s_%s' % (name, city, state) 
    
        if not institution_names.has_key(name_place):
            institution_names[name_place] = []
        
        institution_names[name_place].append(id) 
    
for institution in institutions:
    
    institution_parts = institution.strip().split('\t')
    
    id = int(institution_parts[1].replace('-', ''))
    name = institution_parts[9]
    city = institution_parts[11]
    state = institution_parts[12]
        
    name_place = '%s_%s_%s' % (name, city, state) 
    
    
    if not tarp_ids.has_key(id) and institution_names.has_key(name_place):
            
        for alt_id in institution_names[name_place]:
            
            if tarp_ids.has_key(alt_id):
                tarp_ids[id] = tarp_ids[alt_id]
                #print '%d, %d (%d): %s' % (id, alt_id, tarp_ids[alt_id], name_place)

for id in tarp_ids.keys():
    print '%s,%d' % (id, tarp_ids[id])


                