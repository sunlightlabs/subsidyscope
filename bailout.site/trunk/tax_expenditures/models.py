from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from cube import Cube

TE_CURRENT_YEAR = 2011
TE_YEARS = range(2000,2016)
         
    
class Group(models.Model):
    
    parent = models.ForeignKey('self', null=True)
    
    name = models.TextField()
    
    description = models.TextField()
    
    notes = models.TextField()
    
    def calc_summary(self):
        
        self.groupsummary_set.all().delete()
        
        cube = Cube()
        
        for group in Group.objects.filter(parent=self):
            cube += group.calc_summary()
            
        
        for expenditure in self.expenditure_set.all():            
            
            if expenditure.analysis_year < TE_CURRENT_YEAR:
                
                try:
                    estimate = Estimate.objects.get(expenditure=expenditure, estimate_year=expenditure.analysis_year-2)
                    
                    cube.add({'source':expenditure.source, 'estimate_year':estimate.estimate_year, 'estimate':GroupSummary.ESTIMATE_CORPORATIONS}, estimate.corporations_amount)
                    cube.add({'source':expenditure.source, 'estimate_year':estimate.estimate_year, 'estimate':GroupSummary.ESTIMATE_INDIVIDUALS}, estimate.individuals_amount)
                    
                except ObjectDoesNotExist:
                    pass
                     
            elif expenditure.analysis_year == TE_CURRENT_YEAR:
                
                for year in range(TE_CURRENT_YEAR-2, TE_CURRENT_YEAR + 5):
                    
                    try:
                        estimate = Estimate.objects.get(expenditure=expenditure, estimate_year=year)
                        
                        cube.add({'source':expenditure.source, 'estimate_year':estimate.estimate_year, 'estimate':GroupSummary.ESTIMATE_CORPORATIONS}, estimate.corporations_amount)
                        cube.add({'source':expenditure.source, 'estimate_year':estimate.estimate_year, 'estimate':GroupSummary.ESTIMATE_INDIVIDUALS}, estimate.individuals_amount)
                    
                        
                    except ObjectDoesNotExist:
                        pass 
        
        for estimate_year in TE_YEARS:
            
            if cube.dimensions.has_key('estimate_year') and cube.dimensions['estimate_year'].values.has_key(estimate_year):
            
                results_corp = cube.query(attributes={'estimate_year':estimate_year, 'estimate':GroupSummary.ESTIMATE_CORPORATIONS}, groups=['source'])
                results_indv = cube.query(attributes={'estimate_year':estimate_year, 'estimate':GroupSummary.ESTIMATE_INDIVIDUALS}, groups=['source'])
                results_comb = cube.query(attributes={'estimate_year':estimate_year}, groups=['source'])
            
                if cube.dimensions.has_key('source') and cube.dimensions['source'].values.has_key(Expenditure.SOURCE_JCT):
                    summary_corp = GroupSummary.objects.create(group=self, source=Expenditure.SOURCE_JCT, estimate_year=estimate_year, estimate=GroupSummary.ESTIMATE_CORPORATIONS)
                    summary_corp.amount = results_corp.values[Expenditure.SOURCE_JCT].get_data(aggregator=sum)
                    summary_corp.save()
                   
                    summary_indv = GroupSummary.objects.create(group=self, source=Expenditure.SOURCE_JCT, estimate_year=estimate_year, estimate=GroupSummary.ESTIMATE_INDIVIDUALS)
                    summary_indv.amount = results_indv.values[Expenditure.SOURCE_JCT].get_data(aggregator=sum)
                    summary_indv.save()
                   
                    summary_comb = GroupSummary.objects.create(group=self, source=Expenditure.SOURCE_JCT, estimate_year=estimate_year, estimate=GroupSummary.ESTIMATE_COMBINED)
                    summary_comb.amount = results_comb.values[Expenditure.SOURCE_JCT].get_data(aggregator=sum)
                    summary_comb.save()
                
                
                if cube.dimensions.has_key('source') and cube.dimensions['source'].values.has_key(Expenditure.SOURCE_TREASURY):
                    summary_corp = GroupSummary.objects.create(group=self, source=Expenditure.SOURCE_TREASURY, estimate_year=estimate_year, estimate=GroupSummary.ESTIMATE_CORPORATIONS)
                    summary_corp.amount = results_corp.values[Expenditure.SOURCE_TREASURY].get_data(aggregator=sum)
                    summary_corp.save()
                    
                    summary_indv = GroupSummary.objects.create(group=self, source=Expenditure.SOURCE_TREASURY, estimate_year=estimate_year, estimate=GroupSummary.ESTIMATE_INDIVIDUALS)
                    summary_indv.amount = results_indv.values[Expenditure.SOURCE_TREASURY].get_data(aggregator=sum)
                    summary_indv.save()
                    
                    summary_comb = GroupSummary.objects.create(group=self, source=Expenditure.SOURCE_TREASURY, estimate_year=estimate_year, estimate=GroupSummary.ESTIMATE_COMBINED)
                    summary_comb.amount = results_comb.values[Expenditure.SOURCE_TREASURY].get_data(aggregator=sum)
                    summary_comb.save()
        
        return cube
        
    def __unicode__(self):
        return self.name
    
    class Meta:
        
        ordering = ('name',)
        
        

