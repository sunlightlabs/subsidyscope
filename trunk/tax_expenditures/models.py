from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from cube import Cube

TE_CURRENT_YEAR = 2012
TE_YEARS = range(2000,2017)
         
def te_sum(values):
    
    notes = False
    total = None
    groups = []
    expenditures = {}
    
    for value in values:
        
        if not value == None and not value['amount'] == None:
            if total == None:
                total = 0
            
            total += value['amount'] 
        
        if not value == None and value['notes']:
            notes = True
    
        if not value == None and value.has_key('group') and value['group']:
            groups.append(value['group'])
            
        if not value == None and value.has_key('expenditure') and value['expenditure']:
            expenditures[value['expenditure']] = True  
    
    if len(expenditures) == 1:
        expenditure, val = expenditures.popitem()
    else:
        expenditure = None
            
    return {'amount':total, 'notes':notes, 'groups':groups, 'expenditure':expenditure}


def create_detail_report_object(results, group, analysis_year, source):
    
    detail_report = GroupDetailReport.objects.create(group=group, source=source, analysis_year=analysis_year)
    
    result = results.values[source].get_data(aggregator=te_sum)
    
    for group_source in result['groups']:
        if group != group_source:
            detail_report.group_source.add(group)
        
    detail_report.expenditure_source = result['expenditure']
    
    detail_report.save()

def create_detail_object(results, group, estimate_year, analysis_year, source, estimate):
    
    detail = GroupDetail.objects.create(group=group, source=source, estimate_year=estimate_year, analysis_year=analysis_year, estimate=estimate)
    
    result = results.values[source].get_data(aggregator=te_sum)
        
    detail.amount = result['amount']
    detail.notes = result['notes']
    
    detail.save()
    
def create_summary_object(results, group, estimate_year, source, estimate):
    
    summary = GroupSummary.objects.create(group=group, source=source, estimate_year=estimate_year, estimate=estimate)
    
    result = results.values[source].get_data(aggregator=te_sum)
    
    summary.amount = result['amount']
    summary.notes = result['notes']
    summary.save()
 
    
