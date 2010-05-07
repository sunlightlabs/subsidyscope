from morsels.models import Morsel, Page
from django.template import Library, Node, Variable
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Template
from django.template.loader import render_to_string

from tax_expenditures.models import *

register = Library()

@register.tag
def render_te_category(parser, token):
    
    tag, category = token.split_contents()
    
    return TECategoryNode(category)
    
    
class TECategoryNode(Node):
    
    def __init__(self, category):
        self.category_token = Variable(category)
    
    def render(self, context):
        
        category = self.category_token.resolve(context)
        
        subcategories = [] 
        
        expenditures = TaxExpenditure.objects.filter(category=category)
        
        return render_to_string('tax_expenditures/te_category.html', {'category_name':category.name, 'subcategories': subcategories, 'expenditures':expenditures})
    
    
@register.tag
def render_te_expenditure(parser, token):
    
    tag, expenditure = token.split_contents()
    
    return TENode(expenditure)
    
    
class TENode(Node):
    
    def __init__(self, expenditure):
        self.expenditure_token = Variable(expenditure)
    
    def render(self, context):
        
        expenditure = self.expenditure_token.resolve(context)
        
        return render_to_string('tax_expenditures/te_expenditure.html', {'expenditure_name':expenditure.name})
        
        
        
        
        