# Django settings for subsidyscope project.
import os
from django.core.exceptions import ImproperlyConfigured

DEBUG = False
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    ('Kevin Webb', 'kwebb@sunlightfoundation.com'),
    ('Tom Lee','tlee@sunlightfoundation.com'),
    ('Kaitlin Lee','klee@sunlightfoundation.com')
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

MEDIA_CACHE_TTL = 3600 # force browsers to refresh CSS/JS every hour

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
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.webdesign',
    'GChartWrapper.charts',
    'morsels',
    'rcsfield',
    'contact_form',
    'mediasync',
    'spammer',
    'helpers',
    # 'haystack',
    'csv_generator',
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
    'django_helpers',
    'glossary',
    'carousel',
    'search',
    'faads',
    'fpds',
    'budget_accounts',
    'energy',
    'transportation',
    'nonprofits',
    'tagging',
    'aip',
    'news_briefs',
    'cfda',
    'transit',
    'inflation',
    'navigation',
)

#try:
#    INSTALLED_APPS = INSTALLED_APPS + INSTALLED_LOCAL_APPS
#except:
#    pass

EMAIL_HOST = "smtp.sunlightlabs.com"
EMAIL_PORT = "25"
EMAIL_HOST_USER = "***REMOVED***"
EMAIL_HOST_PASSWORD = "***REMOVED***"
EMAIL_USE_TLS = True

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

MEDIASYNC = {
    'BACKEND': 'mediasync.backends.s3',
    'AWS_KEY': "***REMOVED***",
    'AWS_SECRET': "***REMOVED***",
    'AWS_BUCKET': "assets.sunlightlabs.com",
    'AWS_PREFIX': 'subsidyscope',
    'SERVE_REMOTE': False
}



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
    url = "https://api.constantcontact.com/ws/customers/subsidyscope/contacts"
    
    # import urllib2
    
    #     
    #     passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    #     passman.add_password(None, url, user, CONSTANTCONTACT_PASSWORD)
    #     auth = urllib2.HTTPBasicAuthHandler(passman)
    #     opener = urllib2.build_opener(auth)
    #     urllib2.install_opener(opener)
    # 
    #     req = urllib2.Request(url)
    #     req.add_header('Content-Type', 'application/atom+xml')
    #     resp = urllib2.urlopen(req, data=xml)

    import httplib2
    http = httplib2.Http()
    http.add_credentials(user, CONSTANTCONTACT_PASSWORD)
    response, content = http.request(url, 'POST', body=xml, headers={'Content-Type': 'application/atom+xml'})
    
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
HAYSTACK_SEARCH_ENGINE = 'solr' 
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8080/solr'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20
HAYSTACK_FAADS_SEARCH_RESULTS_PER_PAGE = 50
HAYSTACK_FPDS_SEARCH_RESULTS_PER_PAGE = 50
HAYSTACK_SITECONF = 'search_sites'

# Auth 
LOGIN_URL = '/subsidysort/login/'


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


#Navigation configuration - kept in another file to keep settings clean
from navigation.templatetags.navigation_tree import SECTORS



