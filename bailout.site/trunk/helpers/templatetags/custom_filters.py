from django import template
import re
from string import capitalize
register = template.Library()

@register.filter
def in_list(value, arg):
    return value in arg


@register.filter
def camelcase(value):
    return " ".join([capitalize(w) for w in re.split(re.compile("[\W_]*"), value)])    
