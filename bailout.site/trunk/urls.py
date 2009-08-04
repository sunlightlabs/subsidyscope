from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from contact_form.forms import ContactForm
from bailout.views import *
from project_updates.feeds import ProjectUpdatesFeed
import django.contrib.syndication.views
import haystack 
import csv_generator 

csv_generator.autodiscover()
haystack.autodiscover()
admin.autodiscover()

class SubsidyContactForm(ContactForm):
    attrs_dict = { 'class': 'required' }    
    from_email = "bounce@sunlightfoundation.com"
    recipient_list = ['kwebb@sunlightfoundation.com', 'tlee@sunlightfoundation.com', 'jmorris@sunlightfoundation.com', 'subsidyscope@pewtrusts.org']
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
    url(r'^mailinglist-subscribe/', direct_to_template, {'template': 'misc/email_signup_nojavascript.html'}, name="email_signup_nojavascript"),
    url(r'^mailinglist/', include('spammer.urls')),
	url(r'^projects/bailout/glossary/', include('glossary.urls')),
    
    url(r'^subsidysort/', include('subsidysort.urls')),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'index.html'}, name="index"),   
    url(r'^projects/bailout/', include('bailout.urls')),
    url(r'^crossdomain\.xml$', 'direct_to_template', {'template': 'crossdomain.xml', 'mimetype':'text/x-cross-domain-policy', 'extra_context': {'crossdomain_additions': getattr(settings, 'FLASH_CROSSDOMAIN_ADDITIONS', '')}}, name="crossdomain_xml"),  
    url(r'^projects/', redirect_to_bailout, name="projects"),
    url(r'^updates/', include('project_updates.urls')),
    url(r'^about/', 'direct_to_template', {'template': 'about.html'}, name="about"),
    url(r'^contact/', include('contact_form.urls'), {"form_class": SubsidyContactForm, "fail_silently": False}, name="contact"),
    url(r'^sent/', 'direct_to_template', {'template': 'contact_form/contact_form_sent.html'}, name="contact_sent"),  
    url(r'^feeds/(?P<url>.*)/$', django.contrib.syndication.views.feed, {'feed_dict': {'updates': ProjectUpdatesFeed}}, name="feed_project_updates"),  
    url(r'^data/', 'direct_to_template', {'template': 'misc/data.html'}, name='datasets'),
    url(r'^rss/', 'direct_to_template', {'template': 'misc/rss.html'}, name='about_rss'),
    url(r'^staff/', 'direct_to_template', {'template': 'misc/staff.html'}, name='staff'),
    url(r'^faq/', 'direct_to_template', {'template': 'misc/faq.html'}, name='faq'),
    url(r'^press/', 'direct_to_template', {'template': 'misc/press.html'}, name='press'),
    url(r'^board/', 'direct_to_template', {'template': 'misc/board.html'}, name='board'),
    url(r'^data-quality/$', direct_to_template, { 'template': 'bailout/bailout.html'}, name='data-quality'),
)

urlpatterns += patterns('',
    url(r'^rcsfield/', include('rcsfield.urls'))
)
urlpatterns += patterns('',
    url(r'^morsels/', include('morsels.urls'))
)

urlpatterns += patterns('',
    url(r'^search/', include('search.urls'))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_MEDIA_DIR}),
    )