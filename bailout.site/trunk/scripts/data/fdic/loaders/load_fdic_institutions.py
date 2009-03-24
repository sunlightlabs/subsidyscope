#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from bailout.models import * 
from etl.models import *
from django.core.exceptions import ObjectDoesNotExist

fdic_datarun = DataRun.objects.get(id=16)

data_dir = '../data/sept08/'

# load hier_institutions


hier_institutions = open(data_dir + 'hier_institutions', 'r')

for institution in hier_institutions.readlines():
    
    institution_parts = institution.strip().split('\t')
    
    fdic_holding_co_id = int(institution_parts[0].strip())
    
    if len(institution_parts) == 9:
        
        fdic_cert_id = int(institution_parts[1].strip())
        
        institution_type = institution_parts[6]
        
        try:
            bank_institution = Institution.objects.get(fdic_number=fdic_cert_id)
            print str(fdic_cert_id) + ' bank exists'
        except ObjectDoesNotExist: 
            
            if holding_institution.fdic_number != fdic_holding_co_id:
                holding_institution = Institution.objects.get(fdic_number=fdic_holding_co_id)
            
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
        
        
    elif len(institution_parts) == 8:
        
        institution_type = institution_parts[5]
        
        try:
            holding_institution = Institution.objects.get(fdic_number=fdic_holding_co_id)
            print str(fdic_holding_co_id) + ' bhc exists'
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
            
            
# load institutions

institutions = open(data_dir + 'institutions', 'r')

for institution in institutions.readlines():
    
    institution_parts = institution.strip().split('\t')
    
    fdic_cert_id = int(institution_parts[0].strip())
    
    if institution_parts[2].strip() == 'FED':
        regulator = 'Federal Reserve'
    elif institution_parts[2].strip() == 'FDIC':
        regulator = 'FDIC'
    elif institution_parts[2].strip() == 'OCC':
        regulator = 'Comptroller'
    elif institution_parts[2].strip() == 'OTS':
        regulator = 'Thrift'
    else:
        regulator = 'Other'
        
    try:
        institution = Institution.objects.get(fdic_number=fdic_cert_id)
        
        print str(fdic_cert_id) + ' bank exists'
        
        if institution.regulator == None:
            institution.regulator = regulator
            institution.save()
            print 'updated regulator'
        
        
    except ObjectDoesNotExist:
        
        location = institution_parts[4].split(',')
        city = location[0].strip()
        state = location[1].strip()
        
        Institution.objects.create(fdic_number=fdic_cert_id,
                                   name=institution_parts[3],
                                   type_of_institution='bank',
                                   city=city,
                                   state=state,
                                   regulator=regulator,
                                   total_assets=institution_parts[1], 
                                   datarun=fdic_datarun)
        print str(fdic_cert_id) + ' bank created'
