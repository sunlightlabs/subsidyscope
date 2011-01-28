import pickle
import os
import sys
from cfda.models import ProgramDescription, ProgramDescriptionManager
from django.core.management.base import BaseCommand, make_option
from csv_generator import manager
from datetime import datetime

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-f", "--file", dest="file", default=None),
    )

    def handle(self, *args, **options):
        
        if options['file'] is not None:
            
            ProgramDescription.objects.import_programs(options['file'])
                



# def main():
#     field_counts = {}
#     total_count = 0
#     files = os.listdir(sys.argv[1])
#     for f in files:
#                 
#         p = open(sys.argv[1] + '/' + f,'r')
#         r = pickle.load(p)
#         p.close()
#         
#         filled_fields = 0
#         
#         for field in r:
#             if not field_counts.has_key(field):
#                 field_counts[field] = 0
# 
#             if len(str(field_counts[field]).strip())>0:
#                 field_counts[field] = field_counts[field] + 1
#                 filled_fields += 1
#                     
#         if filled_fields==0:
#             print "%s is empty" % f
#         
#         total_count += 1
#         
#     for f in field_counts:
#         print "%s: %.5f%%" % (f, (100.0 * float(field_counts[f]) / float(total_count)))
#         
# 
# if __name__ == '__main__':
#     main()
