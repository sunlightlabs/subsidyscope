from settings import INSTALLED_APPS, MIDDLEWARE_CLASSES 

DATABASE_ENGINE='mysql'
DATABASE_NAME = 'subsidyscope_scoping' #'subsidyscope_staging_backup_02152011'  #
DATABASE_USER = 'root'
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

DEBUG=True

STATIC_MEDIA_DIR = '/home/kaitlin/envs/subsidyscope/trunk/media/'
MEDIA_ROOT='/home/kaitlin/envs/subsidyscope/trunk/media/'

TEMPLATE_DIRS = (
    '/home/kaitlin/envs/subsidyscope/trunk/templates/',
)

MORSELS_JAVASCRIPT_PATH = ''
INSTALLED_APPS += ( 'django.contrib.admin', 'debug_toolbar', )
MIDDLEWARE_CLASSES += ( 'debug_toolbar.middleware.DebugToolbarMiddleware',)
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = { 'INTERCEPT_REDIRECTS': False }

HAYSTACK_SOLR_URL = 'http://morgan.sunlightlabs.org:8080/solr/core_dev'

#FPDS_IMPORT_MYSQL_SETTINGS = {
#    'host': 'smokehouse',
#    'user': 'subsidyscope',
#    'password': 'tarpsucks',
#    'database': 'fpds_april2010',
#    'port': 3306,
#    'source_table': 'fpds_award3_sunlight'
#}

FPDS_IMPORT_MYSQL_SETTINGS = {
    'host': 'staging.influenceexplorer.com',
    'user': 'usaspend',
    'password': '***REMOVED***',
    'database': 'datacommons',
    'port': 5432,
    'source_table': 'contracts_contract'
}
