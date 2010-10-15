from django.db import models
from cube import Cube
        

class Category(models.Model):
    
    parent = models.ForeignKey('self', null=True)
    
    name = models.TextField()

    budget_function = models.BooleanField(default=False)

    def aggregate(self):
    
        total = Cube()

        for expenditure_group in self.budget_function_category_group_set.all():
            total += expenditure_group.aggregate()
            
        return total

    def __unicode__(self):
        return self.name

    
class Expenditure(models.Model):
    
    SOURCE_JCT = 1
    SOURCE_TREASURY = 2
    
    SOURCE_CHOICES = (
        (SOURCE_JCT, 'JCT'),
        (SOURCE_TREASURY, 'Treasury')
    )
    
    source = models.IntegerField(choices=SOURCE_CHOICES)
    
    category = models.ForeignKey(Category)
    
    budget_function_category = models.ManyToManyField(Category, related_name='budget_function_category_expenditure_set')
    
    item_number = models.IntegerField(null=True)
    
    name = models.TextField()
    
    match_name = models.TextField()
    
    analysis_year = models.IntegerField()
    
    description = models.TextField()
    
    notes = models.TextField()
        
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        
        ordering = ('analysis_year',)

# from tax_expenditures.models import *
# ExpenditureGroup.objects.group_expenditures()
 
class ExpenditureGroupManager(models.Manager):
    
    def group_expenditures(self):
        
        for expenditure in Expenditure.objects.all():
            
            group, created = self.get_or_create(match_name=expenditure.match_name, category=expenditure.category)
            
            if created:
                for category in expenditure.budget_function_category.all():
                    group.budget_function_category.add(category)
                
                group.name = expenditure.name
                group.type = ExpenditureGroup.TYPE_NAME
                group.save()
            
            group.group.add(expenditure)
            
    
class ExpenditureGroup(models.Model):
    
    TYPE_NAME = 1
    TYPE_MANUAL = 2
  
    TYPE_CHOICES = (
        (TYPE_NAME, 'Name'),
        (TYPE_MANUAL, 'Manual')
    )
    
    type = models.IntegerField(choices=TYPE_CHOICES, null=True)
    
    category = models.ForeignKey(Category, null=True)
    
    budget_function_category = models.ManyToManyField(Category, related_name='budget_function_category_group_set')
    
    name = models.TextField()
    
    match_name = models.TextField()
    
    group = models.ManyToManyField(Expenditure)
    
    objects = ExpenditureGroupManager()
    
    def get_description(self):
        
        try:
            expenditure = self.group.filter(source=Expenditure.SOURCE_TREASURY).exclude(description='').order_by('-analysis_year')[0]
        
            return '<strong>Description from the %d Analytical Perspectives:</strong> %s'  % (expenditure.analysis_year, expenditure.description)
            
        except:
            return ''
                
    
    
    def aggregate(self):
        
        cube = Cube()
        
        estimates = {}
        
        for expenditure in self.group.filter(source=Expenditure.SOURCE_JCT):
            for estimate in expenditure.estimate_set.all():
                estimates[estimate.estimate_year] = estimate
        
        for year in estimates:
            
            estimate = estimates[year]
            
            if estimate.corporations_amount != None:
                cube.add({'year':estimate.estimate_year, 'source':expenditure.source, 'recipient':'corporation'}, estimate.corporations_amount)
            if  estimate.individuals_amount != None:
                cube.add({'year':estimate.estimate_year, 'source':expenditure.source, 'recipient':'individual'}, estimate.individuals_amount)
        
        for expenditure in self.group.filter(source=Expenditure.SOURCE_TREASURY):
            for estimate in expenditure.estimate_set.all():
                estimates[estimate.estimate_year] = estimate
        
        for year in estimates:
            
            estimate = estimates[year]
            
            if estimate.corporations_amount != None:
                cube.add({'year':estimate.estimate_year, 'source':expenditure.source, 'recipient':'corporation'}, estimate.corporations_amount)
            if  estimate.individuals_amount != None:
                cube.add({'year':estimate.estimate_year, 'source':expenditure.source, 'recipient':'individual'}, estimate.individuals_amount)
            
            
        return cube
    
        
    def __unicode__(self):
        return self.name
    
    
class Estimate(models.Model):
    
    expenditure = models.ForeignKey(Expenditure)
    
    estimate_year = models.IntegerField()

    notes = models.TextField()
    
    corporations_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    individuals_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    NOTE_CHOICES = (
        (1, 'Positive tax expenditure of less than $50 million.'),
        (2, 'Negative tax expenditure of less than $50 million.')
    )
    
    corporations_notes = models.IntegerField(choices=NOTE_CHOICES, null=True)
    individuals_notes = models.IntegerField(choices=NOTE_CHOICES, null=True)
    

    def __unicode__(self):
        return '' % ()
    
    class Meta:
        
        ordering = ('estimate_year',)    