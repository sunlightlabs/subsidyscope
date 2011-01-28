from BeautifulSoup import BeautifulSoup
from types import StringType
import re, os, string

def clean(val):
    if type(val) is not StringType: val = str(val)
    val = re.sub(r'<.*?>', '', val) #remove tags
    val = re.sub(r'&.*;', '', val) #remove tags
    val = re.sub("\s+" , " ", val) #collapse internal whitespace
    return val.strip() #remove leading & trailing whitespace

p = re.compile('(<form action=sod[\s\S]*</form>)', re.MULTILINE)

out = open('branches', 'w')

log = open('log', 'r')
list = log.read().split('\n')

for item in list: 

    item = item.split(' ')
    
    if item[1] == 'bank':
        bank_id = item[0]
        
        if os.path.exists('data/%s_sod.html' % (bank_id)):
            
            f = open('data/%s_sod.html' % (bank_id), 'r')
           
            data = f.read()
            

            data = p.sub('', data)

           
            soup = BeautifulSoup(data)
         
            state = soup.find('td', attrs={'headers':'hdr_state'})
            #tables = soup.findAll('table')
            if state == None:
                print 'fail'
                exit()
            
            
            if state != None:
                
                print bank_id
                
                table = state.findParent('table')
                
                rows = table.findAll('tr')
                
                state = ''
                county = ''
                
                for row in rows:
                    
                    if row.td != None:
                        
                        if row.td.attrs != None and len(row.td.attrs) and len(row.td.attrs[0]) and row.td.attrs[0][0] == 'headers':
                            
                            if row.td['headers'] == 'hdr_state':
                                state = clean(row.td.contents[0])
                            elif row.td['headers'] == 'hdr_county':
                                county = clean(row.td.contents[0])
                            elif row.td['headers'] == 'hdr_address':    
                                
                                try:
                                    address = clean(row.find('td', attrs={'headers':'hdr_address'}).font.contents[0])
                                except:
                                    address = ''
                                try:
                                    city = clean(row.find('td', attrs={'headers':'hdr_city'}).font.contents[0])
                                except:
                                    city = ''
                                try:
                                    zip = clean(row.find('td', attrs={'headers':'hdr_zip'}).font.contents[0])
                                except:
                                    zip = ''
                                try:
                                    service_type = clean(row.find('td', attrs={'headers':'hdr_brsertyp'}).font.contents[0])
                                except:
                                    service_type = ''
                                try:
                                    office_number = clean(row.find('td', attrs={'headers':'hdr_brnum'}).font.contents[0])
                                except:
                                    office_number = ''
                                try:
                                    unique_number = clean(row.find('td', attrs={'headers':'hdr_UNINUMBR'}).font.contents[0])
                                except:
                                    unique_number = ''
                                try:
                                    deposits = clean(row.find('td', attrs={'headers':'hdr_deposit'}).font.contents[0]).replace(',', '')
                                except:
                                    deposits = ''
                                
                                out.write(bank_id + '|' + address + '|' + city + '|' + county + '|' + state + '|' + zip + '|' + service_type + '|' + office_number + '|' + unique_number + '|' + deposits + '\n')
                
                print bank_id + '*'
                
                f.close()
                out.flush()