from BeautifulSoup import BeautifulSoup
from types import StringType
import re, os, string


strip_tags = re.compile(r'<[^>]*?>') 

holding_co = re.compile('<tr><td HEADER=\'column1\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'align=\'right\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column2\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column3\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\' colspan=2><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column4\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'align=\'left\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column5\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column6\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'align=\'right\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column7\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'align=\'right\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td></tr>')

bank = re.compile('<tr><td HEADER=\'column1\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'align=\'right\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column2\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'align=\'left\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column3\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'align=\'left\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column4\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'align=\'left\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column5\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'align=\'left\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column6\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'align=\'left\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column7\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'align=\'right\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td><td HEADER=\'column8\' SCOPE=\'row\' bgcolor=\'[a-z0-9]*\'align=\'right\'><font FACE=\'Arial, Helvetica\' size=\'2\'>(.*?)</font></td></tr>')


out = open('hier_institutions', 'w')

log = open('log', 'r')
list = log.read().split('\n')

for item in list: 

    item = item.split(' ')
    
    if item[1] == 'holding':
        bank_id = item[0]
        
        if os.path.exists('data/%s_hier.html' % (bank_id)):
                    
            f = open('data/%s_hier.html' % (bank_id), 'r')
            
            data = f.read()
            
            holding_co_data = holding_co.findall(data)
            holding_co_data = holding_co_data[0]
            
            holding_co_id = strip_tags.sub('', holding_co_data[0]) 
            
            out.write('%s\t\t%s\t%s\t%s\t%s\t%s\t%s\n' % (holding_co_id, holding_co_data[1], holding_co_data[2], holding_co_data[3], holding_co_data[4], holding_co_data[5].replace(',', ''), holding_co_data[6].replace(',', '')))
            
            data = data.replace('</tr><tr>', '</tr>\n<tr>')
            
            bank_data = bank.findall(data)
            
            for b in bank_data:
                bank_id = strip_tags.sub('', b[0])
                out.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (holding_co_id, bank_id, b[1], b[2], b[3], b[4], b[5], b[6].replace(',', ''), b[7].replace(',', '')))
            
            
             