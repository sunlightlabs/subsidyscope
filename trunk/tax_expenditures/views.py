import csv, re
from django.http import HttpResponse
from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect
from django.template import RequestContext
from tax_expenditures.models import Group, GroupSummary, Expenditure, Estimate, TE_YEARS


SOURCES = ('', 'JCT', 'Treasury')
MAX_COLUMNS = 11


def get_year_choices(columns, year):
    
    year_choices = []
    years = len(TE_YEARS) - columns + 1;
        
    previous_year = False
    next_year = False
    
    for i in range(0, years):
        
        first_year = TE_YEARS[0] + i
        
        year_choices.append({'value':first_year,'label':'%d-%d' % (first_year, first_year + columns - 1)})
        
        if not i == 0 and year == first_year:
            previous_year = first_year - 1
            
        if not i == years - 1 and year == first_year:
            next_year = first_year + 1
            
    return year_choices, previous_year, next_year


def main(request):
    
    groups = Group.objects.filter(parent=None)
    
    if request.GET.has_key('estimate'):
        estimate = int(request.GET['estimate'])
    else:
        estimate = GroupSummary.ESTIMATE_COMBINED
        
    if request.GET.has_key('year'):
        year = int(request.GET['year'])
    else:
        year = 2001
        
    year_choices, previous_year, next_year = get_year_choices(MAX_COLUMNS, year)
        
    estimate_years = range(year , year + MAX_COLUMNS)
    return render_to_response('tax_expenditures/main.html', {'groups':groups, 'source':None, 'estimate':estimate, 'estimate_years':estimate_years, 'num_years':len(estimate_years), 'year':year, 'year_choices':year_choices, 'previous_year':previous_year, 'next_year':next_year}, context_instance=RequestContext(request))


def group(request, group_id):
    
    group_id = int(group_id)
    
    if request.GET.has_key('estimate'):
        estimate = int(request.GET['estimate'])
    else:
        estimate = GroupSummary.ESTIMATE_COMBINED
    
    group = Group.objects.get(pk=group_id)
    
    subgroups = Group.objects.filter(parent=group)
    
    if request.GET.has_key('year'):
        year = int(request.GET['year'])
    else:
        year = 2001
        
    year_choices, previous_year, next_year = get_year_choices(MAX_COLUMNS, year)
        
    estimate_years = range(year, year + MAX_COLUMNS)
    
    report_years = range(2000, 2013)
    
    return render_to_response('tax_expenditures/group.html', {'group':group, 'subgroups':subgroups, 'source':None, 'estimate':estimate, 'report_years':report_years, 'estimate_years':estimate_years,  'year':year, 'year_choices':year_choices, 'previous_year':previous_year, 'next_year':next_year}, context_instance=RequestContext(request))


