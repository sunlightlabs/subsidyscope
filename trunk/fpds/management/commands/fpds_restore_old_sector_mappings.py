from sectors.models import *
from fpds.models import NAICSCode, ProductOrServiceCode
import csv
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Loads contract code mappings for sectors 4 and 5"

    def handle_noargs(self, **options):

        psc_code_map = csv.reader(open('data/psc/psc_sector_map.csv'))
        naics_code_map = csv.reader(open('data/naics/sector_naics_map.csv'))

        psc_code_map.next()
        naics_code_map.next()

        for row in psc_code_map:
            code = row[0]
            sect = row[1]
            s = Sector.objects.get(id=sect)
            try:
                c = ProductOrServiceCode.objects.get(code=code)
                if s:
                    c.sectors.add(s)
            
            except ObjectDoesNotExist as e:
                print code
                c = ProductOrServiceCode(code=code, name='')
                c.save()
                c.sectors.add(s)

        for row in naics_code_map:
            code = row[0]
            sect = row[1]
            s = Sector.objects.get(id=sect)
            try:
                c = NAICSCode.objects.get(code=code)
                if s:
                    c.sectors.add(s)
            
            except ObjectDoesNotExist as e:
                print code
                c = NAICSCode(code=code, name='')
                c.save()
                c.sectors.add(s)

