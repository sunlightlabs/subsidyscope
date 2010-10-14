#!/usr/bin/env python

import os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.management.base import NoArgsCommand

from tax_expenditures.models import Category

class Command(NoArgsCommand):
    help = "Performs an import of tax expenditure categories from Analytical Perspectives."

    def handle_noargs(self, **options):
        indent_regex = re.compile('^-.*')

        file = open ('scripts/data/tax_expenditures/data/omb_ap/omb_categories_2000.txt', 'r')
        
        parent = None
        last_item = None
        
        for line in file.readlines():
            line = line.strip()
            
            if indent_regex.match(line):
                line = line.replace('-', '')
                if parent == None:
                    parent = last_item
            else:
                parent = None
            
            last_item = Category.objects.create(name=unicode(line), parent=parent, budget_function=True)
            
        
        