def te_csv(request, group_id=None):
    
    try:
        parent = Group.objects.get(pk=int(group_id))
        file_name = re.sub('[ ]', '_', re.sub('^a-zA-Z ', '', parent.name))[:30] + '.csv'
    except:
        parent = None
        file_name = 'tax_expenditures.csv'
    
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % (file_name)

    writer = csv.writer(response)
    
    header_summary = ['Indent', 'Budget Function', 'Subsidyscope Title', 'Title as Appears in Budget', 'Source', 'Footnotes', '2000 Total','2001 Total','2002 Total','2003 Total','2004 Total','2005 Total','2006 Total','2007 Total','2008 Total','2009 Total','2010 Total','2011 Total','2012 Total','2013 Total','2014 Total','2015 Total', '2016 Total', '2000 Corp','2001 Corp','2002 Corp','2003 Corp','2004 Corp','2005 Corp','2006 Corp','2007 Corp','2008 Corp','2009 Corp','2010 Corp','2011 Corp','2012 Corp','2013 Corp','2014 Corp','2015 Corp', '2016 Corp','2000 Indv','2001 Indv','2002 Indv','2003 Indv','2004 Indv','2005 Indv','2006 Indv','2007 Indv','2008 Indv','2009 Indv','2010 Indv','2011 Indv','2012 Indv','2013 Indv','2014 Indv','2015 Indv', '2016 Indv']

    
    if parent:
         
        top_level_group = parent
        
        while top_level_group.parent:
            top_level_group = top_level_group.parent
            
        budget_function = top_level_group.name
        if (parent.parent and not parent.parent.parent) or (Group.objects.filter(parent=parent).count() == 0):
            #this is a TE, not a group per se, so should print the line item for all subsequent groups, even multiple jct items
            header_summary.insert( 5, 'Report')
            writer.writerow(header_summary)
            line_item_csv(parent, writer, budget_function)

            for g in Group.objects.filter(parent=parent):
                line_item_csv(g, writer, budget_function, '**')
        
        else:
            #need footnote disclaimer
            writer.writerow(("The estimates presented below are the most recent estimates made for the year indicated in Row 1. Thus, the years in Row 1 do not correspond to the budget document from which the data was taken. For the years FY2000 through FY2009, the data presented can be found in the budget document two years prior to that fiscal year. For the years FY2010 through FY2016, the data presented can be found in the FY2012 Analytical Perspectives or the Estimates of Federal Tax Expenditures For Fiscal Years 2010-2014.",))
            writer.writerow(("\n",))
            writer.writerow(header_summary)
            recurse_category(parent, writer, '', budget_function)
    
    else:
        header = header_summary[4:]
        header.insert(0, 'Budget Function') 
        writer.writerow(header)
        for parent in Group.objects.filter(parent=None):
            budget_function = parent.name
            parent_summary(parent, writer)
#           recurse_category(parent, writer, '', budget_function)
    
    return response

def parent_summary(group, writer):
    for source in SOURCES[1:]:
        row = []
        row.append(group.name)
        row.append(source)
        row.append(group.notes)
        totals = GroupSummary.objects.filter(group=group, source=SOURCES.index(source), estimate=3).order_by('estimate_year')
        indv = GroupSummary.objects.filter(group=group, source=SOURCES.index(source), estimate=2).order_by('estimate_year')
        corp = GroupSummary.objects.filter(group=group, source=SOURCES.index(source), estimate=3).order_by('estimate_year')
        for est_group in (totals, corp, indv):
            for year in TE_YEARS:
                try:
                    est = est_group.get(estimate_year=year)
                    row.append(est.amount)
                except:
                    row.append('')
        writer.writerow(row)



def line_item_csv(parent, writer, budget_function, indent='*'):
    
    for expenditure in parent.expenditure_set.all().order_by('source'):
   
        corp_estimates = {}
        indv_estimates = {}
        total_estimates = {}
        
        for estimate in expenditure.estimate_set.all().order_by('estimate_year'):
            if estimate.corporations_amount or estimate.individuals_amount:
                total_estimates[estimate.estimate_year] = None
            
            if estimate.corporations_notes == Estimate.NOTE_POSITIVE:
                total_estimates[estimate.estimate_year] = 0
                corp_estimates[estimate.estimate_year] = '<50'
            elif estimate.corporations_notes == Estimate.NOTE_NEGATIVE:
                total_estimates[estimate.estimate_year] = 0
                corp_estimates[estimate.estimate_year] = '>-50'
            else:
                if estimate.corporations_amount:
                    corp_estimates[estimate.estimate_year] = estimate.corporations_amount
                    total_estimates[estimate.estimate_year] = estimate.corporations_amount
            
            if estimate.individuals_notes == Estimate.NOTE_POSITIVE:
                
                if total_estimates.get(estimate.estimate_year) and not total_estimates[estimate.estimate_year]:
                    total_estimates[estimate.estimate_year] = 0
                    
                indv_estimates[estimate.estimate_year] = '<50'
                
            elif estimate.individuals_notes == Estimate.NOTE_NEGATIVE:
                
                if not total_estimates[estimate.estimate_year]:
                    total_estimates[estimate.estimate_year] = 0
                
                indv_estimates[estimate.estimate_year] = '>-50'
                
            else:
                if estimate.individuals_amount:
                    indv_estimates[estimate.estimate_year] = estimate.individuals_amount
                    
                    if total_estimates[estimate.estimate_year]:
                        total_estimates[estimate.estimate_year] += estimate.individuals_amount
                    else:
                        total_estimates[estimate.estimate_year] = estimate.individuals_amount
        
        row = []
        row.append(indent) #no indent
        row.append(budget_function)
        row.append(parent.name)
        row.append(expenditure.name)
        row.append(expenditure.get_source_display())
        row.append(expenditure.analysis_year)
        row.append(expenditure.notes)
        
        for year in TE_YEARS:
            if total_estimates.has_key(year):
                row.append(total_estimates[year])
            else:
                row.append('')
            
        for year in TE_YEARS:
            if corp_estimates.has_key(year):
                row.append(corp_estimates[year])
            else:
                row.append('')
                
        for year in TE_YEARS:                
            if indv_estimates.has_key(year):
                row.append(indv_estimates[year])
            else:
                row.append('')    
        
        writer.writerow(row)                  


