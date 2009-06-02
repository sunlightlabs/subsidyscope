from django.db import models
import sectors.models

class TaxExpenditure():
    
    pass

class TaxExpenditureEstimate(models.Model):

    # year when analysis was performed/published in ESTIMATES OF FEDERAL TAX EXPENDITURES
    analysis_year = models.IntegerField()
    
    # year estimate is for
    estimate_year = models.IntegerField()
    
    corporations_amount = models.DecimalField(max_digits=15, decimal_places=2)
    individuals_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    class Meta:
        abstract = True



class JCTCategory(models.Model):
    
    parent = models.ForeignKey('self')
    
    name = models.CharField(max_length=255)
    

class JCTExpenditure(models.Model):
    
    category = models.ForeignKey(JCTCategory)
    
    name = models.CharField(max_length=255)
    
    description = models.TextField()
    
    

class JCTExpenditureEstimate(TaxExpenditureEstimate):
    
    expenditure = models.ForeignKey(JCTExpenditure)
    
    NOTE_CHOICES = (
        (1, 'Positive tax expenditure of less than $50 million.'),
        (2, 'Negative tax expenditure of less than $50 million.')
    )
    
    corporations_notes = models.IntegerField(choices=NOTE_CHOICES)
    individuals_notes = models.IntegerField(choices=NOTE_CHOICES)
    

class OMBCategory(models.Model):
    
    parent = models.ForeignKey('self', null=True)
    
    name = models.CharField(max_length=255)
    

class OMBExpenditure(models.Model):
    
    category = models.ForeignKey(OMBCategory)
    
    name = models.CharField(max_length=255)
    match_name = models.CharField(max_length=255)
    
    description = models.TextField()
  
  
class OMBExpenditureEstimate(TaxExpenditureEstimate):
    
    expenditure = models.ForeignKey(OMBExpenditure)
    
    
    
    
    
    