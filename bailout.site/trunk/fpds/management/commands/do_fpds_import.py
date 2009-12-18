from django.core.management.base import NoArgsCommand
from fpds.models import *

class Command(NoArgsCommand):
    help = "Performs an import of FPDS data (all sectors)."

    def handle_noargs(self, **options):
        f = FPDSLoader()
        f.do_import()