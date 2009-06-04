from morsels.models import Morsel
from django.template import Library, Node


@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''
