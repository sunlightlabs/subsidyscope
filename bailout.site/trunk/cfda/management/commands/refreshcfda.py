import pickle
import os
import sys
from cfda.models import ProgramDescription
from django.core.management.base import BaseCommand, make_option
from csv_generator import manager
from datetime import datetime

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-d", "--directory", dest="directory", default=None),
    )

    def handle(self, *args, **options):
        
        if options['directory'] is not None:
            files = os.listdir(options['directory'])
            for f in files:
                p = open(options['directory'] + '/' + f,'r')
                r = pickle.load(p)
                p.close()

                cfda_program = ProgramDescription.objects.filter(program_number=r['program_number'])

                # previously-recorded program
                if len(cfda_program)>0:
                    cfda_program = cfda_program[0]
                    for field in r:
                        value = r[field]
                        if value is None:
                            value = ''
                        if getattr(cfda_program, field, False):
                            setattr(cfda_program, field, value)
                    
                    cfda_program.load_date = datetime.now()
                    print 'updating %s - %s' % (cfda_program.program_number, cfda_program.program_title)
                    cfda_program.save()

                # new program
                else:
                    cfda_program = ProgramDescription()
                    cfda_program.cfda_edition = datetime.now().year
                    for field in r:
                        value = r[field]
                        if value is None:
                            value = ''
                        try:
                            setattr(cfda_program, field, value)
                        except Exception, e:
                            pass

                    cfda_program.load_date = datetime.now()                            
                    print 'inserting %s - %s' % (r['program_number'], r['program_title'])
                    cfda_program.save()
                            


                    

                
                
                
                
                cfda_program.save()
                



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
