from te_importer.models import ExpenditureGroup 
from django.core.management.base import BaseCommand, make_option

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        print('Grouping expenditures!')  
        
        ExpenditureGroup.objects.group_expenditures()
                        

