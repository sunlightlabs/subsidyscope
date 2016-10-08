from django.db import models

from cfda.models import ProgramDescription



class CFDASummaryManager(models.Manager):
    
    def load_summary_data(self):
        
        program_lookup = {}
        
        for program in ProgramDescription.objects.all():
            program_lookup[program.program_number] = program
        
        import psycopg2
        conn = psycopg2.connect("dbname=test user=test password=test host=localhost")

        cur = conn.cursor()
        
        cur.execute('select fiscal_year, cfda_program_num, assistance_type, sum(fed_funding_amount) from grants_grant group by fiscal_year, cfda_program_num, assistance_type;')
        
        for record in cur:
            
            try:
                self.create(fiscal_year=record[0], program=program_lookup[record[1]], assistance_type=match_assitance_type(record[2]), federal_funding_amount=record[3  ]) 
            except:
                print "Can't save summary for %s (%d)." % (record[1], record[0])
            
            

class CFDASummary(models.Model):
    
    ASSISTANCE_TYPE_CHOICES = (                       
        (3, "Formula Grants"),
        (4, "Project Grants"),
        (6, "Direct Payments for Specified Use"),
        (10, "Direct Payments with Unrestricted Use"),
        (11, "Other"),
        (7, "Direct Loans"),
        (8, "Guaranteed/Insured Loans"),
        (9, "Insurance"),
        (5, "Cooperative Agreements"),
        (2, "Block Grants"),
    )
    
    program = models.ForeignKey(ProgramDescription)
    fiscal_year = models.IntegerField()
    assistance_type =models.IntegerField(choices=ASSISTANCE_TYPE_CHOICES)
    
    federal_funding_amount = models.DecimalField("Total Funding Amount", max_digits=15, decimal_places=2, blank=True, null=True)
    
    #data_load = models.ForeignKey()
    
    objects = CFDASummaryManager()

    
def match_assitance_type(type_code):
    
    code_int = int(type_code)
    
    for choice in CFDASummary.ASSISTANCE_TYPE_CHOICES:
        if code_int == choice[0]:
            return choice[0]
    
    print "Can't match code %s." % type_code
       
    return None
