from django.db import models
from sectors.models import Sector, Subsector



class JCTCategory(models.Model):
    
    parent = models.ForeignKey('self', null=True)
    
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name
    

class JCTExpenditure(models.Model):
    
    category = models.ForeignKey(JCTCategory)
    
    name = models.CharField(max_length=500)
    match_name = models.CharField(max_length=500)
    
    description = models.TextField()

    def __unicode__(self):
        return self.name


    def get_estimates(self):
        
        estimate_years = {}
        
        most_recent_estimate_years = {}
        
        for estimate in JCTExpenditureEstimate.objects.filter(expenditure=self):
        
            if not estimate_years.has_key(estimate.estimate_year):
                
                estimate_years[estimate.estimate_year] = {}
            
            estimate_years[estimate.estimate_year][estimate.analysis_year] = estimate
    
    
        for estimate_year in estimate_years:
            
            analysis_years = estimate_years[estimate_year].keys()
            
            most_recent_analysis_year = max(analysis_years)
            
            estimate = estimate_years[estimate_year][most_recent_analysis_year]
            
            most_recent_estimate_years[estimate_year] = estimate
        
        years = most_recent_estimate_years.keys()
        years.sort()
        
        corporations = []
        
        for year in years:
            corporations.append(int(most_recent_estimate_years[year].corporations_amount * 1000))
            
        individuals = []
        
        for year in years:
            individuals.append(int(most_recent_estimate_years[year].individuals_amount * 1000))
        
        totals_list = [corporations, individuals]
        totals = map(sum, zip(*totals_list))
        
        results = {}
        
        results['years'] = years 
        results['corporations'] = corporations
        results['individuals'] = individuals
        results['totals'] = totals

        return results


class JCTExpenditureGroup(models.Model):
    
    group = models.ManyToManyField(JCTExpenditure)
    
    name = models.CharField(max_length=500)
    

    

class JCTExpenditureEstimate(models.Model):
    
    expenditure = models.ForeignKey(JCTExpenditure)
    
    NOTE_CHOICES = (
        (1, 'Positive tax expenditure of less than $50 million.'),
        (2, 'Negative tax expenditure of less than $50 million.')
    )
    
    # year when analysis was performed/published in ESTIMATES OF FEDERAL TAX EXPENDITURES
    analysis_year = models.IntegerField()
    
    # year estimate is for
    estimate_year = models.IntegerField()
    
    
    corporations_amount = models.DecimalField(max_digits=15, decimal_places=2)
    individuals_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    corporations_notes = models.IntegerField(choices=NOTE_CHOICES, null=True)
    individuals_notes = models.IntegerField(choices=NOTE_CHOICES, null=True)
    



class OMBCategory(models.Model):
    
    parent = models.ForeignKey('self', null=True)
    
    name = models.CharField(max_length=255)
    

class OMBExpenditure(models.Model):
    
    category = models.ForeignKey(OMBCategory)
    
    name = models.CharField(max_length=255)
    match_name = models.CharField(max_length=255)
    
    description = models.TextField()
    
    
    def get_estimates(self):
        
        estimate_years = {}
        
        most_recent_estimate_years = {}
        
        for estimate in OMBExpenditureEstimate.objects.filter(expenditure=self):
        
            if not estimate_years.has_key(estimate.estimate_year):
                
                estimate_years[estimate.estimate_year] = {}
            
            estimate_years[estimate.estimate_year][estimate.analysis_year] = estimate
    
    
        for estimate_year in estimate_years:
            
            analysis_years = estimate_years[estimate_year].keys()
            
            most_recent_analysis_year = max(analysis_years)
            
            estimate = estimate_years[estimate_year][most_recent_analysis_year]
            
            most_recent_estimate_years[estimate_year] = estimate
        
        years = most_recent_estimate_years.keys()
        years.sort()
        
        corporations = []
        
        for year in years:
            corporations.append(int(most_recent_estimate_years[year].corporations_amount))
            
        individuals = []
        
        for year in years:
            individuals.append(int(most_recent_estimate_years[year].individuals_amount))
        
        totals_list = [corporations, individuals]
        totals = map(sum, zip(*totals_list))
        
        results = {}
        
        results['years'] = years 
        results['corporations'] = corporations
        results['individuals'] = individuals
        results['totals'] = totals

        return results
  
  
class OMBExpenditureEstimate(models.Model):
    
    # year when analysis was performed/published in ESTIMATES OF FEDERAL TAX EXPENDITURES
    analysis_year = models.IntegerField()
    
    # year estimate is for
    estimate_year = models.IntegerField()
    
    corporations_amount = models.DecimalField(max_digits=15, decimal_places=2)
    individuals_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    expenditure = models.ForeignKey(OMBExpenditure)
    



class TaxExpenditureCategory(models.Model):
    
    parent = models.ForeignKey('self', null=True)
    
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name
    
    def recurse_subcategories(self):
        
        subcategories = []
        
        for category in self.taxexpenditurecategory_set.all():
            
            subcategories.append(category.recurse_subcategories())
            
           
class TaxExpenditure(models.Model):
    
    sector = models.ForeignKey(Sector, null=True)
    subsector = models.ForeignKey(Subsector, null=True)
    
    category = models.ForeignKey(TaxExpenditureCategory)
    
    name = models.CharField(max_length=500)
    match_name = models.CharField(max_length=500)
    
    jct_estimate = models.ForeignKey(JCTExpenditure, null=True)
    omb_estimate = models.ForeignKey(OMBExpenditure, null=True)
    


    
    
    
    
    