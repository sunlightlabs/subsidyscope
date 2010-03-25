from django import template
from django.core.urlresolvers import reverse, resolve
from django.conf import settings
from django.template import Library, Node, Context, TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import get_template, render_to_string
from helpers.templatetags.custom_filters import camelcase
from morsels.models import *
from copy import deepcopy

import re 
register = Library()

#module level globals to track path of navigation tree traversal

path = []
sectors = []
subsectors = []
dropdowns = []
inner_dropdowns = [] #deprecated - should use context menus instead of having inner dropdowns from now on
breadcrumbs = []
current_url = None
leaf_depth = 1
been_processed = False
last_traverse_level = 0
#initialize the list to the max depth we have and then some
current_tree = [None, None, None, None, None, None]


def traverse(data, callback, url):
    #pre order traversal so we put the callback here
    callback(data, url)

    subsectors = globals()['subsectors']
    
    if not been_processed and traverse.level > 2:
        if traverse.level == 3: subsectors.append('<ul class="sf-menu" id="'+data['sector']+'">')
        subsectors.append('<li id="'+data["url_name"]+'"><a ')
        if data['children']: subsectors.append('class="sf-with-ul" ')
        subsectors.append('href="'+reverse(data["url_name"])+'">'+data["name"]+'</a>')
        if data['children']: subsectors.append('<ul>')

    for child in data['children']:
        traverse.level += 1
        traverse(child, callback, url)
        traverse.level -= 1

    if not been_processed and traverse.level > 2:
        if data['children']: subsectors.append('</ul>')
        subsectors.append('</li>')
        if traverse.level == 3: subsectors.append("</ul>")
        

def main_nav_path(data, url):
    
    #keep track of what our current path is at each nav depth since python dict trees don't really have parent pointers
    current_tree =  globals()['current_tree']
    last_traverse_level = globals()['last_traverse_level']
    current_tree[traverse.level] = (data['name'], reverse(data['url_name']), data['sector'], data['url_name'])
    
    data_structs = [0, 0, 'sectors', 'subsectors', 'dropdowns', 'inner_dropdowns']

    if reverse(data['url_name']) == url:
        #this is the page we're on
        globals()['leaf_depth'] = traverse.level
        globals()['path'] = deepcopy(current_tree)
         
    if not been_processed:
        #append a tuple to the sectors,subsectors, dropdowns, breadcrumb list, depending on the current traversal depth
        try:
            if traverse.level < 3:
                globals()[data_structs[traverse.level]].append((data['name'], reverse(data['url_name']), data['sector'], data['url_name'] ))
            
        except KeyError:
            pass

    current_tree = []  
    last_traverse_level = traverse.level

                       
class NavigationNode(template.Node):

    def __init__(self, type, subnav_id=None):

        self.type = type
        if subnav_id:
            self.subnav_id = template.Variable(subnav_id)
        else:
            self.subnav_id = None

    
    def render(self, context):
        
        #initialize the list to the max depth we have and then some, reset every time render is called
        current_tree = [None, None, None, None, None, None]

        traverse.level = 1
        nav_tree = settings.SECTORS
        try:
            request = context['request']
            url = request.path
        except KeyError:
            request = None
            url = ''

        globals()['path'] = []
        globals()['breadcrumbs'] = []
            
        traverse(nav_tree, main_nav_path, url)
        
        path = globals()['path']
        
        globals()['been_processed'] = True  
        
        if self.type == 'main-nav':
            if url == '/' : active_sector = None  # little hack to make sure there's no active sector on the homepage
            else:
                try:
                    active_sector = path[2]
                except IndexError:
                    active_sector = None

            return get_template('navigation/main-nav.html').render(Context({'active_sector': active_sector, 'sectors': sectors }))

        elif self.type == 'sub-nav':
            subsectors = globals()['subsectors'] 
            return '<style> ul.sf-menu{ display: none;} #'+ path[2][2] +'{display:inline;}</style><div class="span-24"><div id="sector_subnav">' + "".join(subsectors) + '</div></div>'
#            return get_template('navigation/sub-nav.html').render(Context({'active_subsector': path[3] , 'subsectors': subsectors, 'active_sector': path[2], 'request': request }))

        elif self.type == 'dropdown':

            if self.subnav_id:
            
                sub_id = self.subnav_id.resolve(context)
                this_dropdown = []
                temp = []
                for d in globals()['dropdowns']:
                    if reverse(d[2]) == sub_id:
                        #this_dropdown.append(d)
                        temp.append("%s, %s" % (reverse(d[2]), sub_id) )
    
                if len(this_dropdown) > 0:

                    return get_template('navigation/sub-nav-dropdown.html').render(Context({ 'this_dropdown': this_dropdown, 'request': request }))

                else: return temp 

            else: return "no id"
            
         
        elif self.type == 'breadcrumb':                     
            if leaf_depth > 2:

               return get_template('navigation/breadcrumb.html').render(Context({'breadcrumbs': path[2:leaf_depth+1] }))

            else: return ""


@register.tag
def navigation(parser, token):

    try:
        tag_name, nav_type = token.split_contents()
        return NavigationNode(nav_type)

    except ValueError:
    
        try: 
            tag_name, nav_type, subnav_id = token.split_contents()
            
            return NavigationNode(nav_type, subnav_id)

        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires at least 1 argument" % token.contents.split()[0]


