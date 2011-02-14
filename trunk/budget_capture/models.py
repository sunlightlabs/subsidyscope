from django.db import models

from cfda.models import ProgramDescription 
from django.contrib.auth.models import User

class Task(models.Model):
    
    name = models.CharField(max_length=255)
    
    description = models.TextField()
    
    def __unicode__(self):
        return self.name
    
    
class Item(models.Model):
    
    task = models.ForeignKey(Task)
    
    cfda_program = models.ForeignKey(ProgramDescription)
    
    def __unicode__(self):
        return str(self.cfda_program.program_number)
    

class BudgetData(models.Model):

    item = models.ForeignKey(Item, editable=False)
    
    user = models.ForeignKey(User, editable=False)
    
    notes = models.TextField("Notes", blank=True)
    
    

class BudgetDataFiscalYear(models.Model):
    
    budget_data = models.ForeignKey(BudgetData, editable=False)
    
    
       
    fiscal_year = models.IntegerField("Fiscal Year")
    
    amount = models.DecimalField("Amount", max_digits=15, decimal_places=2)

    
    DATA_TYPE_AUTHORIZATION = 1
    DATA_TYPE_APPROPRIATION = 2
    DATA_TYPE_OBLIGATION = 3
    DATA_TYPE_ALLOCATION_APPORTIONMENT = 4
    DATA_TYPE_OTHER = 5
    
    DATA_TYPE_CHOICES = (
        (DATA_TYPE_AUTHORIZATION, 'Authorization'),
        (DATA_TYPE_APPROPRIATION, 'Appropriation'),
        (DATA_TYPE_OBLIGATION, 'Obligation'),
        (DATA_TYPE_ALLOCATION_APPORTIONMENT, 'Allocation/Apportionment'),
        (DATA_TYPE_OTHER, 'Other'))

    data_type = models.IntegerField("Data type", choices=DATA_TYPE_CHOICES)
    
    DATA_SOURCE_AGENCY = 1
    DATA_SOURCE_LEGISLATION = 2
    DATA_SOURCE_APPORTIONMENT_NOTICE = 3
    DATA_SOURCE_CFDA = 4
    DATA_SOURCE_OTHER = 5
    
    DATA_SOURCE_CHOICES = (
        (DATA_SOURCE_AGENCY, 'Agency'),
        (DATA_SOURCE_LEGISLATION, 'Legislation'),
        (DATA_SOURCE_APPORTIONMENT_NOTICE, 'Apportionment Notice'),
        (DATA_SOURCE_CFDA, 'CFDA'),
        (DATA_SOURCE_OTHER, 'Other'))
    
    data_source = models.IntegerField("Data source", choices=DATA_SOURCE_CHOICES)
    
    
    citation = models.CharField("Data citation (URL)", max_length=200, blank=True)
    
    transactional_data_available = models.CharField("Transactional data (URL)", max_length=200, blank=True)
        