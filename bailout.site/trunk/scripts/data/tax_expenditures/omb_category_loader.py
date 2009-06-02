#!/usr/bin/env python
import os, re
import urllib
from datetime import date
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

indent_regex = re.compile('^-.*')

from tax_expenditures.models import OMBCategory

file = open ('data/omb_ap/omb_categories_2000.txt', 'r')

parent = None

for line in file.readlines():
    line = line.strip()
    
    if indent_regex.match(line):
        line = line.replace('-', '')
        if parent == None:
            parent = last_item
    else:
        parent = None
    
    last_item = OMBCategory.objects.create(name=unicode(line), parent=parent)