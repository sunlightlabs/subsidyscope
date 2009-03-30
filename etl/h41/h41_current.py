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
    for collector in parser.collectors:
        labels.append(collector['label'])
    writer.writerow(labels)
           
    http = httplib2.Http()
    resp, content = http.request('http://www.federalreserve.gov/Releases/H41/Current/', 'GET')                
    
    parsed = parser.process_e41(content)
    row = []
    m = re_date.search(sys.argv[1])
    if m:
        row.append('%d-%d-%d' % (int(m.group(1)), int(m.group(2)), int(m.group(3))))
    else:
        print >>sys.stderr, "ERROR: did you specify the YYYYMMDD string as the script's first argument?"
        return 1

    # add individual line items
    for collector in parser.collectors:
        row.append(parsed[collector['label']])
    
    if '--debug' in sys.argv:
        for field in parser.out_order:
            print '%s: %s' % (collector['label'], parsed[collector['label']])
    else:
        writer.writerow(row)


if __name__ == '__main__':
    main()