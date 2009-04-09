#!/usr/bin/env python
import os
from datetime import date
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from bailout.models import * 
from etl.models import *
from django.core.exceptions import ObjectDoesNotExist

fdic_datarun = DataRun.objects.get(id=16)

report_date = date(2008, 12, 31)
crawl_date = date(2009, 3, 17)

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
            bank_institution = Institution.objects.get(fdic_number=fdic_cert_id)
            
            InstitutionAssetHistory.objects.create(institution=bank_institution,
                                       report_date=report_date,
                                       crawl_date=crawl_date,
                                       total_deposits=institution_parts[7],
                                       total_assets=institution_parts[8])       
                        
        except ObjectDoesNotExist: 
            print str(fdic_cert_id) + ' bank not found'
        
        
    elif len(institution_parts) == 8:
        
        institution_type = institution_parts[5]
        
        try:
            holding_institution = Institution.objects.get(fdic_number=fdic_holding_co_id)
            
            InstitutionAssetHistory.objects.create(institution=holding_institution,
                                       report_date=report_date,
                                       crawl_date=crawl_date,
                                       total_deposits=institution_parts[6],
                                       total_assets=institution_parts[7])   
        
        except ObjectDoesNotExist:

            print str(fdic_holding_co_id) + ' bhc not found'
            
hier_institutions.close()          
            
            
# load institutions
#
institutions = open(data_dir + 'institutions', 'r')

for institution in institutions.readlines():
    
    institution_parts = institution.strip().split('\t')
    
    fdic_cert_id = int(institution_parts[0].strip())
        
    try:
        institution = Institution.objects.get(fdic_number=fdic_cert_id)
        
        if institution.institutionassethistory_set.all().count() == 0:
            InstitutionAssetHistory.objects.create(institution=institution,
                                           report_date=report_date,
                                           crawl_date=crawl_date,
                                           total_deposits=None,
                                           total_assets=institution_parts[1])   
            
    except ObjectDoesNotExist:
    
        print str(fdic_cert_id) + ' bank not found'


institutions.close()