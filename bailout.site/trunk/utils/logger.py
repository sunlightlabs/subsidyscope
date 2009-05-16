from django.core.management.color import color_style
from django.core.management.color import no_style
import sys


class Logger():

    def __init__(self, verbosity=1):
        self.verbosity = verbosity

    def info(self, message, threshold=1):
        self._log(message, threshold, sys.stdout, no_style())

    def notice(self, message, threshold=1):
        self._log(message, threshold, sys.stdout, color_style().NOTICE)

    def error(self, message, threshold=1):
        self._log(message, threshold, sys.stderr, color_style().ERROR)

    def _log(self, message, threshold, stream, style):
        if self.verbosity >= threshold:
            stream.write(style("%s\n" % message))