class Group(models.Model):
    
    parent = models.ForeignKey('self', null=True)
    
    name = models.TextField()
    
    description = models.TextField()
    
    notes = models.TextField()
    
    def calc_detail(self):
        
        self.groupdetail_set.all().delete()
        
        cube = Cube()
        
        for group in Group.objects.filter(parent=self):
            cube += group.calc_detail()
        
        for expenditure in self.expenditure_set.all():
            for estimate in expenditure.estimate_set.all():
                cube.add({'source':expenditure.source, 'analysis_year':expenditure.analysis_year, 'estimate_year':estimate.estimate_year, 'estimate':GroupSummary.ESTIMATE_CORPORATIONS}, {'amount':estimate.corporations_amount, 'notes':estimate.corporations_notes, 'group':self, 'expenditure':expenditure})
                cube.add({'source':expenditure.source, 'analysis_year':expenditure.analysis_year, 'estimate_year':estimate.estimate_year, 'estimate':GroupSummary.ESTIMATE_INDIVIDUALS}, {'amount':estimate.individuals_amount, 'notes':estimate.individuals_notes, 'group':self, 'expenditure':expenditure})
                
        for analysis_year in TE_YEARS:
            
            if cube.dimensions.has_key('analysis_year') and cube.dimensions['analysis_year'].values.has_key(analysis_year):
                
                results_sources = cube.query(attributes={'analysis_year':analysis_year}, groups=['source'])
                
                if cube.dimensions.has_key('source') and cube.dimensions['source'].values.has_key(Expenditure.SOURCE_JCT):
                    create_detail_report_object(results_sources, self, analysis_year, Expenditure.SOURCE_JCT)
                    
                if cube.dimensions.has_key('source') and cube.dimensions['source'].values.has_key(Expenditure.SOURCE_TREASURY):
                    create_detail_report_object(results_sources, self, analysis_year, Expenditure.SOURCE_TREASURY)
            
            for estimate_year in TE_YEARS:
            
                if cube.dimensions.has_key('estimate_year') and cube.dimensions['estimate_year'].values.has_key(estimate_year) and cube.dimensions.has_key('analysis_year') and cube.dimensions['analysis_year'].values.has_key(analysis_year):
                    
                    results_corp = cube.query(attributes={'analysis_year':analysis_year, 'estimate_year':estimate_year, 'estimate':GroupSummary.ESTIMATE_CORPORATIONS}, groups=['source'])
                    results_indv = cube.query(attributes={'analysis_year':analysis_year, 'estimate_year':estimate_year, 'estimate':GroupSummary.ESTIMATE_INDIVIDUALS}, groups=['source'])
                    results_comb = cube.query(attributes={'analysis_year':analysis_year, 'estimate_year':estimate_year}, groups=['source'])
                
                    if cube.dimensions.has_key('source') and cube.dimensions['source'].values.has_key(Expenditure.SOURCE_JCT):
                        
                        create_detail_object(results_corp, self, estimate_year, analysis_year, Expenditure.SOURCE_JCT, GroupSummary.ESTIMATE_CORPORATIONS)
                        create_detail_object(results_indv, self, estimate_year, analysis_year, Expenditure.SOURCE_JCT, GroupSummary.ESTIMATE_INDIVIDUALS)
                        create_detail_object(results_comb, self, estimate_year, analysis_year, Expenditure.SOURCE_JCT, GroupSummary.ESTIMATE_COMBINED)
                        
                    if cube.dimensions.has_key('source') and cube.dimensions['source'].values.has_key(Expenditure.SOURCE_TREASURY):
                        
                        create_detail_object(results_corp, self, estimate_year, analysis_year, Expenditure.SOURCE_TREASURY, GroupSummary.ESTIMATE_CORPORATIONS)
                        create_detail_object(results_indv, self, estimate_year, analysis_year, Expenditure.SOURCE_TREASURY, GroupSummary.ESTIMATE_INDIVIDUALS)
                        create_detail_object(results_comb, self, estimate_year, analysis_year, Expenditure.SOURCE_TREASURY, GroupSummary.ESTIMATE_COMBINED)
                                  
        return cube
    
    
    def calc_summary(self):
        
        self.groupsummary_set.all().delete()
        
        cube = Cube()
        
        for group in Group.objects.filter(parent=self):
            cube += group.calc_summary()
            
        
        for expenditure in self.expenditure_set.all():            
            
            if expenditure.analysis_year < TE_CURRENT_YEAR:
                
                try:
                    estimate = Estimate.objects.get(expenditure=expenditure, estimate_year=expenditure.analysis_year-2)
                    
                    cube.add({'source':expenditure.source, 'analysis_year':expenditure.analysis_year, 'estimate_year':estimate.estimate_year, 'estimate':GroupSummary.ESTIMATE_CORPORATIONS}, {'amount':estimate.corporations_amount, 'notes':estimate.corporations_notes})
                    cube.add({'source':expenditure.source, 'analysis_year':expenditure.analysis_year, 'estimate_year':estimate.estimate_year, 'estimate':GroupSummary.ESTIMATE_INDIVIDUALS}, {'amount':estimate.individuals_amount, 'notes':estimate.individuals_notes})
                    
                except ObjectDoesNotExist:
                    pass
                     
            elif expenditure.analysis_year == TE_CURRENT_YEAR:
                
                for year in range(TE_CURRENT_YEAR-2, TE_CURRENT_YEAR + 5):
                    
                    try:
                        estimate = Estimate.objects.get(expenditure=expenditure, estimate_year=year)
                        
                        cube.add({'source':expenditure.source, 'analysis_year':expenditure.analysis_year, 'estimate_year':estimate.estimate_year, 'estimate':GroupSummary.ESTIMATE_CORPORATIONS}, {'amount':estimate.corporations_amount, 'notes':estimate.corporations_notes})
                        cube.add({'source':expenditure.source, 'analysis_year':expenditure.analysis_year, 'estimate_year':estimate.estimate_year, 'estimate':GroupSummary.ESTIMATE_INDIVIDUALS}, {'amount':estimate.individuals_amount, 'notes':estimate.individuals_notes})
                    
                        
                    except ObjectDoesNotExist:
                        pass 
        
        for estimate_year in TE_YEARS:
            
            if cube.dimensions.has_key('estimate_year') and cube.dimensions['estimate_year'].values.has_key(estimate_year):
            
                results_corp = cube.query(attributes={'estimate_year':estimate_year, 'estimate':GroupSummary.ESTIMATE_CORPORATIONS}, groups=['source'])
                results_indv = cube.query(attributes={'estimate_year':estimate_year, 'estimate':GroupSummary.ESTIMATE_INDIVIDUALS}, groups=['source'])
                results_comb = cube.query(attributes={'estimate_year':estimate_year}, groups=['source'])
            
                if cube.dimensions.has_key('source') and cube.dimensions['source'].values.has_key(Expenditure.SOURCE_JCT):
                    
                    create_summary_object(results_corp, self, estimate_year, Expenditure.SOURCE_JCT, GroupSummary.ESTIMATE_CORPORATIONS)
                    create_summary_object(results_indv, self, estimate_year, Expenditure.SOURCE_JCT, GroupSummary.ESTIMATE_INDIVIDUALS)
                    create_summary_object(results_comb, self, estimate_year, Expenditure.SOURCE_JCT, GroupSummary.ESTIMATE_COMBINED)
                    
                if cube.dimensions.has_key('source') and cube.dimensions['source'].values.has_key(Expenditure.SOURCE_TREASURY):
                    
                    create_summary_object(results_corp, self, estimate_year, Expenditure.SOURCE_TREASURY, GroupSummary.ESTIMATE_CORPORATIONS)
                    create_summary_object(results_indv, self, estimate_year, Expenditure.SOURCE_TREASURY, GroupSummary.ESTIMATE_INDIVIDUALS)
                    create_summary_object(results_comb, self, estimate_year, Expenditure.SOURCE_TREASURY, GroupSummary.ESTIMATE_COMBINED)
                    
        
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
    
    NOTE_POSITIVE = 1
    NOTE_NEGATIVE = 2
    
    NOTE_CHOICES = (
        (NOTE_POSITIVE, 'Positive tax expenditure of less than $50 million.'),
        (NOTE_NEGATIVE, 'Negative tax expenditure of less than $50 million.')
    )
    
    notes = models.IntegerField(choices=NOTE_CHOICES, null=True)
        
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


class GroupDetailReport(models.Model):

    group = models.ForeignKey(Group)

    SOURCE_JCT = 1
    SOURCE_TREASURY = 2
    
    SOURCE_CHOICES = (
        (SOURCE_JCT, 'JCT'),
        (SOURCE_TREASURY, 'Treasury')
    )
    
    source = models.IntegerField(choices=SOURCE_CHOICES)

    
    group_source = models.ManyToManyField(Group, related_name='group_source_set')
    expenditure_source = models.ForeignKey(Expenditure, null=True)
    
    analysis_year = models.IntegerField()
   
    class Meta:
        
        ordering = ('analysis_year',)



class GroupDetail(models.Model):

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
    
    NOTE_POSITIVE = 1
    NOTE_NEGATIVE = 2
    
    NOTE_CHOICES = (
        (NOTE_POSITIVE, 'Positive tax expenditure of less than $50 million.'),
        (NOTE_NEGATIVE, 'Negative tax expenditure of less than $50 million.')
    )
    
    notes = models.IntegerField(choices=NOTE_CHOICES, null=True)
        
    estimate_year = models.IntegerField()
    analysis_year = models.IntegerField()
    
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    class Meta:
        
        ordering = ('estimate_year',)
        



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