from django.db import models


class StateMatcher():
    
    # for bulk matching in memory
    
    name_list = {}
    abbreviation_list = {}
    fips_list = {}
    
    def __init__(self):
        
        for state in State.objects.all():
            
            self.name_list[state.name.lower()] = state
            self.abbreviation_list[state.abbreviation.lower()] = state
            self.fips_list[state.fips_state_code] = state
            
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
 

class CountyMatcher():
    
    pass
 
class CountyManager(models.Manager):
    
    def matchCounty(self, county, state):
        
        state = State.objects.matchState(state)
        
        if state:
            
            
            self.get(state=state, )
            
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
