from math import ceil
from itertools import chain
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms import CheckboxInput

        

class CheckboxSelectMultipleMulticolumn(forms.CheckboxSelectMultiple):

    def __init__(self, attrs=None, columns=1, *args, **kwargs):
        if attrs:
            self.attrs.update(attrs)
        self.columns = columns
        super(CheckboxSelectMultipleMulticolumn, self).__init__(attrs, *args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        
        output = []

        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
    
        # where to drop in the <ul> breaks
        every = ceil((len(choices) + len(self.choices)) / float(self.columns))

        output.append(u'<ul>')

        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            # option_label = conditional_escape(force_unicode(option_label))
            option_label = force_unicode(option_label)        
            output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
            
            if (i % every)==(every-1):
                output.append(u'</ul><ul>')

        output.append(u'</ul>')
            
        return mark_safe(u'\n'.join(output))