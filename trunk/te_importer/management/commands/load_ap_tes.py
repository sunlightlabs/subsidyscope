#!/usr/bin/env python

import os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Performs an import of FAADS data."

    def handle_noargs(self, **options):
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


from tax_expenditures.models import Category, Expenditure, Estimate

categories = {}

for category in Category.objects.all():
    
    categories[category.name.lower()] = category
    
heading_regex = re.compile('^.*:$')
dot_regex = re.compile('^\.+$')
number_regex = re.compile('^[0-9,]+$')

def recurse_parent_categories(category, expenditure):
    
    if category.budget_function:
        expenditure.budget_function_category.add(category)
    
    if category.parent:
        recurse_parent_categories(category.parent, expenditure)



def process_file(year):
    
    print "processing %d..." % (year) 
    
    file = open ('scripts/data/tax_expenditures/data/omb_ap/spec%d.txt' % (year), 'r')
    
    line_id = 1
    in_line = False
    
    expense_parts = []
    
    category = False
    
    for line in file.readlines():
        line = unicode(line.decode("utf-8"))
        line = line.strip().replace(u'\x96', '-').replace(u'\u20ac', '-').replace(u'\u2013', '-')
        
        if line == '#' and category:
            category = category.parent
        
        if heading_regex.match(line):
            line = line.replace(':', '')
            try:
                category = categories[unicode(line.lower())]
            except:
                print "Missing category: %s" % (unicode(line.lower()))
             
            
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
                                individual_total = int(part.replace(',', ''))
                        elif position < 8:
                            if not dot_regex.match(part):
                                try:
                                    individual_amounts.append(int(part.replace(',', '')))
                                except:
                                    print line
                                    print part
                            else:
                                individual_amounts.append(0)
                        elif position == 8:
                            if not dot_regex.match(part):
                                corp_total = int(part.replace(',', ''))
                        elif position < 16:
                            if not dot_regex.match(part):
                                corp_amounts.append(int(part.replace(',', '')))
                            else:
                                corp_amounts.append(0)
                        
                        position += 1
                    
                    individual_amounts.reverse()
                    corp_amounts.reverse()
                    
                    expense = ' '.join(expense_parts)
                    match_expense = re.sub('[^0-9A-z]', '', expense).lower()
                    
                    
                    expenditure = Expenditure.objects.create(source=Expenditure.SOURCE_TREASURY, category=category, name=expense, match_name=match_expense, item_number=line_id, analysis_year=year)
                    
                    recurse_parent_categories(category, expenditure)
                    
                    if corp_total != sum(corp_amounts[2:]):
                        print "Error in corporate total for %d: %s (%d vs %d)" % (line_id, expense, corp_total, sum(corp_amounts[2:]))
                        
                    
                    if individual_total != sum(individual_amounts[2:]):
                        print "Error in individual total for %d: %s (%d vs %d)" % (line_id, expense, individual_total, sum(individual_amounts[2:]))
                        
                    
                    
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
    
    print "%d TEs" % (line_id - 1) 
                



