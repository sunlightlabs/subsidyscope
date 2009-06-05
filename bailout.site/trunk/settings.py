# Django settings for subsidyscope project.
import os
import httplib2
from django.core.exceptions import ImproperlyConfigured

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Kevin Webb', 'kwebb@sunlightfoundation.com'),
    ('Tom Lee','tlee@sunlightfoundation.com'),
    ('David James','djames@sunlightfoundation.com')
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# if DEBUG:
#     MEDIA_URL = '/media/'
# else:
#     MEDIA_URL = 'http://assets.subsidyscope.com/v2'
MEDIA_URL = '/media/' # we're not using mediasync anymore

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '***REMOVED***'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '***REMOVED***'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (    
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.auth'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'middleware.feedburner.FeedburnerMiddleware'
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.webdesign',
    'GChartWrapper.charts',
    'morsels',
    'rcsfield',
    'contact_form',
    'sunlightcore',
    'spammer',
    'haystack',
    #'django_evolution',
    'etl',
    'geo',
    'bailout',
    'bailout_pdfs',
    'project_updates',
    'tarp_subsidy_graphics',
    'fdic_bank_failures',
    'fed_h41',
    'sectors',
    'tax_expenditures',
    'cfda',
    'django_helpers',
    'glossary',
    'carousel'
)


EMAIL_HOST = "smtp.sunlightlabs.com"
EMAIL_PORT = "25"
EMAIL_HOST_USER = "***REMOVED***"
EMAIL_HOST_PASSWORD = "***REMOVED***"
EMAIL_USE_TLS = True

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

MEDIASYNC_AWS_KEY = '***REMOVED***'
MEDIASYNC_AWS_SECRET = '***REMOVED***'
MEDIASYNC_AWS_BUCKET = 'assets.subsidyscope.com'
MEDIASYNC_AWS_PREFIX = 'v2'

# send welcome email -- not used
def send_welcome_email(recipient):
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    subject = "Welcome to the SubsidyScope"
    message = render_to_string("email/welcome_letter.txt", { "hashcode": recipient.hashcode })
    send_mail(subject, message, "bounce@sunlightfoundation.com", [recipient.email], fail_silently=True)

# constant contact API hook -- in use
def constant_contact_signup(recipient):
    """send the user's info to constant contact"""

    CONSTANTCONTACT_API_KEY = 'd233160e-8540-40a4-b28f-b459fecc387b'
    CONSTANTCONTACT_LOGIN = 'subsidyscope'
    CONSTANTCONTACT_PASSWORD = 'yAsw4pre'

    # time on the entry is unimportant -- req'd by ATOM spec, but thrown away by CC
    # contactList is the URI for the "Updates" list    
    xml = """<entry xmlns="http://www.w3.org/2005/Atom">
      <title type="text"> </title>
      <updated>2008-07-23T14:21:06.407Z</updated>
      <author></author>
      <id>data:,none</id>
      <summary type="text">Contact</summary>
      <content type="application/vnd.ctct+xml">
        <Contact xmlns="http://ws.constantcontact.com/ns/1.0/">
          <EmailAddress>%s</EmailAddress>
          <OptInSource>ACTION_BY_CONTACT</OptInSource>
          <ContactLists>
            <ContactList id="http://api.constantcontact.com/ws/customers/subsidyscope/lists/2" />
          </ContactLists>
        </Contact>
      </content>
    </entry>""" % recipient.email
    user = '%s%%%s' % (CONSTANTCONTACT_API_KEY, CONSTANTCONTACT_LOGIN)
    http = httplib2.Http()
    http.add_credentials(user, CONSTANTCONTACT_PASSWORD)
    response, content = http.request('http://api.constantcontact.com/ws/customers/subsidyscope/contacts', 'POST', body=xml, headers={'Content-Type': 'application/atom+xml'})
    
MAILINGLIST_SUBSCRIBE_CALLBACK = constant_contact_signup
MAILINGLIST_SUBSCRIBED_URL = "/mailinglist/subscribed/"
MAILINGLIST_REQUIRED_FIELDS = {
    "email": u"A valid email address is required",
}

# Scribd
SCRIBD_API_KEY = '***REMOVED***'
SCRIBD_API_SECRET = '***REMOVED***'
SCRIBD_PUBLISHER_ID = '***REMOVED***'

# Haystack
HAYSTACK_SEARCH_ENGINE = 'whoosh' 



# RCSField
if DEBUG == True:
    # We rely on the GitPython package ('gitcore')
    RCS_BACKEND = 'gitcore'
elif DEBUG == False:
    # ./manage.py test requires that RCS_BACKEND = 'test'
    RCS_BACKEND = 'test'
else:
    raise ImproperlyConfigured('DEBUG must be either True or False')

# Feedburner
FEEDBURNER = { 'feeds/updates': 'http://feedproxy.google.com/subsidyscope' }

# Django Morsels
MORSELS_USE_JEDITABLE = True

try:
    from local_settings import *
except ImportError, exp:    
    pass
