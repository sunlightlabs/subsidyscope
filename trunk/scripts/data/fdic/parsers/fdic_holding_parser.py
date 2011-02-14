from BeautifulSoup import BeautifulSoup
from types import StringType
import re, os, string

p = re.compile('BHClist_cert.asp\?inCert1=([0-9]+)')

log = open('log', 'r')
list = log.read().split('\n')

for item in list: 

    item = item.split(' ')
            
    if item[1] == 'bank':
        
        bank_id = item[0]
        
        if os.path.exists('data/%s_bank.html' % (bank_id)):
            
            f = open('data/%s_bank.html' % (bank_id), 'r')
           
            data = f.read()
            
            result = p.findall(data)
            
            if len(result) == 1:
                print bank_id + ' ' + result[0]
            