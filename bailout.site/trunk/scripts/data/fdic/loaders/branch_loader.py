import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from bailout.models import *
from geo.models import *
  
from etl.models import *
from django.core.exceptions import ObjectDoesNotExist


state_matcher = StateMatcher(match_counties=True)

institutions = {}

for institution in Institution.objects.all():
    
    institutions[institution.fdic_number] = institution


branches = open('../data/sept08/branches', 'r')

for branch in branches.readlines():
    
    branch_parts = branch.strip().split('|')
    
    state = state_matcher.matchName(branch_parts[4])
    
    if state:
        
        county_matcher = state_matcher.getCountyMatcher(state)
        
        county = county_matcher.matchName(branch_parts[3])
        
        if county:
            
            fdic_number = int(branch_parts[0])
            
            if institutions.has_key(fdic_number):
                
                InstitutionBranch.objects.create(institution=institutions[fdic_number], 
                                         county=county, 
                                         address=branch_parts[1], 
                                         city=branch_parts[2], 
                                         zip=branch_parts[5], 
                                         service=int(branch_parts[6]),
                                         deposits=Decimal(branch_parts[9])*1000) 
                                         
                
                
            else:
                print "bad institution: %s" % branch_parts
            
        #else:
        #    print "bad county: %s" % branch_parts
            
    #else:
    #    print "bad state: %s" % branch_parts
    