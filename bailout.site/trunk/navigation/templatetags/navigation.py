from django import template
from django.conf import settings
from django.template import Library, Node, TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import get_template

register = Library()

class NavigationNode(template.Node):

    def __init__(self, type, path):
        self.type = type
    
    def render(self, context):
        
        current_path = context['request'].path        
        
        return current_path
#        try:
#            nav_template = get_template('navigation/%s.html' % self.type)
#
#            return menu.render(self.context)
#
  #      except TemplateDoesNotExist:
   #         pass            

@register.tag
def navigation(parser, token):

    try:
        tag_name, nav_type = token.split_contents()
    
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires 1 argument" % token.contents.split()[0]

    return NavigationNode(type, path)
