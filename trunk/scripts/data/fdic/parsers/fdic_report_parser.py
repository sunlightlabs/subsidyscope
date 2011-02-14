from BeautifulSoup import BeautifulSoup
from types import StringType
import re, os, string



header = re.compile('<th scope="col" width="22%"><font face=Arial, Helvetica  size="2"><center>(.*?)</center>')
assets = re.compile('<B>Total assets</B> </font></td><td width=22% valign=top align=right><font face=Arial, Helvetica size=2><B>([0-9\,]*)</B>')
regulator = re.compile('size="2">Regulator</font></td>[\s\t]*<td><font face="Arial, Helvetica" size="2">(.*?)</font></td>')

out = open('institutions', 'w')

log = open('log', 'r')
list = log.read().split('\n')

for item in list: 

    item = item.split(' ')
    
    if item[1] == 'bank':
        bank_id = item[0]
        
        if os.path.exists('data/%s_report.html' % (bank_id)):
            
            f = open('data/%s_report.html' % (bank_id), 'r')
            
            data = f.read()
            
            data = data.replace('\n', '')
            
            header_data = header.findall(data)
            header_data = header_data[0].replace('\t', '')
            header_parts = header_data.split('<br>')
            #print header_parts
            
            assets_data = assets.findall(data)
            assets_data = assets_data[0].replace(',', '')
            #print assets_data 
            
            regulator_data = regulator.findall(data)
            #print regulator_data[0]
             
            out.write('%s\t%s\t%s\t%s\t%s\n' % (bank_id, assets_data, regulator_data[0].strip(), header_parts[0].strip(), header_parts[1].strip()))