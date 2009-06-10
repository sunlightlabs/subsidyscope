import re

from django import template
from django.template import Variable


register = template.Library()

@register.filter
def get_fields(model):
    
    fields = []
    
    for field in model._meta.fields:
        
        field = {'name':field.verbose_name, 'value': getattr(model, field.name)}
    
        fields.append(field)
        
    return fields 
        
        
    