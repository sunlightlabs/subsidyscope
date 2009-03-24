import csv
import sys
import datetime
import re
import fed_h41.models
from decimal import Decimal
import H41Parser

def getdatetime(d):
    """ converts string YYYY-MM-DD to datetime """
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
    
    reader = csv.reader(sys.stdin)
    reader.next() # discard headers
    
    h41 = H41Parser.H41Parser()
    for row in reader:
        record = { 'Date': getdatetime(row[0]) }
        i = 1
        for collector in h41.collectors:
            if len(row[i]):
                record[collector['label']] = row[i]
            else:
                record[collector['label']] = None
            i = i + 1
        
        snapshot = fed_h41.models.H41Snapshot()
        for field in snapshot._meta.fields:
            if field.verbose_name in record:
                setattr(snapshot, field.name, record[field.verbose_name])
                
        snapshot.save()   

        del record

if __name__ == '__main__':
    main()