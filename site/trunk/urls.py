from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from contact_form.forms import ContactForm

admin.autodiscover()

class SubsidyContactForm(ContactForm):
    
    attrs_dict = { 'class': 'required' }
    
    from_email = "bounce@sunlightfoundation.com"
    recipients = ['contact@sunlightfoundation.com','jcarbaugh@sunlightfoundation.com','tlee@sunlightfoundation.com']
    subject = "[SubsidyScope.com] Contact form submission"
    
    name = forms.CharField(max_length=100,
                widget=forms.TextInput(attrs=attrs_dict),
                label=u'Name')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=200)),
                label=u'Email Address')
    body = forms.CharField(widget=forms.Textarea(attrs=attrs_dict),
                label=u'Comment')

urlpatterns = patterns('',
    url(r'^admin/(.*)', admin.site.root),
    url(r'^mailinglist/', include('spammer.urls')),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'index.html'}, name="index"),
    url(r'^contact/', include('contact_form.urls'), {"form_class": SubsidyContactForm, "fail_silently": False}, name="contact"),
    url(r'^sent/', 'direct_to_template', {'template': 'contact_form/contact_form_sent.html'}, name="contact_sent"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
    )