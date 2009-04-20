#!/usr/bin/python

import os
import sys
from BeautifulSoup import BeautifulSoup

def main(filename):
    f = open(filename, 'r')
    b = BeautifulSoup(''.join(f.readlines()))
    f.close()

    tables = b.findAll('table')
    for table in tables[2:-1]:                
        key = False
        value = ''
        rows = table.findAll('tr')
        for row in rows:
            row_contents = ''
            cells = row.findAll('td')
            for cell in cells:
                if len(cell.contents)>0:
                    try:
                        row_contents = row_contents + ''.join(cell.contents).strip()
                    except:
                        pass
            
            if row_contents>0:
                if key:
                    value = value + row_contents
                else:
                    key = row_contents.upper()

        if len(key) and len(value):
            print '%s: %s' % (key, value)
        elif len(key):
            print 'TITLE: %s' % key
            

if __name__ == '__main__':
    main(sys.argv[1])