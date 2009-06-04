from BeautifulSoup import BeautifulSoup
from types import StringType
import re, os, string

p = re.compile('parID_RSSD=([0-9]+)&')

log = open('rss_ids', 'r')
list = log.readlines()

rss_ids = {}

for item in list: 

    item = item.split(' ')
            
    if len(item) > 1 and item[1] == 'bank':
        
        bank_id = item[0]
        
        if os.path.exists('data/%s_bank.html' % (bank_id)):
            
            f = open('data/%s_bank.html' % (bank_id), 'r')
           
            data = f.read()
            
            result = p.findall(data)
            
            if len(result) == 1:
                #print bank_id + ' ' + result[0]
                rss_ids[result[0]] = True
                
for rss_id in rss_ids.keys():
    print rss_id 
                
            