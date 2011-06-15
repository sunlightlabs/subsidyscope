#!/usr/bin/env python

import os, re, csv
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.management.base import BaseCommand, make_option

from te_importer.models import Category

class Command(BaseCommand):
    
    help = "Loads TE categories from text file (e.g. scripts/data/tax_expenditures/data/omb_ap/omb_categories_2000.txt)"
    
    option_list = BaseCommand.option_list + (
        make_option("-p", "--path", dest="path", default=None),
    )

    def handle(self, *args, **options):
        
        if options['path'] is not None:   
            indent_regex = re.compile('^-.*')

            file = open (options['path'], 'r')
            
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
        else:
            print ('No --path to categories file specified (probably need scripts/data/tax_expenditures/data/omb_ap/omb_categories_2000.txt).')
            exit()
        
        
        
            



