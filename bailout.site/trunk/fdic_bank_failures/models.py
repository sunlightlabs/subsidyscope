from django.db import models
import math

class BankFailure(models.Model):    
    
    def __unicode__(self):
        return '%s - %s' % (self.closing_date, self.name)
    class Meta:
        verbose_name = 'Bank Failure'
        ordering = ['-closing_date', 'name']    
        
    name = models.CharField("Name", max_length=50, blank=True, null=True)
    city = models.CharField("City", max_length=50, blank=True, null=True)
    state = models.CharField("State", max_length=5, blank=True, null=True)
    closing_date = models.DateField("Closing Date", blank=True, null=True)  
    updated_date = models.DateField("Updated Date", blank=True, null=True)      
    amount = models.DecimalField("Amount ($millions)", max_digits=15, decimal_places=2, blank=True, null=True)
    notes = models.CharField("Notes", max_length=255, blank=True, null=True)
    
    def grouping_hash(self):
        """gets the quarter, currently, for easy categorization in flex"""
        return "%d-%d" % (math.floor(self.closing_date.month / 4), self.closing_date.year)

