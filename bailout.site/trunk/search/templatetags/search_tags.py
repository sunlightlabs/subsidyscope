from django.utils.encoding import *
from django.template import Library, Node
from django.utils.safestring import mark_safe
from django.conf import settings

register = Library()

@register.filter
def safe_highlight(value):
    """
    A "safe" filter for sequences. Marks each element in the sequence,
    individually, as safe, after converting them to unicode. Returns a list
    with the results.
    """
    try:
        return mark_safe(value[0])
    except:
        return value 

safe_highlight.is_safe = True

