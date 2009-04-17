import csv
import sys
import datetime
import re
import bailout.models
import fdic_bank_failures.models
from decimal import Decimal

def getdatetime(d):
    re_date = re.compile(r'(\d+)[\-\/](\d+)[\-\/](\d+)')
    m = re_date.search(d)
    if m:
        year = int(m.group(1))
        if year<100:
            year = year + 2000
        
        month = int(m.group(2))
        day = int(m.group(3))
        return datetime.datetime(year,month,day)
    else:
        return None

def main():
    """docstring for main"""
    
    re_rangesplitter = re.compile(r'\b([\d\.]+)\b', re.I)
    
    f = open('csv/fund_balances.csv','r')    
    reader = csv.reader(f)
    reader.next() # discard headers
    for row in reader:
        qbp = fdic_bank_failures.models.QBPSnapshot()
        qbp.date = getdatetime(row[0])
        qbp.fund_balance = Decimal(row[1])
        qbp.reserve_ratio = Decimal(row[2])
        qbp.save()
    f.close()
    
    f = open('csv/problem_institutions.csv', 'r')
    reader = csv.reader(f)
    reader.next() # discard headers
    for row in reader:
        row_date = getdatetime(row[0])
        qbp = fdic_bank_failures.models.QBPSnapshot.objects.filter(date=row_date)
        if len(qbp)>0:
            qbp[0].problem_institutions = Decimal(row[1])
            qbp[0].save()
        else:
            print 'did not find matching date for %s' % row[0]        
    f.close()


if __name__ == '__main__':
    main()