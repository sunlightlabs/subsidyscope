#!/bin/python

from bailout.models import *
import csv
import re
from TarpReader import TarpReader

if __name__ == "__main__":

    mode = None

    TR = TarpReader()

    # compose ignore list
    ignore_list = []
    for i in range(0, len(sys.argv)-1):
        if sys.argv[i]=='--ignore':
            f = open(sys.argv[i+1],'r')
            reader = csv.reader(f)
            for row in reader:
                if row!=TR.CSV_LAYOUT:
                    ignore_list.append(row)
            f.close()
            

    line = sys.stdin.readline()
    writer = csv.writer(sys.stdout)
    row = []
    for f in TR.CSV_LAYOUT:
        row.append(f)
    writer.writerow(row)
    while line:
        processed_line = TR.process_line(line, ignore=ignore_list)
        row = []
        if processed_line:
            for f in TR.CSV_LAYOUT:
                row.append(processed_line[f])
            writer.writerow(row)
        line = sys.stdin.readline()