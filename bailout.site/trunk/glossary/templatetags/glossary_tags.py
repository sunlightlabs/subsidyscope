from django import template
import glossary.helpers
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.filter
@stringfilter
def glossarize(value):
    """
    Custom template tag.
    A filter.
    """
    return glossary.helpers.glossarize(value)

glossarize.is_safe = True
