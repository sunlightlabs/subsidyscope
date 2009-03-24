#!/usr/bin/python

import csv
import re
import sys
from H41Parser import H41Parser


def main():
    """main loop"""
    
    parser = H41Parser()
    
    re_date = re.compile(r'(\d{4})(\d{2})(\d{2})')
    
    f = open(sys.argv[1])
    file_root = f.readline()

    writer = csv.writer(sys.stdout)
    
    # write headers
    labels = ['date']
    for collector in parser.collectors:
        labels.append(collector['label'])
    writer.writerow(labels)
            
    while file_root:
        file_root = file_root.strip()
        f2 = open('./src/%s.html' % file_root, 'r')
        content = ''.join(f2.readlines())
        f2.close()

        parsed = parser.process_e41(content)
        row = []
        m = re_date.search(file_root)
        if m:
            row.append('%d-%d-%d' % (int(m.group(1)), int(m.group(2)), int(m.group(3))))
        else:
            row.append('')

        # add individual line items
        for collector in parser.collectors:
            row.append(parsed[collector['label']])
        
        if '--debug' in sys.argv:
            for field in parser.out_order:
                print '%s: %s' % (collector['label'], parsed[collector['label']])
        else:
            writer.writerow(row)
            
        file_root = f.readline()

    f.close()


if __name__ == '__main__':
    main()