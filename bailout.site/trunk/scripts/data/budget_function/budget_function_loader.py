import os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from budget_functions.models import BudgetFunction 

code_regex = re.compile('^Code:[\s]+([0-9]{3,3});')
subcode_regex = re.compile('^Subcode:[\s]+([0-9]{3,3});')

function_regex = re.compile('^(Function|Subfunction):(.*)\.')

functions = open('budget_functions.txt', 'r')

code = None
subcode = None
description_parts = []


for line in functions.readlines():
    
    if code_regex.match(line):
        
        if subcode:
            subcode.description = ' '.join(description_parts)
            subcode.save()
            
        elif code:
            code.description = ' '.join(description_parts)
            code.save()
            
        code = None
        subcode = None  
        description_parts = []
        
        match = code_regex.match(line)
        
        code = BudgetFunction.objects.create(code=match.group(1))

    elif subcode_regex.match(line):
        
        if subcode:
            subcode.description = ' '.join(description_parts)
            subcode.save()
            
        elif code:
            code.description = ' '.join(description_parts)
            code.save()
            
        subcode = None  
        description_parts = []
        
        match = subcode_regex.match(line)
        
        subcode = BudgetFunction.objects.create(code=match.group(1), parent=code)
        
        
    elif function_regex.match(line):
        match = function_regex.match(line)
         
        if subcode:
            subcode.name = match.group(2).strip()
            subcode.save()
            
        elif code:
            code.name = match.group(2).strip()
            code.save()
    else:
        
        line = line.strip()
        
        if line != '':
            
            description_parts.append(line)
        else:
            if len(description_parts) > 0:
                description_parts.append('\n\n')
                
        
        
    
    