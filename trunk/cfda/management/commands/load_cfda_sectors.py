import pickle
import os
import sys
from django.core.management.base import BaseCommand, make_option
from csv_generator import manager
from datetime import datetime


from cfda.models import ProgramDescription, ProgramFunctionalIndex
from sectors.models import Sector


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-f", "--file", dest="file", default=None),
    )

    def handle(self, *args, **options):
        
        if options['file'] is not None:
            
            f = open(options['file'], 'r')
            
            sectors = {}
            
            for sector in Sector.objects.all():
                sectors[sector.id] = sector
            
            for line in f.readlines():
                
                line_parts = line.strip().split(',')
                
                sector_id = int(line_parts[0].strip())
                cfda = line_parts[1].strip()
            
                try:
                    sector = sectors[sector_id]
                except:
                    print "Sector not found: %d" % sector
                    continue
            
                try: 
                    program = ProgramDescription.objects.get(program_number=cfda)
                except:
                    print "Program not found: %s" % cfda 
                    continue
                
                program.sectors.add(sector)
                
                print "%s: %s" % (cfda, sector)
                