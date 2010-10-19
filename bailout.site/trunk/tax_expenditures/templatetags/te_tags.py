from morsels.models import Morsel, Page
from django.template import Library, Node, Variable
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Template
from django.template.loader import render_to_string

from tax_expenditures.models import Group, GroupSummary, TE_YEARS

register = Library()


@register.tag
def te_breadcrumb(parser, token):
    
    tag, group, estimate_type = token.split_contents()

    return TEBreadcrumb(group, estimate_type)

class TEBreadcrumb(Node):
    
    def __init__(self, group, estimate_type):
        
        self.group_token = Variable(group)
        self.estimate_type_token = Variable(estimate_type)
    
    def render(self, context):
        
        group = self.group_token.resolve(context)
        
        estimate_type = int(self.estimate_type_token.resolve(context))
        if estimate_type:
            estimate = int(estimate_type)

        list = []
        list.append(group)
        while group.parent:
            group = group.parent
            list.append(group)
        
        list.reverse()

        return render_to_string('tax_expenditures/te_breadcrumb.html', {'list':list, 'estimate_type':estimate_type})

@register.tag
def te_expenditure_detail(parser, token):
    
    tag, expenditure, estimate_type = token.split_contents()
    
    return TEEpenditureDetailNode(expenditure, estimate_type)

class TEEpenditureDetailNode(Node):
    
    def __init__(self, expenditure, estimate_type):
        
        self.expenditure_token = Variable(expenditure)
        self.estimate_type_token = Variable(estimate_type)
    
    def render(self, context):
        
        expenditure = self.expenditure_token.resolve(context)
        
        estimate_type = int(self.estimate_type_token.resolve(context))
        if estimate_type:
            estimate = int(estimate_type)
        
        report_year = expenditure.analysis_year
        
        data = []
        
        data_dict = {}
        for year in TE_YEARS:
            data_dict[year] = None
            
        note_dict = {}
        for year in TE_YEARS:
            note_dict[year] = []
    
        for estimate in expenditure.estimate_set.all():
            if estimate.corporations_amount and (estimate_type == GroupSummary.ESTIMATE_COMBINED or estimate_type == GroupSummary.ESTIMATE_CORPORATIONS): 
                
                if data_dict[estimate.estimate_year] == None:
                    data_dict[estimate.estimate_year] = 0
                data_dict[estimate.estimate_year] += estimate.corporations_amount
                
            if estimate.corporations_notes and (estimate_type == GroupSummary.ESTIMATE_COMBINED or estimate_type == GroupSummary.ESTIMATE_CORPORATIONS):
                note_dict[estimate.estimate_year].append(estimate.corporations_notes)
                
            if estimate.individuals_amount and (estimate_type == GroupSummary.ESTIMATE_COMBINED or estimate_type == GroupSummary.ESTIMATE_INDIVIDUALS):
                if data_dict[estimate.estimate_year] == None:
                    data_dict[estimate.estimate_year] = 0 
                data_dict[estimate.estimate_year] += estimate.individuals_amount
            
            if estimate.individuals_notes and (estimate_type == GroupSummary.ESTIMATE_COMBINED or estimate_type == GroupSummary.ESTIMATE_INDIVIDUALS):
                note_dict[estimate.estimate_year].append(estimate.individuals_notes)
            
        data = []
        for year in TE_YEARS:
            if data_dict.has_key(year) and data_dict[year]:
                if expenditure.analysis_year == 2011:
                    color = '#ddf'
                else:
                    if year == expenditure.analysis_year - 2:
                        color = '#ddf'
                    else:
                        color = '#ddd'
                if note_dict.has_key(year) and note_dict[year]:
                    note = True
                else:
                    note = False
                data.append({'value':data_dict[year], 'color':color, 'note':note})
                
            elif note_dict.has_key(year) and note_dict[year]:
                if expenditure.analysis_year == 2011:
                    color = '#ddf'
                else:
                    if year == expenditure.analysis_year - 2:
                        color = '#ddf'
                    else:
                        color = '#ddd'
            
                data.append({'value':None, 'color':color, 'note':True})
                
            else:
                data.append(None)
    
        return render_to_string('tax_expenditures/te_expenditure_detail.html', {'report_year':report_year, 'data':data})


@register.tag
def te_group_summary(parser, token):
    
    tag, group, source, estimate, years = token.split_contents()
    
    return TEGroupSummaryNode(group, source, estimate, years)
    
    
class TEGroupSummaryNode(Node):
    
    def __init__(self, category, source, estimate, years):
        self.group_token = Variable(category)
        self.source_token = Variable(source)
        self.estimate_token = Variable(estimate)
        self.years_token = Variable(years)
    
    def render(self, context):
        
        group = self.group_token.resolve(context)
        
        years = self.years_token.resolve(context)
        
        source = self.source_token.resolve(context)
        if source:
            source = int(source)
        
        estimate = int(self.estimate_token.resolve(context))
        if estimate:
            estimate = int(estimate)
        
        if not source or source == GroupSummary.SOURCE_JCT:
            jct_summary_dict = {}
        
            for summary in group.groupsummary_set.filter(source=GroupSummary.SOURCE_JCT, estimate=estimate):
                jct_summary_dict[summary.estimate_year] = summary.amount
                
            jct_summary = []
            for year in years:
                if jct_summary_dict.has_key(year):
                    jct_summary.append(jct_summary_dict[year])
                else:
                    jct_summary.append(None)
            
        else:
            jct_summary = None
            
        if not source or source == GroupSummary.SOURCE_TREASURY:
            treasury_summary_dict = {}
          
            for summary in group.groupsummary_set.filter(source=GroupSummary.SOURCE_TREASURY, estimate=estimate):
                treasury_summary_dict[summary.estimate_year] = summary.amount
            
            treasury_summary = []
            for year in years:
                if treasury_summary_dict.has_key(year):
                    treasury_summary.append(treasury_summary_dict[year])
                else:
                    treasury_summary.append(None)
            
        else:
            treasury_summary = None
        
        return render_to_string('tax_expenditures/te_group_summary.html', {'group':group, 'jct_summary':jct_summary, 'treasury_summary':treasury_summary})
    
    
    