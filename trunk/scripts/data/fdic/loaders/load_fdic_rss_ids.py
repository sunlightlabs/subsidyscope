#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from bailout.models import * 
from etl.models import *


fdic_datarun = DataRun.objects.get(id=16)

data_dir = '../data/dec08/'

# load hier_institutions


institutions = open(data_dir + 'bank_rss', 'r')

for institution in institutions.readlines():
    
    institution_parts = institution.strip().split(' ')
    
    fdic_cert = int(institution_parts[0].strip())
    fed_rss = int(institution_parts[1].strip())
   
    
    try:
        
        bank = Institution.objects.get(fdic_number=fdic_cert)
        
        
        if bank.parent_institution == None:
            
            try:
                
          
                bank.parent_institution = Institution.objects.get(fed_number=fed_rss)
                bank.save()
              
            except Institution.DoesNotExist:
                
                if bank.fed_number == None:
                    bank.fed_number = fed_rss
                    bank.save()
                else:
                    print "fed mismatch for: %d (%d/%d)" % (fdic_cert, fed_rss, bank.fed_number)
        else:
            
            
            
            try:
                
                existing_parent_institution = Institution.objects.get(fed_number=fed_rss)
                
                if existing_parent_institution != bank.parent_institution:
                    
                    if bank.fed_number == None:
                
                        bank.fed_number = fed_rss
                        bank.save()
                    
                    else:
                        print "parent mismatch for: %d (%d/%d)" % (fdic_cert, fed_rss, bank.parent_institution.fed_number)
            
            except Institution.DoesNotExist:
            
                if bank.fed_number == None:
                    bank.fed_number = fed_rss
                    bank.save()
                    
                else:  
                    print "fed not found for: %d (%d)" % (fdic_cert, fed_rss)
            
    
    except:
        
        print 'cert not found: %d' % (fdic_cert)
        
        
   
   