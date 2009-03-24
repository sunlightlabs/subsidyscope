#!/usr/bin/python

import csv
import re
import sys
import httplib2
from H41Parser import H41Parser

def main():
    """main loop"""
    
    parser = H41Parser()
    
    re_date = re.compile(r'(\d{4})(\d{2})(\d{2})')
    
    writer = csv.writer(sys.stdout)
    
    # write headers
    labels = ['date']
    for field in parser.out_order:
        labels.append(field)

    writer.writerow(labels)
            
    url = sys.argv[1].strip()

    http = httplib2.Http()
    resp, content = http.request(url, 'GET')

    parsed = parser.process_e41(content)
    row = []
    m = re_date.search(url)
    if m:
        row.append('%d-%d-%d' % (int(m.group(1)), int(m.group(2)), int(m.group(3))))
    else:
        row.append('')

    # add individual line items
    for field in parser.out_order:
        row.append(parsed[field])
    
    writer.writerow(row)
              


if __name__ == '__main__':
    main()