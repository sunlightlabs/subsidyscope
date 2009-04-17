import sys
import os

bad = 0
total = 0
for f in os.listdir('./pdf'):
    line_count = int(os.popen('pdftotext pdf/%s - 2>/dev/null | wc -l' % f).read().strip())
    if line_count<1:
        bad = bad + 1
        #print '%s: %d' % (f, line_count)
        print f
    total = total + 1

print "%d bad pdfs out of %d" % (bad, total)