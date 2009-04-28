from settings import *

DATABASE_ENGINE   = 'mysql'
DATABASE_NAME     = 'ss_staging'
DATABASE_USER     = 'root'
DATABASE_PASSWORD = ''
DATABASE_HOST     = 'localhost'
DATABASE_PORT     = ''

TEMPLATE_DIRS = (
    'templates/',
)

STATIC_MEDIA_DIR = 'media/'

SPAMMER_EXPOSE_LIST = True

GIT_REPO_PATH = '/Users/david/rcsfield-subsidyscope/'

DEBUG = True
