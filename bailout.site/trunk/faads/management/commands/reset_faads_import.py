from django.core.management.base import NoArgsCommand
from faads.models import *

class Command(NoArgsCommand):
    help = "Performs an import of FAADS data."

    def handle_noargs(self, **options):
        f = FAADSLoader()
        f.reset_faads_import()