#!/bin/python

from bailout.models import *
import csv
import re
from TarpReader import TarpReader

if __name__ == "__main__":

    mode = None

    TR = TarpReader()

    reader = csv.reader(sys.stdin)
    writer = csv.writer(sys.stdout)

    for line in reader:
        if len(line)>=len(TR.GOVERNMENT_CSV_LAYOUT):
            processed_line = TR.convert_government_csv_line(line)
            if processed_line:
                row = []
                for f in TR.CSV_LAYOUT:
                    row.append(processed_line[f])
                writer.writerow(row)