from tax_expenditures.models import * 
from django.core.management.base import BaseCommand, make_option

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        groups = Group.objects.filter(parent=None)

        for group in groups:
            print 'Processing %s...' % group.name
            group.calc_detail()
                        






