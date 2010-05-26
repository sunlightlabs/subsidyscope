from django.core.management.base import NoArgsCommand
from faads.models import *

class Command(NoArgsCommand):
    help = "Performs a sample import of FAADS data (all sectors)."

    def handle_noargs(self, **options):
        f = FAADSLoader()
        f.do_import('faads_main_sf_sample')