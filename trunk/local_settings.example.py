from settings import INSTALLED_APPS, MIDDLEWARE_CLASSES

DATABASE_ENGINE='mysql'
DATABASE_NAME = '' #'subsidyscope_staging_backup_02152011'  #
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

DEBUG=True

STATIC_MEDIA_DIR = ''
MEDIA_ROOT=''

TEMPLATE_DIRS = (
    'subsidyscope/trunk/templates/',
)

MORSELS_JAVASCRIPT_PATH = ''
INSTALLED_APPS += ( 'django.contrib.admin', 'debug_toolbar', )
MIDDLEWARE_CLASSES += ( 'debug_toolbar.middleware.DebugToolbarMiddleware',)
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = { 'INTERCEPT_REDIRECTS': False }

HAYSTACK_SOLR_URL = 'localhost:8080'

FPDS_IMPORT_MYSQL_SETTINGS = {
    'host': 'localhost',
    'user': '',
    'password': '',
    'database': '',
    'port': 5432,
    'source_table': 'contracts_contract'
}
