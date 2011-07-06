import csv, re
from django.http import HttpResponse
from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect
from django.template import RequestContext
from tax_expenditures.models import Group, GroupSummary, Expenditure, Estimate, TE_YEARS
from haystack.query import SearchQuerySet

SOURCES = ('', 'JCT', 'Treasury')
MAX_COLUMNS = 8

lower_level_footnote = """The Joint Committee on Taxation (JCT) does not provide numerical data for values that are between -$50 million and $50 million. Rather it provides a footnote indicating that the values are either "greater than -$50 million" or "less than $50 million." The estimates in the individual and corporation columns from the JCT may contain values between -$50 million and $50 million (denoted as >-50 or <50). When aggregated, in the totals column, the sums of these values are unknown and thus are rounded to zero. For more information, see Subsidyscope's methodology."""

top_level_footnote = """The Joint Committee on Taxation (JCT) does not provide numerical data for values that are between -$50 million and $50 million. Rather it provides a footnote indicating that the values are either "greater than -$50 million" or "less than $50 million." When aggregated, the sums of these values are unknown and thus are rounded to zero. The aggregated estimates that are presented in this document do not indicate where these rounded values exist. For information on which estimates contain these rounded values please review the specific tax expenditure estimates. For more information, see Subsidyscope's methodology."""


def search(request):
    querystring = request.GET['query']
    if querystring:
        search_results = SearchQuerySet().filter(content=querystring).models(Group).load_all()
        results = []

        for r in search_results:
            bf = r._object.parent
            if bf:
               while bf.parent is not None:
                   bf = bf.parent
               results.append((r._object, bf))

        return render_to_response('tax_expenditures/search-results.html', {'results': results, 'query': querystring}, context_instance=RequestContext(request))
    else:
        return render_to_response('tax_expenditures/search-results.html', {'query': querystring}, context_instance=RequestContext(request))

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
        year = 2007
        
    year_choices, previous_year, next_year = get_year_choices(MAX_COLUMNS, year)
        
    estimate_years = range(year, year + MAX_COLUMNS)
    
    report_years = range(2000, 2013)
    
    return render_to_response('tax_expenditures/group.html', {'group':group, 'subgroups':subgroups, 'source':None, 'estimate':estimate, 'report_years':report_years, 'estimate_years':estimate_years,  'year':year, 'year_choices':year_choices, 'previous_year':previous_year, 'next_year':next_year}, context_instance=RequestContext(request))


def data_page_csv():
    source_text = [None, 'JCT', 'Treasury']
    report_years = range(2000, 2013)
    for ry in report_years:
        for source in (1, 2):
            writer = csv.writer(open('tax_expenditures/data_page_csvs/'+ source_text[source] + '_' + str(ry) + '.csv', 'w'))
            header = ['Budget_function', 'Title as it Appears in Source']
            groups = Group.objects.filter(parent=None).order_by('id')
            if source == 1:
                years = range(ry-2, ry+3)
            else:
                years = range(ry-2, ry+5)

            for y in years:
                header.append(str(y) + ' Indv')
            for y in years:
                header.append(str(y) + ' Corp')
            for y in years:
                header.append(str(y) + ' Total')

            header.append('Notes')
            writer.writerow(header)

            for gp in groups:
                static_csv_recurse(gp, writer, gp.name, ry, source, years)

def static_csv_recurse(gp, writer, budget_function, ry, source, years):
     
    exps = Expenditure.objects.filter(analysis_year=ry, source=source, group=gp).order_by('id')
    if exps.count() > 0:
        for ex in exps:
            row = [budget_function, ex.name]
            estimates = Estimate.objects.filter(expenditure=ex, estimate_year__in=years).order_by('estimate_year')
            for est in estimates:
                row.append(est.individuals_amount)
                
            for est in estimates:
                row.append(est.corporations_amount)

            for est in estimates:
                row.append((est.corporations_amount or 0) + (est.individuals_amount or 0))

            row.append(ex.notes)

            writer.writerow(row)

    else:
        for subgroup in Group.objects.filter(parent=gp):
            static_csv_recurse(subgroup, writer, budget_function, ry, source, years)

def one_off_csv():
    writer = csv.writer(open('post_processed_all.csv', 'w'))
    header_summary = ['Indent', 'Budget Function', 'Subsidyscope Title', 'Title as Appears in Budget', 'Source', 'Report Year', '2000 Total','2001 Total','2002 Total','2003 Total','2004 Total','2005 Total','2006 Total','2007 Total','2008 Total','2009 Total','2010 Total','2011 Total','2012 Total','2013 Total','2014 Total','2015 Total', '2016 Total', '2000 Corp','2001 Corp','2002 Corp','2003 Corp','2004 Corp','2005 Corp','2006 Corp','2007 Corp','2008 Corp','2009 Corp','2010 Corp','2011 Corp','2012 Corp','2013 Corp','2014 Corp','2015 Corp', '2016 Corp','2000 Indv','2001 Indv','2002 Indv','2003 Indv','2004 Indv','2005 Indv','2006 Indv','2007 Indv','2008 Indv','2009 Indv','2010 Indv','2011 Indv','2012 Indv','2013 Indv','2014 Indv','2015 Indv', '2016 Indv']
    writer.writerow(header_summary)
    top_level_groups = Group.objects.filter(parent=None).order_by('id')
    for gp in top_level_groups:
        one_off_recurse_category(gp, writer, '', gp.name)


