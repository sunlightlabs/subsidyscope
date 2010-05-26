from django.shortcuts import render_to_response
from tax_expenditures.models import *


def render_tax_expenditures(request, category_id=''):
    
    if not category_id == '':
        category_id = int(category_id)
    else:
        category_id = 25
    
    top_level_categories = TaxExpenditureCategory.objects.filter(parent=None).order_by('name')
    
    selected_category = TaxExpenditureCategory.objects.get(id=category_id)
    
    subcategories = TaxExpenditureCategory.objects.filter(parent__id=category_id).order_by('name')
    
    expenditures = TaxExpenditure.objects.filter(category=selected_category).order_by('name')
    
    return render_to_response('tax_expenditures/te_view.html', {'top_level_categories':top_level_categories, 'subcategories':subcategories, 'selected_category': selected_category, 'expenditures':expenditures})



def render_tax_expenditure(request, expenditure_id):
    
    expenditure_id = int(expenditure_id)
    
    expenditure = TaxExpenditure.objects.get(id=expenditure_id)
    
    category_stack = []
    
    category = expenditure.category
    
    category_stack.append(category)
    
    while category.parent: 
    
        category_stack.append(category.parent)
        
        category = category.parent
        
    top_category = category_stack.pop()
    
    category_stack.reverse()
    
    if expenditure.jct_estimate:
        jct = expenditure.jct_estimate.get_estimates()
    else:
        jct = False
        
    
    if expenditure.omb_estimate:
        treasury = expenditure.omb_estimate.get_estimates()
    else:
        treasury = False
    
    return render_to_response('tax_expenditures/te_detail.html', {'expenditure':expenditure, 'category_stack':category_stack, 'top_category':top_category, 'treasury': treasury, 'jct': jct})