def recurse_category(parent, writer, indent, budget_function):

    if not parent.parent:
        writer.writerow([indent, budget_function, parent.name])
    else:
        for source in (1, 2):
            row = []
            row.append(indent)
            row.append(budget_function)
            row.append(parent.name)
#    row.append(expenditure.name)
#   row.append(parent.get_source_display())
#    row.append(parent.analysis_year)
           
            first = True
            has_expenditure = False 
            corp_estimates = {}
            indv_estimates = {}
            total_estimates = {}
        
            for expenditure in parent.expenditure_set.filter(source=source).order_by('analysis_year'):
                has_expenditure = True
                if first:
                    row.append(expenditure.name)
                    row.append(SOURCES[source])
                    row.append(parent.notes)
                    first = False

                for estimate in expenditure.estimate_set.all().order_by('estimate_year'):
                    if estimate.corporations_amount or estimate.individuals_amount:
                        total_estimates[estimate.estimate_year] = None
                    
                    if estimate.corporations_notes == Estimate.NOTE_POSITIVE:
                        total_estimates[estimate.estimate_year] = 0
                        corp_estimates[estimate.estimate_year] = '<50'
                    elif estimate.corporations_notes == Estimate.NOTE_NEGATIVE:
                        total_estimates[estimate.estimate_year] = 0
                        corp_estimates[estimate.estimate_year] = '>-50'
                    else:
                        if estimate.corporations_amount:
                            corp_estimates[estimate.estimate_year] = estimate.corporations_amount
                            total_estimates[estimate.estimate_year] = estimate.corporations_amount
                    
                    if estimate.individuals_notes == Estimate.NOTE_POSITIVE:
                        
                        if total_estimates.get(estimate.estimate_year) and not total_estimates[estimate.estimate_year]:
                            total_estimates[estimate.estimate_year] = 0
                            
                        indv_estimates[estimate.estimate_year] = '<50'
                        
                    elif estimate.individuals_notes == Estimate.NOTE_NEGATIVE:
                        
                        if not total_estimates[estimate.estimate_year]:
                            total_estimates[estimate.estimate_year] = 0
                        
                        indv_estimates[estimate.estimate_year] = '>-50'
                        
                    else:
                        if estimate.individuals_amount:
                            indv_estimates[estimate.estimate_year] = estimate.individuals_amount
                            
                            if total_estimates[estimate.estimate_year]:
                                total_estimates[estimate.estimate_year] += estimate.individuals_amount
                            else:
                                total_estimates[estimate.estimate_year] = estimate.individuals_amount
                
                
            for year in TE_YEARS:
                if total_estimates.has_key(year):
                    row.append(total_estimates[year])
                else:
                    row.append('')
                
            for year in TE_YEARS:
                if corp_estimates.has_key(year):
                    row.append(corp_estimates[year])
                else:
                    row.append('')
                    
            for year in TE_YEARS:                
                if indv_estimates.has_key(year):
                    row.append(indv_estimates[year])
                else:
                    row.append('')    
            if has_expenditure:
                writer.writerow(row)                  
                
    indent += '*'
        
    for subgroup in Group.objects.filter(parent=parent):
            
        recurse_category(subgroup, writer, indent, budget_function)
                        

