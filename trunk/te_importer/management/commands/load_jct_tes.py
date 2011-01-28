#!/usr/bin/env python

import os, re, csv
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.management.base import BaseCommand, make_option

class Command(BaseCommand):
    
    help = "Loads raw JCT TE data files from specified path"
    
    option_list = BaseCommand.option_list + (
        make_option("-p", "--path", dest="path", default=None),
    )
    
    def handle(self, *args, **options):
        
        if options['path'] is not None:
            
            path = options['path']
               
            parse_jct(os.path.join(path, 'JCS-1-98.txt'), 2001,  9, 1)
            parse_jct(os.path.join(path, 'JCS-13-99.txt'), 2002, 9, 1)        
            parse_jct(os.path.join(path, 'JCS-1-01.txt'), 2003, 9, 1)
            parse_jct(os.path.join(path, 'JCS-1-05.txt'), 2007, 4, 1)
            parse_jct(os.path.join(path, 'JCS-2-06.txt'), 2008, 4, 1)
            parse_jct(os.path.join(path, 'JCS-3-07.txt'), 2009, 4, 1)
            parse_jct(os.path.join(path, 'JCS-2-08_combined.txt'), 2010, 2, 1)
            parse_jct(os.path.join(path, 'JCS-1-10.txt'), 2011, 2, 5)
            parse_jct(os.path.join(path, 'JCS-3-10.txt'), 2012, 8, 3)
            
        else:
            print 'No --path to data files set.' 


from decimal import Decimal
from te_importer.models import *

re_header_line = re.compile('[\s]+Function[\s]+[\-]+[\s]+')
re_header_year_line = re.compile('([0-9]{4,4})')
re_table_body_line = re.compile('[\-]{152,152}')
re_page_line = re.compile('\[\[Page')

re_indent = re.compile('^([\s]{0,20})')

re_expenditure_figures = re.compile('([\s]?[\\(][\\\\][1-9][\\\\][\\)][\s]?|[\-]*[0-9\.]{1,5}[\s]?|[\s]?[\.]{6,10}[\s]?)')
re_blank = re.compile('[\.]{6,10}')
re_footnote = re.compile('\\\\[0-9,]+\\\\')
re_nonalpha = re.compile('[^A-Za-z]')


grouped_expenditures = {}
categories = {}

def assign_budget_functions(expenditure, category):
    if category.budget_function:
        expenditure.budget_function_category.add(category)
    if category.parent:
        assign_budget_functions(expenditure, category.parent)
    

def parse_jct(path, analysis_year, neg_footnote, pos_footnote):
    
    print('Loading %d data from %s' % (analysis_year, path))
    
    in_header = False
    in_table = False
    in_item = False
    
    years_set = False
    
    indent = -2
    
    stack = []
    
    expenditures = []
    
    years = []
    
    text_break_position = 50
    
    indent_size = None
    
    f = open(path)

    for line in f.readlines():
        
        if in_table:
            
            if len(line.strip()) == 0 or re_page_line.search(line):
                continue
                
            if re_table_body_line.match(line):
                break
            
            indent_match = re_indent.match(line)
            cur_indent = len(indent_match.groups()[0])
            
            text = line[:text_break_position]
            text = re_footnote.sub('', text).strip()
            
            if cur_indent - indent < 0:
                
                pop_count = (cur_indent - indent) / indent_size
            
                stack = stack[:pop_count]
                
                indent = cur_indent - indent_size
                
            
            if cur_indent - indent == 1:
                
                if in_item:
                    
                    if expenditures[-1]['text'][-1] == '-':
                        expenditures[-1]['text'] += text.replace('.', '').replace(':', '')
                    else:
                        expenditures[-1]['text'] += ' ' + text.replace('.', '').replace(':', '')
                        
                else:
                    if stack[-1]['text'][-1] == '-':
                        stack[-1]['text'] += text.replace('.', '').replace(':', '')
                    else:
                        stack[-1]['text'] += ' ' + text.replace('.', '').replace(':', '')
                        
            else:
                
                in_item = False
                
                indent = cur_indent
                
                if not indent_size and cur_indent > 0:
                    indent_size = cur_indent
                
                new_item = {}
                new_item['text'] = text.replace('.', '').replace(':', '')
                
            
                figures = re_expenditure_figures.findall(' ' + line[text_break_position:])
                
                if len(figures) == 11:
                    
                    in_item = True
                    
                    tmp_figures = []
                    
                    for figure in figures:
                        
                        figure = figure.strip().replace('\\', '')
                        
                        if re_blank.match(figure):
                            tmp_figures.append(Decimal('0'))
                        elif figure == '(' + str(pos_footnote) + ')':
                            tmp_figures.append(Decimal('0.01'))
                        elif figure == '(' + str(neg_footnote) + ')':
                            tmp_figures.append(Decimal('-0.01'))
                        else:
                            tmp_figures.append(Decimal(figure))
                            
                    new_item['figures'] = list(tmp_figures)
                    new_item['stack'] = list(stack)
                    
                    expenditures.append(new_item.copy())
                
                else:
                    
                    stack.append(new_item)
    
        else:
            
            if in_header and not in_table:
                
                if not years_set:
                    matches = re_header_year_line.findall(line)
                    years = map(lambda x: int(x), matches[:5])
                    years_set = True
                    
                if re_table_body_line.match(line):
                    in_table = True
                    
            elif re_header_line.search(line):
                pos = 0
                for char in line:
                    pos += 1
                    if char == '-':
                        text_break_position = pos
                        break 
                
                in_header = True
        
     
    for expenditure in expenditures:
        
        name = expenditure['text']
        category_string =  '|'.join(map(lambda x: x['text'], expenditure['stack']))
        
        
        if not categories.has_key(category_string):
            
            parent = None
            stack = []
            
            for category in expenditure['stack']:
                
                category = category['text']
                
                stack.append(category)
                
                stack_string = '|'.join(stack)
                
                if not categories.has_key(stack_string):
                
                    parent, created = Category.objects.get_or_create(name=category, parent=parent)
                    
                    categories[stack_string] = parent
                    
                else:
                    
                    parent = categories[stack_string]
        
        category_object = categories[category_string]
        
        match_name = re_nonalpha.sub('', name).lower()
        
        expenditure_object = Expenditure.objects.create(source=Expenditure.SOURCE_JCT, name=name, match_name=match_name, category=category_object, analysis_year=analysis_year)
        assign_budget_functions(expenditure_object, category_object)
        

        i = 0
            
        for estimate_year in years:
        
            corporations_amount = expenditure['figures'][i] * 1000
            individuals_amount = expenditure['figures'][i + 5] * 1000
        
            Estimate.objects.create(expenditure=expenditure_object, 
                
                                                  estimate_year=estimate_year, 
                                                  corporations_amount=corporations_amount, 
                                                  individuals_amount=individuals_amount)
            i += 1
        