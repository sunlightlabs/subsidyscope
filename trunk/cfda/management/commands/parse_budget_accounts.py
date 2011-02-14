from cfda.models import *
from django.core.management.base import BaseCommand, make_option

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        print "Parsing budget accounts from CFDA data."
        
        ProgramDescription.objects.parseBudgetAccounts()