from django.db import models

class State(models.Model):

    name = models.CharField("Name", max_length=50)
    abbreviation = models.CharField("Name", max_length=2)
    
    fips_state_code = models.IntegerField()
 
 
class County(models.Model):

    name = models.CharField("Name", max_length=100)
    name_complete = models.CharField("Complete Name", max_length=100)
    
    state = models.IntegerField(null=True) # models.ForeignKey(State)
    
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
    
    
