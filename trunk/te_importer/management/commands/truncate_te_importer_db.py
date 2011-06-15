#!/usr/bin/env python

import os, csv
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.management.base import BaseCommand, make_option
from django.db import connection, transaction
from decimal import Decimal

from te_importer.models import Category, Expenditure, Estimate, ExpenditureGroup

years = range(2000, 2016)

te_tables = ['te_importer_category', 'te_importer_expenditure', 'te_importer_estimate', 'te_importer_expendituregroup']

class Command(BaseCommand):
    help = "Loads processed TE data files from specified path"
    
    option_list = BaseCommand.option_list + (
        make_option("-p", "--path", dest="path", default=None),
    )

    def handle(self, *args, **options):
            
        print 'Truncating TE database...'
        
        Category.objects.all().delete()
        ExpenditureGroup.objects.all().delete()
        Expenditure.objects.all().delete()
        Estimate.objects.all().delete() 
        
        cursor = connection.cursor()
    
        # Data modifying operation - commit required
        for table in te_tables:
            cursor.execute("ALTER TABLE %s auto_increment=1;" % table)
            transaction.commit_unless_managed()