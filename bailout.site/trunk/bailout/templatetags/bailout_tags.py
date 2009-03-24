import re

from django import template
from django.template.loader import render_to_string

from bailout.models import Transaction

register = template.Library()

@register.filter
def shorten_name(name):
    
    trimed_name = name.replace(' Incorporated', '').replace(' Inc', '').replace(' Corporation', '').replace(' Corp', '')
            
    trimed_name = re.sub('[^a-z]+$', '', trimed_name)
    
    return trimed_name

@register.filter
def scale_number(number):
    
    try:
        if int(number) > 999999999:
            return str(round(number / 100000000) / 10) + ' billion'
        elif int(number) > 999999: 
            return str(round(number / 100000) / 10) + ' million'
        else:
            return number
        
    except:
        return number
    

@register.filter
def multiply(value, arg):
    "Multiplies the arg and the value"
    #return int(args[0]) * int(args[1])
    if value is None or value=="None":
        return value
    else:
        return int(value) * int(arg)

@register.filter
def divide(value, arg):
    "Divides the value by the arg"
    if value is None or value=="None":
        return value
    else:
        return float(value) / float(arg)


@register.filter
def percent(value, decimals=0):
    
    try:
        # need to handle variable precision  
        return '%d' % int(value * 100)
    except:
        return value

@register.filter
def price(value, decimal='show'):
    
    try:
        if decimal == 'show':
            return '$%.2f' % float(value)
        else:
            return '$%d' % int(value)   
    except:
        return value
    
@register.filter
def price_abs(value, decimal='show'):
    
    try:
        if decimal == 'show':
            return '$%.2f' % float(value)
        else:
            return '$%d' % int(value)
    except:
        return value 
        
@register.tag
def tarp_warrant_tracker(parser, token):
    
    return TARPWarrantTrackerNode()

class TARPWarrantTrackerNode(template.Node):
    
    def render(self, context):
        transactions = Transaction.objects.filter(show_in_tracker=True).order_by('institution__name')
        
        if transactions.count() > 0:
            price_date = transactions[0].getLastPriceUpdateDate()
        
            return  render_to_string('bailout/tarp_warrant_tracker.html', {'price_date':price_date, 'transactions':transactions})
        
        else:
            return ''
    
    
@register.tag
def bank_search(parser, token):
    
    return BankSearchNode()

class BankSearchNode(template.Node):
    
    def render(self, context):
        
        return  render_to_string('bailout/bank_search.html')
    
    
  
#register.filter('multiply', mult)
#register.filter('divide', div)
#register.filter('percent', percent)
#register.filter('price', price)
#register.filter('price_abs', price_abs)


