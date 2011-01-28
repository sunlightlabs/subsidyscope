from django.core.management.base import BaseCommand, make_option
from fpds.models import *
from sectors.models import Sector

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-f", "--file", dest="file", default=None),
    )

    def handle(self, *args, **options):
        
        if options['file'] is not None:
            
            try:
                data = open(options['file'], 'r')
            except:
                exit('Unable to open %s' % (options['file']))
            
            sector = Sector.objects.get(pk=5)
            
            for line in data.readlines():
                
                code = line.strip()
                    
                psc_codes = ProductOrServiceCode.objects.filter(code=code)
                
                if psc_codes:
                    for psc in psc_codes:
                        psc.sectors.add(sector)
                else:
                    psc = ProductOrServiceCode.objects.create(code=code)
                    
                    psc.sectors.add(sector)