def one_off_recurse_category(grp, writer, indent, budget_function, name_prefix=None):
    
    if Group.objects.filter(parent=grp).count() == 0:
        line_item_csv(grp, writer, budget_function, indent, name_prefix)
    else:
        name_prefix = ''
        if Expenditure.objects.filter(group=grp).count() > 0:
            line_item_csv(grp, writer, budget_function, indent)
            name_prefix = grp.name + ' - '

        indent += '*'
        
        for subgroup in Group.objects.filter(parent=grp):
            
            one_off_recurse_category(subgroup, writer, indent, budget_function, name_prefix)


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
    
    header_summary = ['Indent', 'Budget Function', 'Subsidyscope Title', 'Title as Appears in Budget', 'Source', '2000 Total','2001 Total','2002 Total','2003 Total','2004 Total','2005 Total','2006 Total','2007 Total','2008 Total','2009 Total','2010 Total','2011 Total','2012 Total','2013 Total','2014 Total','2015 Total', '2016 Total', '2000 Corp','2001 Corp','2002 Corp','2003 Corp','2004 Corp','2005 Corp','2006 Corp','2007 Corp','2008 Corp','2009 Corp','2010 Corp','2011 Corp','2012 Corp','2013 Corp','2014 Corp','2015 Corp', '2016 Corp','2000 Indv','2001 Indv','2002 Indv','2003 Indv','2004 Indv','2005 Indv','2006 Indv','2007 Indv','2008 Indv','2009 Indv','2010 Indv','2011 Indv','2012 Indv','2013 Indv','2014 Indv','2015 Indv', '2016 Indv', 'Footnotes']

    general_footnote = "The estimates presented below are the most recent estimates made for the year indicated in Row 1. Thus, the years in Row 1 do not correspond to the budget document from which the data was taken. For the years FY2000 through FY2009, the data presented can be found in the budget document two years prior to that fiscal year. For the years FY2010 through FY2016, the data presented can be found in the FY2012 Analytical Perspectives or the Estimates of Federal Tax Expenditures For Fiscal Years 2010-2014."
    
    if parent:
         
        top_level_group = parent
        
        while top_level_group.parent:
            top_level_group = top_level_group.parent
            
        budget_function = top_level_group.name
        if (parent.parent and not parent.parent.parent) or (Group.objects.filter(parent=parent).count() == 0):
            writer.writerow((lower_level_footnote,))
            writer.writerow(('',))
            #this is a TE, not a group per se, so should print the line item for all subsequent groups, even multiple jct items
            header_summary.insert( 5, 'Report')
            writer.writerow(header_summary)
            line_item_csv(parent, writer, budget_function)

            for g in Group.objects.filter(parent=parent):
                line_item_csv(g, writer, budget_function, '**')
        
        else:
            #need footnote disclaimer
            writer.writerow((general_footnote,))
            writer.writerow((lower_level_footnote,))
            writer.writerow(("",))
            writer.writerow(header_summary[:len(header_summary)-1])
            recurse_category(parent, writer, '', budget_function)
    
    else:
        writer.writerow((general_footnote,))
        writer.writerow((top_level_footnote,))
        writer.writerow(("",))
        header = header_summary[4:len(header_summary)-1]
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



def line_item_csv(parent, writer, budget_function, indent='*', name_prefix=''):
    
    for expenditure in parent.expenditure_set.all().order_by('source'):
   
        corp_estimates = {}
        indv_estimates = {}
        total_estimates = {}
        
        for estimate in expenditure.estimate_set.all().order_by('estimate_year'):
            if estimate.corporations_amount != None or estimate.individuals_amount != None:
                total_estimates[estimate.estimate_year] = None
            
            if estimate.corporations_notes == Estimate.NOTE_POSITIVE:
                total_estimates[estimate.estimate_year] = 0
                corp_estimates[estimate.estimate_year] = '<50'
            elif estimate.corporations_notes == Estimate.NOTE_NEGATIVE:
                total_estimates[estimate.estimate_year] = 0
                corp_estimates[estimate.estimate_year] = '>-50'
            else:
                if estimate.corporations_amount != None:
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
                if estimate.individuals_amount != None:
                    indv_estimates[estimate.estimate_year] = estimate.individuals_amount
                    
                    if total_estimates[estimate.estimate_year]:
                        total_estimates[estimate.estimate_year] += estimate.individuals_amount
                    else:
                        total_estimates[estimate.estimate_year] = estimate.individuals_amount
        
        row = []
        row.append(indent) #no indent
        row.append(budget_function)
        row.append(name_prefix + parent.name)
        row.append(expenditure.name)
        row.append(expenditure.get_source_display())
        row.append(expenditure.analysis_year)
        
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
        
        row.append(expenditure.notes)
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
            #        row.append(parent.notes)
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
                        

