from django.core.management.base import NoArgsCommand
from fpds.models import *

class Command(NoArgsCommand):
    help = "Deletes all imported FPDS data."

    def handle_noargs(self, **options):
        f = FPDSLoader()
        f.reset_fpds_import()