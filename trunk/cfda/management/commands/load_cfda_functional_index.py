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
        make_option("-p", "--path", dest="path", default=None),
    )

    def handle(self, *args, **options):
        
        if options['path'] is not None:
            
            for filename in os.listdir(options['path']):
                
                filepath = os.path.join(options['path'], filename)
                
                code = filename[:1]
                name = filename[2:].split('.')[0]
                
                functional_index, created = ProgramFunctionalIndex.objects.get_or_create(code=code)
                
                if created:
                    functional_index.name = name 
                    functional_index.save()
                    
                f = open(filepath, 'r')
                
                for line in f.readlines()[1:]:
                    
                    line_parts = line.strip().split(',')
                    cfda_number = line_parts[0].strip()
                    
                    try:
                        program = ProgramDescription.objects.get(program_number=cfda_number)
                    except:
                        print "Program not found: '%s'" % cfda_number
                        continue
                
                    program.functional_index.add(functional_index)
                    print "%s: %s" % (cfda_number, code)
                    