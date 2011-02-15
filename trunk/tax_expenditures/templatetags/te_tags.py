from morsels.models import Morsel, Page
from django.template import Library, Node, Variable
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Template
from django.template.loader import render_to_string

from tax_expenditures.models import Expenditure, Group, GroupSummary, TE_YEARS

register = Library()

JCT_SOURCES = {}

JCT_SOURCES[2001] = 'JCT. "JCS-1-98: Estimates Of Federal Tax Expenditures For Fiscal Years 1999-2003."'
JCT_SOURCES[2002] = 'JCT. "JCS-13-99: Estimates Of Federal Tax Expenditures For Fiscal Years 2000-2004."'
JCT_SOURCES[2003] = 'JCT. "JCS-1-01: Estimates Of Federal Tax Expenditures For Fiscal Years 2001-2005."'
JCT_SOURCES[2004] = 'JCT. "JCS-1-02: Estimates Of Federal Tax Expenditures For Fiscal Years 2002-2006."'
JCT_SOURCES[2005] = 'JCT. "JCS-5-02: Estimates Of Federal Tax Expenditures For Fiscal Years 2003-2007."'
JCT_SOURCES[2006] = 'JCT. "JCS-8-03: Estimates Of Federal Tax Expenditures For Fiscal Years 2004-2008."'
JCT_SOURCES[2007] = 'JCT. "JCS-1-05: Estimates Of Federal Tax Expenditures For Fiscal Years 2005-2009."'
JCT_SOURCES[2008] = 'JCT. "JCS-2-06: Estimates Of Federal Tax Expenditures For Fiscal Years 2006-2010."'
JCT_SOURCES[2009] = 'JCT. "JCS-3-07: Estimates Of Federal Tax Expenditures For Fiscal Years 2007-2011."'
JCT_SOURCES[2010] = 'JCT. "JCS-2-08: Estimates Of Federal Tax Expenditures For Fiscal Years 2008-2012."'
JCT_SOURCES[2011] = 'JCT. "JCS-1-10: Estimates Of Federal Tax Expenditures For Fiscal Years 2009-2013."'
JCT_SOURCES[2012] = 'JCT. "JCS-3-10: Estimates Of Federal Tax Expenditures For Fiscal Years 2010-2014."'


TREASURY_SOURCES = {}

TREASURY_SOURCES[2000] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2000."'
TREASURY_SOURCES[2001] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2001."'
TREASURY_SOURCES[2002] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2002."'
TREASURY_SOURCES[2003] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2003."'
TREASURY_SOURCES[2004] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2004."'
TREASURY_SOURCES[2005] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2005."'
TREASURY_SOURCES[2006] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2006."'
TREASURY_SOURCES[2007] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2007."'
TREASURY_SOURCES[2008] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2008."'
TREASURY_SOURCES[2009] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2009."'
TREASURY_SOURCES[2010] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2010."'
TREASURY_SOURCES[2011] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2011."'
TREASURY_SOURCES[2012] = 'OMB. "Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2011."'


@register.tag
def te_previous_year(parser, token):
    
    tag, previous_year = token.split_contents()

    return TEYearButton(previous_year, TEYearButton.DIRECTION_PREVIOUS)

@register.tag
def te_next_year(parser, token):
    
    tag, next_year = token.split_contents()

    return TEYearButton(next_year, TEYearButton.DIRECTION_NEXT)


class TEYearButton(Node):
    
    DIRECTION_PREVIOUS = 1
    DIRECTION_NEXT = 2
    
    def __init__(self, year, direction):
        
        self.direction = direction
        self.year_token = Variable(year)

    def render(self, context):
        
        year = self.year_token.resolve(context)
    
        if year:
            
            if self.direction == self.DIRECTION_PREVIOUS:
                return  '<a href="#" onclick="changeYear(%d); return false;" class="left_arrow"></a>&nbsp;' % (year)
            else:
                return  '&nbsp;<a href="#" onclick="changeYear(%d); return false;" class="right_arrow"></a>' % (year) 
        
        else:
            return ''

@register.tag
def te_breadcrumb(parser, token):
    
    tag, group, estimate_type, year = token.split_contents()

    return TEBreadcrumb(group, estimate_type, year)

class TEBreadcrumb(Node):
    
    def __init__(self, group, estimate_type, year):
        
        self.group_token = Variable(group)
        self.estimate_type_token = Variable(estimate_type)
        self.year_token = Variable(year)
    
    def render(self, context):
        
        group = self.group_token.resolve(context)
        
        estimate_type = int(self.estimate_type_token.resolve(context))
        year = int(self.year_token.resolve(context))
        if estimate_type:
            estimate = int(estimate_type)

        list = []
        
        if group:
        
            list.append(group)
            while group.parent:
                group = group.parent
                list.append(group)
            
            list.reverse()

        return render_to_string('tax_expenditures/te_breadcrumb.html', {'list':list, 'estimate_type':estimate_type, 'year':year})

@register.tag
def te_expenditure_detail(parser, token):
    
    tag, group, report_years, estimate_years, estimate_type, source, previous_year, next_year = token.split_contents()
    
    return TEEpenditureDetailNode(group, report_years, estimate_years, estimate_type, source, previous_year, next_year)

