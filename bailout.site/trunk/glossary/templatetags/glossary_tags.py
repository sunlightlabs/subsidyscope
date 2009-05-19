from django import template
import glossary.helpers
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.filter
@stringfilter
def glossarize(value):
    """
    Add hyperlinks to specific glossary terms.
    """
    return glossary.helpers.glossarize(value)

glossarize.is_safe = True
