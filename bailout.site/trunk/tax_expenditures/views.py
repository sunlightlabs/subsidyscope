from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect
from tax_expenditures.models import Category, ExpenditureGroup, Expenditure


def main(request, category_id=None, year=None, source=None):
    
    categories = Category.objects.filter(parent=None)
    
    return render_to_response('tax_expenditures/main.html', {'categories':categories})


def category(request, category_id, year=None, source=None):
    
    category_id = int(category_id)
    
    category = Category.objects.get(pk=category_id)
    
    return render_to_response('tax_expenditures/category.html', {'category':category})
    

def expenditure(request, expenditure_id, year=None, source=None):
    
    expenditure_id = int(expenditure_id)
    
    expenditure = ExpenditureGroup.objects.get(pk=expenditure_id)
    
    treasury_expenditure_summary = []
    
    for expenditure_report in expenditure.group.filter(source=Expenditure.SOURCE_TREASURY):
        
        estimates = {}
        
        for estimate in expenditure_report.estimate_set.all():
            
            estimates[estimate.estimate_year] = 0
             
            if estimate.corporations_amount:
                estimates[estimate.estimate_year] += estimate.corporations_amount  
            if estimate.individuals_amount:
                estimates[estimate.estimate_year] += estimate.individuals_amount
        
        report = {}
        report['analysis_year'] = expenditure_report.analysis_year
        report['estimates'] = []
        
        i = 0
        for year in range(2000,2016):
            if estimates.has_key(year):
                if len(treasury_expenditure_summary) and treasury_expenditure_summary[-1]['estimates'][i] != None:
                    treasury_expenditure_summary[-1]['estimates'][i]['latest'] = False
                report['estimates'].append({'value':estimates[year],'latest':True})
            else:
                report['estimates'].append(None)
                
            i += 1
        
        treasury_expenditure_summary.append(report)
        
        
    jct_expenditure_summary = []
    
    for expenditure_report in expenditure.group.filter(source=Expenditure.SOURCE_JCT):
        
        estimates = {}
        
        for estimate in expenditure_report.estimate_set.all():
            
            estimates[estimate.estimate_year] = 0
             
            if estimate.corporations_amount:
                estimates[estimate.estimate_year] += estimate.corporations_amount  
            if estimate.individuals_amount:
                estimates[estimate.estimate_year] += estimate.individuals_amount
        
        report = {}
        report['analysis_year'] = expenditure_report.analysis_year
        report['estimates'] = []
        
        i = 0
        for year in range(2000,2016):
            if estimates.has_key(year):
                if len(jct_expenditure_summary) and jct_expenditure_summary[-1]['estimates'][i] != None:
                    jct_expenditure_summary[-1]['estimates'][i]['latest'] = False
                report['estimates'].append({'value':estimates[year],'latest':True})
            else:
                report['estimates'].append(None)
            i += 1
        
        jct_expenditure_summary.append(report)
    
    other_expenditures = Expenditure.objects.filter(category=expenditure.category).order_by('name', 'analysis_year')
     
    
    return render_to_response('tax_expenditures/expenditure.html', {'expenditure':expenditure, 'treasury_expenditure_summary':treasury_expenditure_summary, 'jct_expenditure_summary':jct_expenditure_summary, 'other_expenditures':other_expenditures})
        
#def expenditure_add(request, expenditure_id, year=None, source=None):
#    
#    expenditure_id = int(expenditure_id)
#    
#    if request.method == "POST":
#        group = ExpenditureGroup.objects.get(pk=expenditure_id)
#        request.POST['']
#        group.group.add()
#    else:
#        return HttpResponseRedirect('/tax_expenditures/expenditure/%d/' % expenditure_id)