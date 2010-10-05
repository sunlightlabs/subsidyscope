#!/usr/bin/env python
import os
import re
import csv
import urllib
from datetime import date
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from decimal import Decimal
from tax_expenditures.models import Category, Expenditure, Estimate

categories = {}

for category in Category.objects.all():
    
    categories[category.name.lower()] = category
    

heading_regex = re.compile('^.*:$')
dot_regex = re.compile('^\.+$')
number_regex = re.compile('^[0-9,]+$')
spaces_regex = re.compile('[\s]+')
footnotes1_regex = re.compile('\\\\[0-9]+')
footnotes2_regex = re.compile('[0-9]+/')


def check_figures(figures, check_value):

    total = 0

    if check_value == None:
        check_value = 0
    else:
        check_value = abs(check_value)

    for figure in figures:
        if not figure == None:
            total += figure

    total = abs(total)
        
    if total > check_value + (Decimal('50')) or total < check_value - (Decimal('50')):
        return False
    else:
        return True

def clean_line(line):
    return line.strip().replace(u'\x96', '-').replace(u'\u20ac', '-').replace(u'\u2013', '-').replace(u'\xc2-15', '-')

def clean_figure(figure):
    
    if figure == '-' or figure == '' or figure == None:
        return None
    else:
        return Decimal(figure.replace(',', ''))

def clean_name(name):
    
    name = name.strip()
    
    name = footnotes1_regex.sub('', name)
    name = footnotes2_regex.sub('', name)
    
    return name
    
def assign_budget_functions(expenditure, category):
    if category.budget_function:
        expenditure.budget_function_category.add(category)
    if category.parent:
        assign_budget_functions(expenditure, category.parent)
    


def process_file(year):
    
    print year
    file = open ('data/omb_ap/spec%d.txt' % (year), 'r')
    
    line_id = 1
    in_line = False
    
    expense_parts = []
    
    category = False
    
    for line in file.readlines():
        line = unicode(line.decode("utf-8"))
        line = clean_line(line)
        
        if line == '#' and category:
            category = category.parent
        
        if heading_regex.match(line):
            line = line.replace(':', '')
            print line
            try:
                category = categories[unicode(line.lower())]
            except:
                print 'No category match: %s' % line
                return 
            
        if category:
            
            line_regex = re.compile('^%d ' % (line_id))
            line_parts = line.split(' ')
            
            if line_regex.match(line):
                line_parts = line_parts[1:]
                in_line = True
        
            if in_line:
                
                expense_part_count = 0
                
                if not dot_regex.match(line_parts[0]) and not number_regex.match(line_parts[0]):
                    
                    for part in line_parts:
                        if not dot_regex.match(part) and not number_regex.match(part):
                            expense_parts.append(part)
                            expense_part_count += 1
                        else:   
                            break
                
                remaining_line_parts = line_parts[expense_part_count:]
    
                if len(remaining_line_parts) >= 16:
                    
                    remaining_line_parts.reverse()
                    
                    corp_amounts = []
                    corp_total = 0
                    individual_amounts = []
                    individual_total = 0
                    position = 0
                      
                    for part in remaining_line_parts:
                        
                        if position == 0:
                            if not dot_regex.match(part):
                                individual_total += clean_figure(part)
                        elif position < 8:
                            if not dot_regex.match(part):
                                individual_amounts.append(clean_figure(part))
                            else:
                                individual_amounts.append(0)
                        elif position == 8:
                            if not dot_regex.match(part):
                                corp_total += clean_figure(part)
                        elif position < 16:
                            if not dot_regex.match(part):
                                corp_amounts.append(Decimal(clean_figure(part)))
                            else:
                                corp_amounts.append(0)
                        
                        position += 1
                    
                    individual_amounts.reverse()
                    corp_amounts.reverse()
                    
                    name = ' '.join(expense_parts)
                    match_name = re.sub('[^0-9A-z]', '', name).lower()
                    
                    
                    
                    expenditure = Expenditure.objects.create(source=Expenditure.SOURCE_TREASURY, category=category, name=name, match_name=match_name, item_number=line_id, analysis_year=year)
                    assign_budget_functions(expenditure, category)
                    
                    
                    if not check_figures(corp_amounts[2:], corp_total):
                        print "corporate amounts out of bounds for for: %s" % (name)
                    
                    if not check_figures(individual_amounts[2:], individual_total):
                        print "individual amounts out of bounds for for: %s" % (name)
                    
                    
                    for i in range(0, 7):
                        individual_estimate = individual_amounts[i]
                        corp_estimate = corp_amounts[i]
                        
                        estimate_year = year + i - 2
                        
                        Estimate.objects.create(expenditure=expenditure,  
                                                              estimate_year=estimate_year, 
                                                              corporations_amount=corp_estimate,
                                                              individuals_amount=individual_estimate)
                        
                    expense_parts = []
                    in_line = False
                    line_id += 1
    
    file.close()
    
