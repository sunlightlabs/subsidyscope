import csv, re
from django.http import HttpResponse
from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect
from django.template import RequestContext
from tax_expenditures.models import Group, GroupSummary, Expenditure, Estimate, TE_YEARS


def main(request, estimate=GroupSummary.ESTIMATE_COMBINED):
    
    groups = Group.objects.filter(parent=None)
    
    estimate = int(estimate)
    years = range(2000,2014)
    return render_to_response('tax_expenditures/main.html', {'groups':groups, 'source':None, 'estimate':estimate, 'te_years':years, 'num_years':len(years)}, context_instance=RequestContext(request))


def group(request, group_id, estimate):
    
    group_id = int(group_id)
    
    estimate = int(estimate)
    
    group = Group.objects.get(pk=group_id)
    
    subgroups = Group.objects.filter(parent=group)
    estimate_years = range(2000, 2014)
    report_years = range(2000, 2012)
    return render_to_response('tax_expenditures/group.html', {'group':group, 'subgroups':subgroups, 'source':None, 'estimate':estimate, 'report_years':report_years, 'estimate_years':estimate_years}, context_instance=RequestContext(request))


def group_alt(request, group_id, estimate):
    
    group_id = int(group_id)
    
    estimate = int(estimate)
    
    group = Group.objects.get(pk=group_id)
    
    subgroups = Group.objects.filter(parent=group)
    estimate_years = range(2007, 2014)
    report_years = range(2000, 2012)
    return render_to_response('tax_expenditures/group_alt.html', {'group':group, 'subgroups':subgroups, 'source':None, 'estimate':estimate, 'report_years':report_years, 'estimate_years':estimate_years}, context_instance=RequestContext(request))
    


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
    
    writer.writerow(['Indent','Category','Source','Report','2000 (Corp)','2001 (Corp)','2002 (Corp)','2003 (Corp)','2004 (Corp)','2005 (Corp)','2006 (Corp)','2007 (Corp)','2008 (Corp)','2009 (Corp)','2010 (Corp)','2011 (Corp)','2012 (Corp)','2013 (Corp)','2014 (Corp)','2015 (Corp)','2000 (Indv)','2001 (Indv)','2002 (Indv)','2003 (Indv)','2004 (Indv)','2005 (Indv)','2006 (Indv)','2007 (Indv)','2008 (Indv)','2009 (Indv)','2010 (Indv)','2011 (Indv)','2012 (Indv)','2013 (Indv)','2014 (Indv)','2015 (Indv)'])
    
    
    if parent:
        
        recurse_category(parent, writer, '')
    
    else:
        for parent in Group.objects.filter(parent=None):
            recurse_category(parent, writer, '')
    
    return response

def recurse_category(parent, writer, indent):
    
    indent += '*'

    writer.writerow([indent, parent.name])
        
    for expenditure in parent.expenditure_set.order_by('source', 'analysis_year'):
        
        row = []
        row.append(indent + '*')
        row.append(expenditure.name)
        row.append(expenditure.get_source_display())
        row.append(expenditure.analysis_year)
        
        corp_estimates = {}
        indv_estimates = {}
        
        footnotes = {}
        
        for estimate in expenditure.estimate_set.all():
            
            if estimate.corporations_notes == Estimate.NOTE_POSITIVE:
                corp_estimates[estimate.estimate_year] = '<50'
            elif estimate.corporations_notes == Estimate.NOTE_NEGATIVE:
                corp_estimates[estimate.estimate_year] = '>-50'
            else:
                corp_estimates[estimate.estimate_year] = estimate.corporations_amount
            
            if estimate.individuals_notes == Estimate.NOTE_POSITIVE:
                indv_estimates[estimate.estimate_year] = '<50'
            elif estimate.individuals_notes == Estimate.NOTE_NEGATIVE:
                indv_estimates[estimate.estimate_year] = '>-50'
            else:
                indv_estimates[estimate.estimate_year] = estimate.individuals_amount
                
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
        
        for year in TE_YEARS:
            if footnotes.has_key(year):
                row.append(footnotes[year])
            else:
                row.append('')
        
        writer.writerow(row)                  
            
            
    for subgroup in Group.objects.filter(parent=parent):
        
        recurse_category(subgroup, writer, indent)
                    

