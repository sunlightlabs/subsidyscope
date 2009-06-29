import re
from django.db import models
from django.db.models import Q


class StateMatcher():
    
    # for bulk matching in memory
    
    def __init__(self, match_counties=False):
        
        self.name_list = {}
        self.abbreviation_list = {}
        self.fips_list = {}
    
        self.county_matchers = {}
        
        for state in State.objects.all():
                
            self.name_list[state.name.lower()] = state
            self.abbreviation_list[state.abbreviation.lower()] = state
            self.fips_list[state.fips_state_code] = state
            
            if match_counties:
                
                self.county_matchers[state.id] = CountyMatcher(state)
            
            
    def matchName(self, state):
        
        state = state.lower()
        
        try:
            if len(state) == 2 and self.abbreviation_list.has_key(state):   
                return self.abbreviation_list[state]
                
            elif len(state) > 2 and self.name_list.has_key(state):
                return self.name_list[state]
            
            else:
                return False
        except:
            return False

    def matchFips(self, fips):
        
        try:
            
            if self.fips_list.has_key(fips):
                return self.fips_list[fips]
            else:
                return False
            
        except:
            return False
        
    def getCountyMatcher(self, state):
            
        if self.county_matchers.has_key(state.id):    
            return self.county_matchers[state.id]
        else: 
            return False
        
        
class StateManager(models.Manager): 
    
    def matchState(self, state):
        
        try:
            if len(state) == 2:
                return self.get(abbreviation__iexact=state)
            
            elif len(state) > 2:
                return self.get(name__iexact=state)
            
            else:
                return False
        except:
            return False
            

class State(models.Model):

    name = models.CharField("Name", max_length=50)
    abbreviation = models.CharField("Name", max_length=2)
    
    fips_state_code = models.IntegerField()
 
    objects = StateManager()

    def __unicode__(self):
        return self.name

class CountyMatcher():
    
    def __init__(self, state):
        
        self.name_list = {}
        self.name_complete_list = {}
        self.fips_list = {}
        
        self.state = state
        
        for county in County.objects.filter(state=state):
            
            self.name_list[county.name.lower()] = county
            self.name_complete_list[county.name_complete.lower()] = county
            self.fips_list[county.fips_county_code] = county
            
    def matchName(self, county):
        
        county = county.lower()
        county = county.replace('(city) county', 'city')
        
        # handling exceptions for errors in FDIC data - ick!
        
        if self.state.fips_state_code == 18: # Indiana
            county = county.replace('la porte', 'laporte')
        elif self.state.fips_state_code == 29: # Missouri
            county = county.replace('st. claire', 'st. clair')
        elif self.state.fips_state_code == 35: # New Mexico
            county = county.replace('debaca', 'de baca')
        
        try:
            if self.name_complete_list.has_key(county):   
                return self.name_complete_list[county]
                
            elif self.name_list.has_key(county.replace(' county', '')):
                return self.name_list[county.replace(' county', '')]
            
            else:
                return False
                
        except:
            return False

    def matchFips(self, fips):
        
        try:
            
            if self.fips_list.has_key(fips):
                return self.fips_list[fips]
            else:
                return False
            
        except:
            return False
 

class FAADSMatcher():
 
    def __init__(self):
        
        self.matcher = StateMatcher(match_counties=True)
    
    # matches FAADS principal_place_codes to state/county objects

    def matchPrincipalPlace(self, place_code):
        
        state = None
        county = None
        
        try:
            state_code = int(place_code[0:2])
            
            state = self.matcher.matchFips(state_code)
            
        except:
            state_code = None
        
        if state:
            
            try:    
                county_code = int(place_code[2:].strip('*'))
                
                county_matcher = self.matcher.getCountyMatcher(state)
                county = county_matcher.matchFips(county_code)
                
                if not county:
                    county = None
                
            except:
                pass
                
        return state, county 
    
        
    
        
        
class CountyManager(models.Manager):
    
    def matchCounty(self, county, state):
        
        state = State.objects.matchState(state)
        
        if state:
            county = county.lower()

            matches = self.filter(Q(state=state), Q(name=county) | Q(name_complete=county))
            
            if matches.count() == 1:
                return matches[0]
            else:
                return False
            
        else:
            return False

class County(models.Model):

    name = models.CharField("Name", max_length=100)
    name_complete = models.CharField("Complete Name", max_length=100)
    
    state = models.ForeignKey(State)
    
    LSAD_CHOICES = ((3, 'City and Borough'),
                    (4, 'Borough'),
                    (5, 'Census Area'),
                    (6, 'County'),
                    (7, 'District'),
                    (8, 'Independent City'), 
                    (9, 'Independent City (NV)'),
                    (10, 'Island (VI)'),
                    (11, 'Island (Samoa)'),
                    (12, 'Municipality'),
                    (13, 'Municipio'),
                    (14, 'County (DC & Guam)'),
                    (15, 'Parish'),
                    (25, 'City')) 
    
    lsad_code = models.IntegerField(choices=LSAD_CHOICES, null=True)
      
    fips_county_code = models.IntegerField(null=True)
    fips_full_code = models.IntegerField(null=True) # combined state/county fips code 
    
    ansi_code = models.IntegerField(null=True)
    
    csa_code = models.IntegerField(null=True) # combined statisical area
    cbsa_code = models.IntegerField(null=True) # core base statistical area (micro/metro areas)
    mdiv_code = models.IntegerField(null=True) # metro div area 
    
    objects = CountyManager()
    
    def __unicode__(self):
        return self.name
