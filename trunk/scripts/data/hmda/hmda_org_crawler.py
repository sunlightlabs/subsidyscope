import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


import urllib, re
import pyPdf

from BeautifulSoup import BeautifulSoup



from bailout.models import *
from geo.models import *
  
from etl.models import *
from django.core.exceptions import ObjectDoesNotExist

for institution in Institution.objects.filter(id__lt=600):
    
    if institution.fed_number:
        
        rss_id = institution.fed_number
        
        url = 'http://www.ffiec.gov/nicpubweb/nicweb/OrgHierarchySearchForm.aspx?parID_RSSD=%d&parDT_END=99991231' % (rss_id)
        
        
        data = urllib.urlopen(url)
        
        soup = BeautifulSoup(data)
        
        event_validation = soup.find(attrs={'name':'__EVENTVALIDATION'}).attrMap['value']
        view_state = soup.find(attrs={'name':'__VIEWSTATE'}).attrMap['value']
        
        post_parms = {'__EVENTARGUMENT':'',   
                      '__EVENTTARGET':'rbHMDA',    
                      '__EVENTVALIDATION':event_validation,
                      '__LASTFOCUS':'',   
                      '__VIEWSTATE':view_state,
        
                      'grpHMDA':'rbHMDA',
                      'grpInstitution':'rbCurInst',
                      'grpRptFormat':'rbRptFormatPDF',
                      'lbTypeOfInstitution':'-99',
                      'txtAsOfDate':'04/23/2009',
                      'txtAsOfDateErrMsg':''}
        
        encoded_post_parms = urllib.urlencode(post_parms)
        
        data = urllib.urlopen(url,  data=encoded_post_parms)
        
        soup = BeautifulSoup(data)
        
        event_validation = soup.find(attrs={'name':'__EVENTVALIDATION'}).attrMap['value']
        view_state = soup.find(attrs={'name':'__VIEWSTATE'}).attrMap['value']
              
        post_parms = {'__EVENTARGUMENT':'',   
                      '__EVENTTARGET':'rbHMDA',    
                      '__EVENTVALIDATION':event_validation,
                      '__LASTFOCUS':'',   
                      '__VIEWSTATE':view_state,

                      
                      'btnSubmit':'Submit',
                      'grpHMDA':'rbHMDA',
                      'grpInstitution':'rbCurInst',
                      'grpRptFormat':'rbRptFormatPDF',
                      'lbHMDAYear':'2008',
                      'txtAsOfDate':'04/23/2009',
                      'txtAsOfDateErrMsg':''}
         
        encoded_post_parms = urllib.urlencode(post_parms)
        
        output_pdf_file = 'data/2008/org/%d.pdf' % (rss_id)
        output_txt_file = 'data/2008/org/%d.txt' % (rss_id)
        
        urllib.urlretrieve(url, filename=output_pdf_file, data=encoded_post_parms)
        
        try:
            
            content = ""
            
            pdf_file = file(output_pdf_file, "rb")
            pdf = pyPdf.PdfFileReader(pdf_file)
            # Iterate pages
            for i in range(0, pdf.getNumPages()):
                # Extract text from page and add to content
                content += pdf.getPage(i).extractText() + "\n"
    
            out_text = open(output_txt_file, 'w')
            out_text.write(content)
            out_text.close()
            
        except:
            print 'error: %d' % (rss_id)
            pdf_file.close()
            os.remove(output_pdf_file)
        
        
        
