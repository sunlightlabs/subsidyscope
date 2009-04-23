from cfda_settings import *
import os

os.popen('rm CFDA.txt')
for i in range(START_PAGE, END_PAGE+1):
    os.popen('cat pages/%d.txt >> CFDA.txt' % i)