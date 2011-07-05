from contractcodes.models import NAICS, PSC
from django.core.management.base import BaseCommand, make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-n", "--naicsfile", dest="naics_infile", default=None),
        make_option("-p", "--pscfile", dest="psc_infile", default=None),
        )
    
    def handle(self, *args, **options):
        try:
            NAICS.objects.load_naics(options['naics_infile'])
        except:
            NAICS.objects.load_naics()

        try:
            PSC.objects.load_psc(options['psc_infile'])
        except:
            PSC.objects.load_psc()