class GroupSummary(models.Model):

    group = models.ForeignKey(Group)

    SOURCE_JCT = 1
    SOURCE_TREASURY = 2
    
    SOURCE_CHOICES = (
        (SOURCE_JCT, 'JCT'),
        (SOURCE_TREASURY, 'Treasury')
    )
    
    source = models.IntegerField(choices=SOURCE_CHOICES)
    
    ESTIMATE_CORPORATIONS = 1
    ESTIMATE_INDIVIDUALS = 2
    ESTIMATE_COMBINED = 3
    
    ESTIMATE_CHOICES = (
        (ESTIMATE_CORPORATIONS, 'Corporations'),
        (ESTIMATE_INDIVIDUALS, 'Individuals'),
        (ESTIMATE_COMBINED, 'Corporations & Individuals')
    )
    
    estimate = models.IntegerField(choices=ESTIMATE_CHOICES)
    
    estimate_year = models.IntegerField()
    
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    class Meta:
        
        ordering = ('estimate_year',)


class Expenditure(models.Model):
    
    SOURCE_JCT = 1
    SOURCE_TREASURY = 2
    
    SOURCE_CHOICES = (
        (SOURCE_JCT, 'JCT'),
        (SOURCE_TREASURY, 'Treasury')
    )
    
    group = models.ForeignKey(Group)
    
    source = models.IntegerField(choices=SOURCE_CHOICES)
    
    item_number = models.IntegerField(null=True)
    
    name = models.TextField()
    
    analysis_year = models.IntegerField()
    
    description = models.TextField()
    
    notes = models.TextField()
        
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        
        ordering = ('analysis_year',)

    
class Estimate(models.Model):
    
    expenditure = models.ForeignKey(Expenditure)
    
    estimate_year = models.IntegerField()

    notes = models.TextField()
    
    corporations_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    individuals_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    NOTE_POSITIVE = 1
    NOTE_NEGATIVE = 2
    
    NOTE_CHOICES = (
        (NOTE_POSITIVE, 'Positive tax expenditure of less than $50 million.'),
        (NOTE_NEGATIVE, 'Negative tax expenditure of less than $50 million.')
    )
    
    corporations_notes = models.IntegerField(choices=NOTE_CHOICES, null=True)
    individuals_notes = models.IntegerField(choices=NOTE_CHOICES, null=True)
    

    def __unicode__(self):
        return '' % ()
    
    class Meta:
        
        ordering = ('estimate_year',)    