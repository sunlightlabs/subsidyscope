from morsels.models import Morsel, Page
from django.template import Library, Node
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Template
import urllib 

typogrify = lambda a: a
try:
    if not getattr(settings, 'MORSELS_NO_TYPOGRIFY', False):
        settings.INSTALLED_APPS.index('typogrify')
        from typogrify import typogrify
except ValueError:
    pass

register = Library()

class MorselNode(Node):

    JS_SIGNAL = '<!-- ADDED JS -->'

    def __init__(self, name, as_var, inherit):
        self.name = name
        self.as_var = as_var
        self.inherit = inherit

    def render(self, context):  
                
        morsel = Morsel.objects.get_for_current(context, self.name, self.inherit)
        
        if getattr(settings,'MORSELS_USE_JEDITABLE',False):
            js = """
            <script type="text/javascript">
            if(typeof(jQuery)=='undefined') { 
                document.write('<script type="text/javascript" src="%sjquery.js"></' + 'script>');
            }
            </script>
            <script type="text/javascript" src="%sjquery.jeditable.js"></script>
            <script type="text/javascript">
            jQuery(document).ready(function(){
                jQuery('.jeditable-morsel').each(function(i){
                    jQuery(this).editable(jQuery(this).attr('rel'), 
                    {
                        type      : 'textarea',
                        cancel    : 'Cancel',
                        submit    : 'OK',
                        indicator : 'Saving...',
                        tooltip   : 'Double-click to edit...',
                        event     : 'dblclick',
                        loadurl   : '%s'                                                
                    });
                });
            });
            </script>
            """ % (settings.MORSELS_JAVASCRIPT_PATH, settings.MORSELS_JAVASCRIPT_PATH, reverse('morsels_ajax_load', None, (urllib.quote(context['request'].path, safe=''),)))
            if self.JS_SIGNAL in context['messages']:
                js = ""
            
        if morsel is None:
            return u''
        if self.as_var:
            context[self.as_var] = morsel
            return u''
            
        output = typogrify(morsel.content)
        if getattr(settings,'MORSELS_USE_JEDITABLE',False) and context['user'].is_authenticated():
            output = '%s<div class="jeditable-morsel" id="%s" rel="%s"><div class="jeditable-morsel-label"></div>%s</div>' % (js, self.name, reverse('morsels_ajax_save', None, (urllib.quote(context['request'].path, safe=''),)), output)           
            context['messages'].append(self.JS_SIGNAL)


        output_template = Template(output) 
        
        return mark_safe(output_template.render(context))

    render.allow_tags = True


@register.tag
def morsel(parser, token):
    tokens = token.split_contents()

    try:
        as_tag = tokens.index(u'as')
        as_var = tokens[as_tag + 1]
        del tokens[as_tag]
        del tokens[as_tag]
    except (ValueError, IndexError):
        as_var = None

    try:
        tokens.remove(u'inherit')
        inherit = True
    except ValueError:
        inherit = False

    name = len(tokens) > 1 and tokens[1] or u''
    if name and name[0] in (u'"', u"'") and name[-1] == name[0]:
        name = name[1:-1]

    return MorselNode(name, as_var, inherit)


class MorselPageTitleNode(Node):

    JS_SIGNAL = '<!-- ADDED JS -->'

    def __init__(self, show_sector, page_title):
        self.page_title = page_title
        self.show_sector = show_sector
        

    def render(self, context):  
        
        page = Page.objects.get_for_current(context, u'', False)
        
        if page:
        
            title = page.title
            
            if self.show_sector and page.sector:
                title = page.sector.name + ': ' + title
            
            if self.page_title:
                return ' &mdash; ' + title
            else:
                return title
        
        else:
            return ''

@register.tag
def morsel_page_title(parser, token):
    tokens = token.split_contents()

    try:
        tokens.remove(u'show_sector')
        show_sector = True
    except ValueError:
        show_sector = False
        
    try:
        tokens.remove(u'page_title')
        page_title = True
    except ValueError:
        page_title = False

    return MorselPageTitleNode(show_sector, page_title)


class MorselSectorTitleNode(Node):

    JS_SIGNAL = '<!-- ADDED JS -->'

    def __init__(self, page_title):
        self.page_title = page_title

    def render(self, context):  
                
        page = Page.objects.get_for_current(context, u'', False)
        
        if page:
            if page.sector:
                if self.page_title:
                    return ' &mdash; ' + page.sector.name
                else:
                    return page.sector.name
        else:
            return ''



@register.tag
def morsel_sector_title(parser, token):
    
    tokens = token.split_contents()

    try:
        tokens.remove(u'page_title')
        page_title = True
    except ValueError:
        page_title = False

    return MorselSectorTitleNode(page_title)

class WithMorselNode(Node):
    def __init__(self, name, as_var, inherit, nodelist):
        self.name = name
        self.as_var = as_var
        self.inherit = inherit
        self.nodelist = nodelist

    def __repr__(self):
        return '<WithMorselNode>'

    def render(self, context):
        morsel = Morsel.objects.get_for_current(context, self.name, self.inherit)
        if morsel is None:
            return u''

        context.push()
        context[self.as_var] = morsel
        output = self.nodelist.render(context)
        context.pop()
        return output

@register.tag
def withmorsel(parser, token):
    tokens = token.split_contents()

    try:
        as_tag = tokens.index(u'as')
        as_var = tokens[as_tag + 1]
        del tokens[as_tag]
        del tokens[as_tag]
    except (ValueError, IndexError):
        as_var = 'morsel'

    try:
        tokens.remove(u'inherit')
        inherit = True
    except ValueError:
        inherit = False

    name = len(tokens) > 1 and tokens[1] or u''
    if name and name[0] in (u'"', u"'") and name[-1] == name[0]:
        name = name[1:-1]

    nodelist = parser.parse(('endwithmorsel',))
    parser.delete_first_token()
    return WithMorselNode(name, as_var, inherit, nodelist)
