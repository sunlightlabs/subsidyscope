from twill.commands import go, save_html, reset_browser, fv, submit, get_browser

from BeautifulSoup import BeautifulSoup
import re, os

cert_href = re.compile('confirmation.asp\?inCert1=([0-9]+)')
bhc_cert_href = re.compile('BHClist_cert.asp\?inCert1=([0-9]+)')
completed_certs = {}
pending_certs = []

log = open('log', 'w')

def get_cert(cert):
    
    try:
        if not completed_certs.has_key(cert):
            reset_browser()
        
            go('http://www2.fdic.gov/idasp/ExternalConfirmation.asp?inCert1=%s' % (cert))
            
            log.write(cert)
            
            html = get_browser().get_html()
            bhc_links = bhc_cert_href.findall(html)
            
            if len(bhc_links) > 0:
                get_bhc(cert)
                log.write(' holding\n')
            else:    
                get_bank(cert)
                log.write(' bank\n')
            
            log.flush()
            
    except Exception, e:
        print e

def get_bhc(cert):
    
    try:
        
        if not completed_certs.has_key(cert):
            
            completed_certs[cert] = True
            
            go('http://www2.fdic.gov/idasp/BHClist_cert.asp?inCert1=%s&inSortIndex=0' % (cert))
        
            html = get_browser().get_html()
        
            save_html('%s_hier.html' % (cert))

            cert_links = cert_href.findall(html)
            
            if cert_links is not None:
                for cert_link in cert_links:        
                    pending_certs.append(cert_link)
                
    except Exception, e:
        print e


def get_bank(cert, get_bhc=False):
    
    try:
        
        if not completed_certs.has_key(cert):

            completed_certs[cert] = True

            go('http://www2.fdic.gov/idasp/confirmation.asp?inCert1=%s&AsOf=9/30/2008' % (cert))
            
            html = get_browser().get_html()
            
            bhc_links = bhc_cert_href.findall(html)
            
            if bhc_links is not None:
                for bhc_link in bhc_links:
                    pending_certs.append(bhc_link)
            
            save_html('%s_bank.html' % (cert))
            
            fv('1', 'ReportName', '99')
            submit()
            fv('2', 'ReportName', '99')
            submit()
            
            save_html('%s_report.html' % (cert))
           
            go('http://www2.fdic.gov/sod/sodInstBranchRpt.asp?rCert=%s&baritem=1&ryear=2008' % (cert))
            save_html('%s_sod.html' % (cert))
            
    except Exception, e:
        print e
     


f = open('certs.txt', 'r')

certs = f.read()

f.close()

os.chdir('data')

pending_certs = certs.split('\n')

while len(pending_certs) > 0:
    
    cert = pending_certs.pop()
    get_cert(cert)
    


     
     