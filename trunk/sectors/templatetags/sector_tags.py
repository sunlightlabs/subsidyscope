from morsels.models import Morsel
from django.template import Library, Node
from django.template.loader import get_template, get_template_from_string, find_template_source
import settings
import re
from mediasync.templatetags.media import CssTagNode 

register = Library()

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''

class SectorCssNode(CssTagNode):
    def __init__(self, *args, **kwargs):
        #super(SectorCssNode, self).__init__(*args, **kwargs)
	pass

    def render(self, context):
        re_slashes = re.compile(r'(^\/|\/$)')
        path = getattr(context.get('request',{}), 'META', {}).get('PATH_INFO', '')
        url_parts = re_slashes.sub('', path).split('/')
        if len(url_parts) and len(url_parts[0].strip())>0:
            self.media_type = ''	   
	    self.path = "styles/%s.css" % url_parts[0].lower()
            return super(SectorCssNode, self).render(context)
	return ''
        
@register.tag
def sector_css(parser, token):
    tokens = token.split_contents()
    return SectorCssNode()




class SectorNavNode(Node):
    def __init__(self):
        self.template = None
        self.re_slashes = re.compile(r'(^\/|\/$)')

    def render(self, context):
        template_path = "includes/generic_nav.html"
        
        path = getattr(context.get('request',{}), 'META', {}).get('PATH_INFO', '')
        url_parts = self.re_slashes.sub('', path).split('/')

        if len(url_parts) and len(url_parts[0].strip())>0:
            template_path = "includes/%s_nav.html" % url_parts[0].lower()
            
        try:
            self.template = get_template(template_path)
        except Exception, e:
            pass
            
        if self.template:
            return self.template.render(context)
        else:
            return ''

        
        

@register.tag
def sector_nav(parser, token):
    tokens = token.split_contents()
    return SectorNavNode()
    