class TEEpenditureDetailNode(Node):
    
    def __init__(self, group, report_years, estimate_years, estimate_type, source, previous_year, next_year):
        
        self.group_token = Variable(group)
        self.report_years_token = Variable(report_years)
        self.estimate_years_token = Variable(estimate_years)
        self.estimate_type_token = Variable(estimate_type)
        self.source_token = Variable(source)
        self.previous_year_type_token = Variable(previous_year)
        self.next_year_token = Variable(next_year)
    
    def render(self, context):
        
        group = self.group_token.resolve(context)
        
        report_years = self.report_years_token.resolve(context)
        estimate_years = self.estimate_years_token.resolve(context)
        
        previous_year = self.previous_year_type_token.resolve(context)
        next_year = self.next_year_token.resolve(context)
       
        estimate_type = int(self.estimate_type_token.resolve(context))
        if estimate_type:
            estimate = int(estimate_type)

        source = self.source_token.resolve(context)

        if source == 'JCT':
            source_id =  Expenditure.SOURCE_JCT
        elif source == 'Treasury':
            source_id =  Expenditure.SOURCE_TREASURY
        else:
            raise Exception('invalid source')
        
        lines = []
        
        
        available_report_years = []
        
        for detail in group.groupdetail_set.filter(source=source_id, estimate=estimate):
            if detail.amount or detail.notes: 
                available_report_years.append(detail.analysis_year)
            
        
        last_available_report = max(available_report_years)   
           
        
        for report_year in report_years:
            
            data_dict = {}
            
            available_report_years = []
            
            for detail in group.groupdetail_set.filter(source=source_id, estimate=estimate, analysis_year=report_year):
                data_dict[detail.estimate_year] = {'amount': detail.amount, 'notes': detail.notes}
                available_report_years.append(detail.analysis_year) 
            
            data = []
            blank_line = True
            for year in estimate_years:
                if data_dict.has_key(year) and not data_dict[year] == None:
                    if report_year == last_available_report:
                        color = '#aaf'
                    else:
                        if year == report_year - 2:
                            color = '#aaf'
                        else:
                            color = '#eee'
                    
                    if not data_dict[year]['amount'] == None or data_dict[year]['notes']:
                        data.append({'value':data_dict[year]['amount'], 'notes':data_dict[year]['notes'], 'color':color})
                        blank_line = False
                    else:
                        data.append(None)
                    
                else:
                    data.append(None)
                    
            if not blank_line:
                id = source + str(report_year)
                report = group.groupdetailreport_set.get(source=source_id, analysis_year=report_year)
                
                if source == 'JCT':
                    source_string = JCT_SOURCES[report_year]
                else:
                    source_string = TREASURY_SOURCES[report_year]
                    
                footnotes = ''
                
                if report.expenditure_source:
                    source_string = '%s from %s' % (report.expenditure_source.name, source_string)
                    footnotes = report.expenditure_source.notes
                else:
                    source_string = '%s Sum of %s tax expenditures listed above.' % (source_string, source)    
            
                lines.append({'report_year':report_year, 'id':id, 'data':data, 'source':source_string, 'footnotes':footnotes})
        
        if len(lines):
            return render_to_string('tax_expenditures/te_expenditure_detail.html', {'lines':lines, 'estimate_years':estimate_years, 'source':source, 'previous_year':previous_year, 'next_year':next_year})
        else:
            return ''


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
                jct_summary_dict[summary.estimate_year] = {'amount': summary.amount, 'notes': summary.notes}
                
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
                treasury_summary_dict[summary.estimate_year] = {'amount': summary.amount, 'notes': summary.notes}
            
            treasury_summary = []
            no_data = True
            for year in years:
                if treasury_summary_dict.has_key(year):
                    treasury_summary.append(treasury_summary_dict[year])
                    no_data = False
                else:
                    treasury_summary.append(None)
            
            if no_data:
                treasury_summary = None
        else:
            treasury_summary = None
        
        return render_to_string('tax_expenditures/te_group_summary.html', {'group':group, 'jct_summary':jct_summary, 'treasury_summary':treasury_summary})
    

@register.tag
def te_group_summary_alt(parser, token):
    
    tag, group, source, estimate, years = token.split_contents()
    
    return TEGroupSummaryAltNode(group, source, estimate, years)
    
    
class TEGroupSummaryAltNode(Node):
    
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
        
        
        jct_summary_dict = {}
        
        if not source or source == GroupSummary.SOURCE_JCT:
        
            for summary in group.groupsummary_set.filter(source=GroupSummary.SOURCE_JCT, estimate=estimate):
                jct_summary_dict[summary.estimate_year] = {'amount': summary.amount, 'notes': summary.notes}
            
            
        treasury_summary_dict = {}
        
        if not source or source == GroupSummary.SOURCE_TREASURY:
          
            for summary in group.groupsummary_set.filter(source=GroupSummary.SOURCE_TREASURY, estimate=estimate):
                treasury_summary_dict[summary.estimate_year] = {'amount': summary.amount, 'notes': summary.notes}
            
            
        summary = []
        for year in years:
            estimate = {}
            
            if jct_summary_dict.has_key(year):
                estimate['jct'] = jct_summary_dict[year]
            else:
                estimate['jct'] = None
                
                
            if treasury_summary_dict.has_key(year):
                estimate['treasury'] = treasury_summary_dict[year]
            else:
                estimate['treasury'] = None
                
            summary.append(estimate)

        
        return render_to_string('tax_expenditures/te_group_summary_alt.html', {'group':group, 'summary':summary})