# Django settings for subsidyscope project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jeremy Carbaugh', 'jcarbaugh@sunlightfoundation.com'),
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
if DEBUG:
    MEDIA_URL = '/media/'
else:
    MEDIA_URL = 'http://assets.subsidyscope.com/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '***REMOVED***'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '***REMOVED***'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
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
    'contact_form',
    'sunlightcore',
    'spammer',
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
#MEDIASYNC_AWS_PREFIX = None

def send_welcome_email(recipient):
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    subject = "Welcome to the SubsidyScope"
    message = render_to_string("email/welcome_letter.txt", { "hashcode": recipient.hashcode })
    send_mail(subject, message, "bounce@sunlightfoundation.com", [recipient.email], fail_silently=True)
#MAILINGLIST_SUBSCRIBE_CALLBACK = send_welcome_email
MAILINGLIST_SUBSCRIBED_URL = "/contact/sent/"
MAILINGLIST_REQUIRED_FIELDS = {
    "email":    u"A valid email address is required",
}

try:
    from local_settings import *
except ImportError, exp:
    pass