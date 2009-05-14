from django.core.management.color import no_style
import sys
from utils.logger import Logger

def exit_if(test, message):
    if test:
        log = Logger()
        log.error(message)
        sys.exit(1)
