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
    
    reader = csv.reader(sys.stdin)
    
    for row in reader:        
        record = { 'date': getdatetime(row[0]), 'text': row[1] }
        news_event = fed_h41.models.FedNewsEvent()
        for k in record:
            setattr(news_event, k, record[k])

        news_event.save()                

if __name__ == '__main__':
    main()