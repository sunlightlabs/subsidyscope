import sys, os, urllib2, re, csv
sys.path.append('/home/kaitlin/envs/subsidyscope/trunk/')
csv_file_path = '/home/kaitlin/envs/subsidyscope/trunk/data/cfda/'
sys.path.append('/home/kaitlin/envs/subsidyscope/lib/python2.6/site-packages/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import settings
from cfda.models import *

response = urllib2.urlopen('ftp://ftp.cfda.gov')
current = ''
for l in response.readlines():
    file_name = re.findall('programs-full\d+\.csv', l)
    if file_name:
        current = file_name[0]
    elif current:
        break

csv_url = 'ftp://ftp.cfda.gov/' + current
csv_path = csv_file_path + current

if not os.path.isfile(csv_path):
    reader = csv.reader(urllib2.urlopen(csv_url))
    writer = csv.writer(open(csv_path, 'w'))

    for line in reader:
        writer.writerow(line)

    ProgramDescription.objects.import_programs(csv_path)


    
        

