from django import forms
from django.utils.safestring import mark_safe
from django.utils import simplejson as json
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.forms.util import flatatt
from django.core.urlresolvers import reverse
from rcsfield.backends import backend
import settings

class RcsTextFieldWidget(forms.Textarea):
    """
    Specialized Widget for `RcsTextField`-Fields.
    TODO: implement access to older revisions.
    FIXME: currently unused. may be used later.

    """
    
    def __init__(self, *args, **kwargs):        
        self.field_instance = None
        self.model_instance = None
        super(RcsTextFieldWidget, self).__init__(*args, **kwargs)
    
    
    class Media:
        js = (
            "%sscripts/jquery.js" % settings.MEDIA_URL,
            "%sscripts/rcsfield.js" % settings.MEDIA_URL
            )       

    def render(self, name, value, attrs=None):
        output = []
        output.append(super(RcsTextFieldWidget, self).render(name, value, attrs))

        key = self.field_instance.get_key(self.model_instance)
        revs = self.field_instance.get_changed_revisions(self.model_instance, self.field_instance)
        rev_html = ['<a style="display:block; width: 80%%" href="#HEAD" rel="%s" class="rcsfield-revision">Most Recent</a>' % attrs['id']]
        for rev in revs:
            rev_html.append('<a style="display:block; width: 80%%" href="%s?key=%s&rev=%s" rel="%s" class="rcsfield-revision">%s</a>' % (reverse('rcsfield_get_revision'), key, rev, attrs['id'], rev ))

        if value is not None:
            output.append('<div style="margin-left:106px; height: 100px; width: 300px; padding: 2px;overflow: auto; border: 1px solid #ccc">%s</div>' % ''.join(rev_html))
                    
        return mark_safe(u"\n".join(output))




class JsonWidget(forms.Textarea):
    """
    Needed to make editing RcsJsonField values via contrib.admin possible.
    This widgets casts python types to json strings before displaying them in
    the textarea for editing.

    """
    def render(self, name, value, attrs=None):
        if value is not None:
            value = force_unicode(json.dumps(value))
        else:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))))
