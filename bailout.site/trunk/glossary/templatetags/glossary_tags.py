from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
import glossary.helpers
register = template.Library()


@register.tag
def glossarize(parser, token):
    """
    Add hyperlinks to matching glossary terms between
    {% glosserize %} content {% endglossarize %}
    """
    
    nodelist = parser.parse(('endglossarize',))
    parser.delete_first_token()
    
    return GlossarizeNode(nodelist)

class GlossarizeNode(template.Node):
    
    def __init__(self, nodelist):    
        self.nodelist = nodelist
        
    def render(self, context):
        
        if context.has_key('glossarize'):
            id_list = context['glossarize']
        else:
            id_list = {}
            
        raw_output = self.nodelist.render(context)
        processed_output, id_list = glossary.helpers.glossarize(raw_output, id_list)
        
        context['glossarize'] = id_list 
        
        return processed_output



@register.simple_tag
def glossary_link(format_string):
    """
    If there is a match, add hyperlink to glossary term.
    """
    return glossary.helpers.glossarize(format_string)
