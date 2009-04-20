from morsels.models import Morsel

from django.template import Library, Node
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.urlresolvers import reverse
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
                
        js = """
        <script type="text/javascript">
        if(typeof($)=='undefined') { 
            document.write('<script type="text/javascript" src="%sscripts/jquery.js"></' + 'script>');
        }
        </script>
        <script type="text/javascript" src="%sscripts/jquery.jeditable.js"></script>
        <script type="text/javascript">
        $(document).ready(function(){
            $('.jeditable-morsel').each(function(i){
                $(this).editable($(this).attr('rel'), 
                {
                    type      : 'textarea',
                    cancel    : 'Cancel',
                    submit    : 'OK',
                    indicator : 'Saving...',
                    tooltip   : 'Click to edit...'
                });
            });
        });
        </script>
        """ % (settings.MEDIA_URL, settings.MEDIA_URL)
        if self.JS_SIGNAL in context['messages']:
            js = ""

        if morsel is None:
            return u''
        if self.as_var:
            context[self.as_var] = morsel
            return u''
            
        output = typogrify(morsel.content)
        if settings.MORSELS_USE_JEDITABLE and context['user'].is_authenticated():
            output = '%s<div class="jeditable-morsel" id="%s" rel="%s">%s</div>' % (js, self.name, reverse('morsels_ajax_save', None, (urllib.quote(context['request'].path, safe=''),)), output)           
    
        context['messages'].append(self.JS_SIGNAL)

        return mark_safe(output)

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
