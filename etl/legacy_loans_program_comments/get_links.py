#!/usr/bin/python

import re
import sys
import time

def main():
    re_pdf_link = re.compile(r'href=[\'\"](.*?\.pdf)[\'\"]', re.I)
    for row in sys.stdin:
        m = re_pdf_link.search(row)
        if m:
            print m.group(1).strip()


if __name__ == '__main__':
    main()