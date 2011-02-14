import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import re

from bailout.models import *
from geo.models import *


file = open('data/2007/hmda_counties', 'r')
lines = file.readlines()
file.close()

total_loan_count = 0
total_loan_amounts = 0

county_loan_counts = {}
county_loan_amounts = {}

for county in lines:
    
    county_parts = county.strip().split(',')
    
    try:
        state_fips = int(county_parts[0])
        county_fips = int(county_parts[1])
        loan_count = int(county_parts[2])
        loan_amount = int(county_parts[3])
        
        if not county_loan_counts.has_key(state_fips):
            county_loan_counts[state_fips] = {}
            county_loan_amounts[state_fips] = {}
            
        county_loan_counts[state_fips][county_fips] = Decimal(loan_count)
        county_loan_amounts[state_fips][county_fips] = Decimal(loan_amount * 1000)
        
        total_loan_count += Decimal(loan_count)
        total_loan_amounts += Decimal(loan_amount * 1000)
    except ValueError:
        pass
        #print county_parts

counties = {}

for county in County.objects.all():

    if not counties.has_key(county.state.fips_state_code):
        
        counties[county.state.fips_state_code] = {}
        
    counties[county.state.fips_state_code][county.fips_county_code] = county
    
    

for county in County.objects.all():
    
    state_fips = county.state.fips_state_code
    county_fips = county.fips_county_code

    if county_loan_counts.has_key(state_fips) and county_loan_counts[state_fips].has_key(county_fips):
        
        county = counties[state_fips][county_fips]
        
        loans = county_loan_counts[state_fips][county_fips]
        loan_amounts = county_loan_amounts[state_fips][county_fips]
        
        loans_percent = county_loan_counts[state_fips][county_fips] / total_loan_count
        loan_amounts_percent = county_loan_amounts[state_fips][county_fips] / total_loan_amounts
        
        try: 
            county_summary = CountySummary.objects.get(county=county)
        
            county_summary.loans = loans
            county_summary.loan_amounts = loan_amounts
    
            county_summary.loans_percent = loans_percent
            county_summary.loan_amounts_percent = loan_amounts_percent
            
            county_summary.save()
            
            
        except CountySummary.DoesNotExist:
            
            county_summary = CountySummary.objects.create(county=county,
                                                          loans = loans,
                                                          loan_amounts = loan_amounts,
                                                          loans_percent = loans_percent,
                                                          loan_amounts_percent = loan_amounts_percent)
            
        

    

file = open('data/tarp_hmda_ids', 'r')
lines = file.readlines()
file.close()

tarp_hmda_institutions = {}

institution_summaries = {}

for institution in lines:
    
    institution_parts = institution.strip().split(',')
    
    hmda_id = institution_parts[0]
    fed_id = int(institution_parts[1])
    
    tarp_hmda_institutions[hmda_id] = fed_id

    
    institution_summaries[fed_id] = {}
    institution_summaries[fed_id]['counties'] = {}
    institution_summaries[fed_id]['total_loans'] = 0
    institution_summaries[fed_id]['total_loan_amounts'] = 0
    

for tarp_institution in tarp_hmda_institutions.keys():

    fed_id = tarp_hmda_institutions[tarp_institution]

    try:
        file = open('data/2007/inst/%s' % (tarp_institution), 'r')
    
        while True:
        
            lines = file.readlines(1000)
            
            for line in lines:
                
                loan_parts = line.strip().split(',')
                
                try:
                    loan_amount = Decimal(int(loan_parts[0]) * 1000)
                    fips_state = int(loan_parts[1])
                    fips_county = int(loan_parts[2])
                    
                  
                    
                    if not institution_summaries[fed_id]['counties'].has_key(fips_state):
                        institution_summaries[fed_id]['counties'][fips_state] = {}
                    
                    if not institution_summaries[fed_id]['counties'][fips_state].has_key(fips_county):
                        institution_summaries[fed_id]['counties'][fips_state][fips_county] = {}
                        institution_summaries[fed_id]['counties'][fips_state][fips_county]['count'] = 0
                        institution_summaries[fed_id]['counties'][fips_state][fips_county]['amount'] = 0
                        
                    institution_summaries[fed_id]['counties'][fips_state][fips_county]['count'] += 1
                    institution_summaries[fed_id]['counties'][fips_state][fips_county]['amount'] += loan_amount
                    
                    institution_summaries[fed_id]['total_loans'] += 1
                    institution_summaries[fed_id]['total_loan_amounts'] += loan_amount
                except ValueError:
                    print loan_parts
               
            if not lines:
                break
        
        
        file.close()
    except IOError:
        print tarp_institution

for fed_id in institution_summaries.keys():
    
    institution = Institution.objects.get(fed_number=fed_id)
    
    for fips_state in institution_summaries[fed_id]['counties'].keys():
        for fips_county in institution_summaries[fed_id]['counties'][fips_state].keys():
            
            if counties.has_key(fips_state) and counties[fips_state].has_key(fips_county):
                county = counties[fips_state][fips_county]
                
                
                institution_loans = institution_summaries[fed_id]['counties'][fips_state][fips_county]['count']
                institution_loan_amounts = institution_summaries[fed_id]['counties'][fips_state][fips_county]['amount']
                
                loans_county_percent = Decimal(institution_summaries[fed_id]['counties'][fips_state][fips_county]['count']) / Decimal(county_loan_counts[fips_state][fips_county])
                loan_amounts_county_percent = Decimal(institution_summaries[fed_id]['counties'][fips_state][fips_county]['amount']) / Decimal(county_loan_amounts[fips_state][fips_county])
                
                loans_institution_percent = Decimal(institution_summaries[fed_id]['counties'][fips_state][fips_county]['count']) / Decimal(institution_summaries[fed_id]['total_loans'])
                loan_amounts_institution_percent = Decimal(institution_summaries[fed_id]['counties'][fips_state][fips_county]['amount']) / Decimal(institution_summaries[fed_id]['total_loan_amounts'])
                
                
                try:
                    summary = InstitutionCountySummary.objects.get(institution=institution, county=county)
                    
                    summary.institution_loans = institution_loans
                    summary.institution_loan_amounts = institution_loan_amounts
                    
                    summary.loans_county_percent = loans_county_percent
                    summary.loan_amounts_county_percent = loan_amounts_county_percent
                    
                    summary.loans_institution_percent = loans_institution_percent
                    summary.loan_amounts_institution_percent = loan_amounts_institution_percent
                    
                    summary.save()
                    
                
                except InstitutionCountySummary.DoesNotExist:
                    InstitutionCountySummary.objects.create(institution=institution, county=county,
                                                            institution_loans = institution_loans,
                                                            institution_loan_amounts = institution_loan_amounts,
                                                            loans_county_percent = loans_county_percent,
                                                            loan_amounts_county_percent = loan_amounts_county_percent,
                                                            loans_institution_percent = loans_institution_percent,
                                                            loan_amounts_institution_percent = loan_amounts_institution_percent )
            else:
                print '%d,%d' % (fips_state, fips_county)
        
        