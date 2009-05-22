from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
import glossary.helpers
register = template.Library()


@register.filter
@stringfilter
def glossarize(value):
    """
    Add hyperlinks to matching glossary terms.
    """
    return glossary.helpers.glossarize(value)

glossarize.is_safe = True


@register.simple_tag
def glossary_link(format_string):
    """
    If there is a match, add hyperlink to glossary term.
    """
    return glossary.helpers.glossarize(format_string)
