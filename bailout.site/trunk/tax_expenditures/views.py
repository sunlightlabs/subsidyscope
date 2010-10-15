from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect
from django.template import RequestContext
from tax_expenditures.models import Group, GroupSummary, Expenditure, TE_YEARS


def main(request, estimate=GroupSummary.ESTIMATE_COMBINED):
    
    groups = Group.objects.filter(parent=None)
    
    estimate = int(estimate)
    
    return render_to_response('tax_expenditures/main.html', {'groups':groups, 'source':None, 'estimate':estimate, 'te_years':TE_YEARS}, context_instance=RequestContext(request))


def group(request, group_id, estimate):
    
    group_id = int(group_id)
    
    estimate = int(estimate)
    
    group = Group.objects.get(pk=group_id)
    
    jct_expenditures = Expenditure.objects.filter(group=group, source=Expenditure.SOURCE_JCT)
    treasury_expenditures = Expenditure.objects.filter(group=group, source=Expenditure.SOURCE_TREASURY)
    
    subgroups = Group.objects.filter(parent=group)
    
    return render_to_response('tax_expenditures/group.html', {'group':group, 'subgroups':subgroups, 'jct_expenditures':jct_expenditures, 'treasury_expenditures':treasury_expenditures, 'source':None, 'estimate':estimate, 'te_years':TE_YEARS})
    