def process_file2010(filename, analysis_year, estimate_years):

    f = open(filename)
    
    line_id = 1
    

    for line in f.readlines():
        line = clean_line(line)
        
        if line == '#' and category:
            category = category.parent
        
        if heading_regex.match(line):
            line = line.replace(':', '')
            print line
            try:
                category = categories[unicode(line.lower())]
            except:
                print 'No category match: %s' % line
                return 
            
            
        if category:
            
            line_regex = re.compile('^%d (.{110,110})' % (line_id))
            line_parts = line_regex.split(line)
            
            if line_regex.match(line):
            
                name = clean_name(line_parts[1])
                
                match_name = re.sub('[^0-9A-z]', '', name).lower()
                
                expenditure = Expenditure.objects.create(source=Expenditure.SOURCE_TREASURY,analysis_year=analysis_year, name=name, match_name=match_name, category=category, item_number=line_id)
                assign_budget_functions(expenditure, category)
                
                figures = line_parts[2].strip()
                
                figure_parts = spaces_regex.split(figures.strip())
                
                if not len(figure_parts) == 16:
                    print 'Missing figures for: %s' % (name)
                    return
                
                figure_parts =  map(lambda x: clean_figure(x), figure_parts)
                
                if not check_figures(figure_parts[2:7], figure_parts[7]):
                    print "corporate amounts out of bounds for for: %s" % (name)
                
                if not check_figures(figure_parts[10:15], figure_parts[15]):
                    print "individual amounts out of bounds for for: %s" % (name)
                
                
                i = 0
                
                for estimate_year in estimate_years:
                    
                    corporations_amount = figure_parts[i] 
                    individuals_amount = figure_parts[i + 8]
                    
                    Estimate.objects.create(expenditure=expenditure, 
                                            estimate_year=estimate_year, 
                                            corporations_amount=corporations_amount, 
                                            individuals_amount=individuals_amount)
                    
                    i += 1 
                
                line_id += 1
                

      

def process_file2011(filename, analysis_year, estimate_years):
    
    f = open(filename, 'rb')
    
    line_id = 1
    
    reader = csv.reader(f)
    
    for row in reader:
        
        heading = clean_line(row[0])
        if heading == '':
            heading = clean_line(row[1])
        
        if heading == '#' and category:
            print heading
            category = category.parent
        
        if heading_regex.match(heading):
            heading = heading.replace(':', '')
            print heading
            try:
                category = categories[unicode(heading.lower())]
            except:
                print 'No category match: %s' % heading
                return
        
        if category:
            
            line_regex = re.compile('^%d' % (line_id))
            
            if line_regex.match(row[0]):
                
                name = clean_name(row[1])
                
                match_name = re.sub('[^0-9A-z]', '', name).lower()
                
                expenditure = Expenditure.objects.create(source=Expenditure.SOURCE_TREASURY,analysis_year=analysis_year, name=name, match_name=match_name, category=category, item_number=line_id)
                assign_budget_functions(expenditure, category)
                
                
                    
                if not len(row[2:]) >= 16:
                    print 'Missing figures for: %s' % (name)
                    return
                
                figure_parts =  map(lambda x: clean_figure(x), row[3:19])
                
                if not check_figures(figure_parts[2:7], figure_parts[7]):
                    print "corporate amounts out of bounds for for: %s" % (name)
                
                if not check_figures(figure_parts[10:15], figure_parts[15]):
                    print "individual amounts out of bounds for for: %s" % (name)
                
                i = 0
                
                for estimate_year in estimate_years:
                    
                    corporations_amount = figure_parts[i] 
                    individuals_amount = figure_parts[i + 9]
                    
                    Estimate.objects.create(expenditure=expenditure, 
                                            estimate_year=estimate_year, 
                                            corporations_amount=corporations_amount, 
                                            individuals_amount=individuals_amount)
                    
                    i += 1 
                
                line_id += 1
                

                
process_file(2000)
process_file(2001)
process_file(2002)
process_file(2003)
process_file(2004)
process_file(2005)
process_file(2006)
process_file(2007)
process_file(2008)
process_file(2009)
process_file2010('data/omb_ap/spec2010.txt', 2010, range(2008,2015))
process_file2011('data/omb_ap/spec2011.txt', 2011, range(2009,2016))     


