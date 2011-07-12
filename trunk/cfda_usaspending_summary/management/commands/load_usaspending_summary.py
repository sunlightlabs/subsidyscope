from cfda_usaspending_summary.models import *
from django.core.management.base import BaseCommand, make_option

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        print "Loading CFDA summary data from USASpending."
        
        CFDASummary.objects.load_summary_data()