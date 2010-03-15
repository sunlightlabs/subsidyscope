from django import template
from django.conf import settings
from django.template import Library, Node, Context, TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import get_template
from helpers.templatetags.custom_filters import camelcase
import re 
register = Library()

def get_subsector_display(active_sector, active_subsector):

    for tuple in settings.SECTORS[active_sector]:
        for sec in tuple:
            if active_subsector == sec[1]:
                return sec[0]

    return camelcase(active_subsector)
                        
class NavigationNode(template.Node):

    def __init__(self, type):
        self.type = type
    

    
    def render(self, context):
        
        current_path = context['request'].path        
        current_page = None
        url_tokens = current_path.strip('/').rstrip('/').split('/')
        nav_depth = len(url_tokens)

        active_sector = url_tokens[0]
        active_subsector = None 
        subsectors = settings.SECTORS[active_sector]
        
        if nav_depth > 1:  
            
            active_subsector = url_tokens[1]    
            
            if nav_depth > 2:  current_page_set = url_tokens[2:]
                
            else: current_page_set = None

        else: active_subsector = None

        if self.type == 'main-nav':

            return get_template('navigation/main-nav.html').render(Context({'active_sector': active_sector ,'sectors': settings.SECTORS.keys()}))

        elif self.type == 'sub-nav':

            
            return get_template('navigation/sub-nav.html').render(Context({'active_subsector': active_subsector, 'subsectors': subsectors }))
             
        elif self.type == 'breadcrumb':
            
            pages = []
            search_pattern = ''

            if current_page_set: 
                #depth is greater than just subsector
                sector_patterns = __import__("%s.urls" % active_sector).urls.urlpatterns
                current_page = current_page_set[len(current_page_set)-1] 
                
                for page in current_page_set:
                    search_pattern += page + '/'
                    for pattern in sector_patterns:

                        exact_patt = re.compile(pattern.regex.pattern+'$')

                        if  exact_patt.match("%s/%s" % (active_subsector, search_pattern) ):
                            #eventually add display name to tuple here
                            pages.append( ( "/%s/%s/%s" % (active_sector, active_subsector, search_pattern), page, ) )

                        elif exact_patt.match(search_pattern):
                            pages.append( ( "/%s/%s" % (active_sector, search_pattern), page, ) )

            else: current_page = active_subsector
                             
                        
            return get_template('navigation/breadcrumb.html').render(Context({'active_sector': active_sector, 'active_subsector': (active_subsector, get_subsector_display(active_sector, active_subsector) ), 'current_page': current_page, 'pages':pages, 'curr':current_page_set }))

        return "%s, %s, %s " % (self.type, active_sector, current_path)
#        try:
#            nav_template = get_template('navigation/%s.html' % self.type)

#            return menu.render(self.context)

#        except TemplateDoesNotExist:
 #           pass            

@register.tag
def navigation(parser, token):

    try:
        tag_name, nav_type = token.split_contents()
    
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires 1 argument" % token.contents.split()[0]

    return NavigationNode(nav_type)
