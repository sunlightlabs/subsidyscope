from morsels.models import Morsel
from django.template import Library, Node
import settings
import re
from mediasync.templatetags.media import css

register = Library()

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''



class SectorCssNode(Node):
    def __init__(self):
        pass

    def render(self, context):
        re_slashes = re.compile(r'(^\/|\/$)')
        url_parts = re_slashes.sub('', context['request'].META['PATH_INFO']).split('/')
        if len(url_parts):
            return css("styles/%s.css" % url_parts[0].lower())
        return ''
        
@register.tag
def sector_css(parser, token):
    tokens = token.split_contents()
    return SectorCssNode()

    