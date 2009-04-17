import csv
import sys
import datetime
import re
import bailout.models
import fdic_bank_failures.models
from decimal import Decimal

def getdatetime(d):
    re_date = re.compile(r'(\d+)\/(\d+)\/(\d+)')
    m = re_date.search(d)
    if m:
        year = int(m.group(3))
        if year<100:
            year = year + 2000
        
        month = int(m.group(1))
        day = int(m.group(2))
        return datetime.datetime(year,month,day)
    else:
        return None

def main():
    """docstring for main"""
    
    re_rangesplitter = re.compile(r'\b([\d\.]+)\b', re.I)
    
    reader = csv.reader(sys.stdin)
    for row in reader:
        bf = fdic_bank_failures.models.BankFailure()
        bf.name = row[1].strip()
        bf.city = row[2].strip()
        bf.state = row[3].strip()
        bf.closing_date = getdatetime(row[4])
        bf.updated_date = getdatetime(row[5])
        row[6] = row[6].strip().replace('<','')
        if row[6].lower()=='not available':
            bf.exact_amount = None
        elif re_rangesplitter.search(row[6]):
            # #if it's a range, calculate the middle point
            parts = re_rangesplitter.findall(row[6])
            parts = map(lambda x: Decimal(str(x)), parts)            
            if len(parts)==1:
                bf.exact_amount = parts[0]
            else:            
                bf.range_low = parts[0]
                bf.range_high = parts[1]
        bf.notes = row[7].strip()
        bf.save()

if __name__ == '__main__':
    main()