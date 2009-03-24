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
    exact_amount = models.DecimalField("Amount ($millions)", max_digits=15, decimal_places=2, blank=True, null=True)
    range_low = models.DecimalField("Amount Range Low Bound ($millions)", max_digits=15, decimal_places=2, blank=True, null=True)
    range_high = models.DecimalField("Amount Range High Bound ($millions)", max_digits=15, decimal_places=2, blank=True, null=True)
    notes = models.CharField("Notes", max_length=255, blank=True, null=True)
    
    def grouping_hash(self):
        """gets the quarter, currently, for easy categorization in flex"""
        return "%d-%d" % (math.floor(self.closing_date.month / 4), self.closing_date.year)

    def get_exact_amount_or_range_average(self):        
        if self.exact_amount is None:
            return (self.range_low + self.range_high) / 2
        else:
            return self.exact_amount

class QBPSnapshot(models.Model):
    date = models.DateField("Date")
    problem_institutions = models.IntegerField(max_length=10, blank=True, null=True)
    reserve_ratio = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fund_balance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
            