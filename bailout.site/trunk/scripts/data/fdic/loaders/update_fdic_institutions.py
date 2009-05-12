#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from bailout.models import * 
from etl.models import *
from django.core.exceptions import ObjectDoesNotExist

fdic_datarun = DataRun.objects.get(id=16)

data_dir = '../data/dec08/'

# load hier_institutions


hier_institutions = open(data_dir + 'hier_institutions', 'r')

for institution in hier_institutions.readlines():
    
    institution_parts = institution.strip().split('\t')
    
    fdic_holding_co_id = int(institution_parts[0].strip())
    
    if len(institution_parts) == 9:
        
        fdic_cert_id = int(institution_parts[1].strip())
        
        institution_type = institution_parts[6]
        
        try:
            holding_institution = Institution.objects.get(fdic_number=fdic_holding_co_id)
            
            try:
                bank_institution = Institution.objects.get(fdic_number=fdic_cert_id)
                
                if bank_institution.parent_institution != holding_institution:
                  
                    bank_institution.parent_institution = holding_institution
                    bank_institution.save()
                    
                    print 'parent changed: %d' % fdic_cert_id
                    
            except ObjectDoesNotExist: 
                
                Institution.objects.create(fdic_number=fdic_cert_id,
                                           parent_institution=holding_institution,
                                           name=institution_parts[2],
                                           type_of_institution='bank',
                                           city=institution_parts[3],
                                           state=institution_parts[5],
                                           total_deposits=institution_parts[7],
                                           total_assets=institution_parts[8], 
                                           datarun=fdic_datarun)
                
                print str(fdic_holding_co_id) + ' bank created'
        except:
             print str(fdic_holding_co_id) + ' missing'
        
    elif len(institution_parts) == 8:
        
        institution_type = institution_parts[5]
        
        try:
            holding_institution = Institution.objects.get(fdic_number=fdic_holding_co_id)
#            print str(fdic_holding_co_id) + ' bhc exists'
        except ObjectDoesNotExist:
            Institution.objects.create(fdic_number=fdic_holding_co_id,
                                       name=institution_parts[2],
                                       type_of_institution='holding company',
                                       city=institution_parts[3],
                                       state=institution_parts[4],
                                       total_deposits=institution_parts[6],
                                       total_assets=institution_parts[7], 
                                       datarun=fdic_datarun)
            print str(fdic_holding_co_id) + ' bhc created'
            
hier_institutions.close()          
            
         