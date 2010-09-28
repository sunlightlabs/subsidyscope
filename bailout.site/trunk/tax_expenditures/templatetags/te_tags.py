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
def te_category_summary(parser, token):
    
    tag, category = token.split_contents()
    
    return TECategoryNode(category)
    
    
class TECategoryNode(Node):
    
    def __init__(self, category):
        self.category_token = Variable(category)
    
    def render(self, context):
        
        category = self.category_token.resolve(context)
        
        cube = category.aggregate()
        
        years = range(2008, 2016)
        
        data = []
        
        for year in years:
            
            if cube.dimensions.has_key('year') and cube.dimensions['year'].values.has_key(year):
            
                results = cube.query(attributes={'year':year}, groups=['source'])
                
                data_point = {}
                
                data_point['year'] = year
                if results.values.has_key(Expenditure.SOURCE_JCT):
                    data_point['jct'] = results.values[Expenditure.SOURCE_JCT].get_data(aggregator=sum)
                if results.values.has_key(Expenditure.SOURCE_TREASURY):    
                    data_point['treasury'] = results.values[Expenditure.SOURCE_TREASURY].get_data(aggregator=sum)
                
                data.append(data_point)
            
            
        return render_to_string('tax_expenditures/te_category_summary.html', {'category':category, 'data':data})
    
   

@register.tag
def te_expenditure_summary(parser, token):
    
    tag, expenditure = token.split_contents()
    
    return TEExpenditureNode(expenditure)
    
    
class TEExpenditureNode(Node):
    
    def __init__(self, expenditure):
        self.expenditure_token = Variable(expenditure)
    
    def render(self, context):
        
        expenditure = self.expenditure_token.resolve(context)
        
        cube = expenditure.aggregate()
        
        years = range(2008, 2016)
        
        data = []
        
        for year in years:
            
            if cube.dimensions.has_key('year') and cube.dimensions['year'].values.has_key(year):
            
                results = cube.query(attributes={'year':year}, groups=['source'])
                
                data_point = {}
                
                data_point['year'] = year
                if results.values.has_key(Expenditure.SOURCE_JCT):
                    data_point['jct'] = results.values[Expenditure.SOURCE_JCT].get_data(aggregator=sum)
                if results.values.has_key(Expenditure.SOURCE_TREASURY):    
                    data_point['treasury'] = results.values[Expenditure.SOURCE_TREASURY].get_data(aggregator=sum)
                
                data.append(data_point)
            
            
        return render_to_string('tax_expenditures/te_expenditure_summary.html', {'expenditure':expenditure, 'data':data})

