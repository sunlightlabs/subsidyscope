from django.core.management.base import NoArgsCommand
from fpds.models import *

class Command(NoArgsCommand):
    help = "Performs a sample import of FPDS data."

    def handle_noargs(self, **options):
        f = FPDSLoader()
        f.do_import('fpds_award3_sf_sample')