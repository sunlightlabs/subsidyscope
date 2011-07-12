from django.core.management.base import BaseCommand, make_option
from fpds.models import *
from sectors.models import Sector

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-f", "--file", dest="file", default=None),
    )

    def handle(self, *args, **options):
        
        if options['file'] is not None:
            ProductOrServiceCode.objects.load_psc(options['file'])
        else:
            ProductOrServiceCode.objects.load_psc()
                       
