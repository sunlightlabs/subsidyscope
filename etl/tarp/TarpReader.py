from bailout.models import *
import csv
import re

class TarpReader():
    
    def __init__(self):
        self.CSV_LAYOUT = [
            'transaction_date',
            'transaction_transaction_type',
            'transaction_description',
            'transaction_price_paid',
            'transaction_pricing_mechanism',
            'institution_is_new',
            'institution_existing_id',
            'institution_name',
            'institution_existing_name',
            'institution_city',
            'institution_existing_city',
            'institution_state',
            'institution_existing_state',
            'institution_institution_type'
        ]
        
        self._re_is_transaction = re.compile(r'^([\d]+)\/([\d]+)\/([\d]+)\s+(\w[\w\s\&\,\.\'\-]+)\s{3,}(\w[\w\s\'\.\-\&]+)\s{3,}([A-Z]{2})\s{3,}(\w[\w\s]+)\s{3,}(\w[\w\s\/]+)\s{3,}\$?([\d\,]+)\s+(\w[\w\s\/]+)$')
        self._re_is_classification_line = re.compile(r'^\s{50,}([A-Z\s]+?)$')
        self._re_typo_garbage = re.compile(r'^\s*\d{1,2}\/?\s{5,}')
        self._re_name_normalization = re.compile(r'\,?\s+\b(Inc|LLC|Corp|Corporation|Company|Bank|Group)\b\.?', re.I)
    
    def get_empty_record(self):
        r = {}
        for f in self.CSV_LAYOUT:
            r[f] = None
        return r
    
    def process_line(self, line, ignore=[]):
        """processes a single line of input"""
        # remove general crud (footnotes) and TARP-specific date typo. it's a weird one.
        line = self._re_typo_garbage.sub('',line)
        line = line.replace('QQQ','')
        
        # check for a new classification set, e.g. "AUTOMOTIVE INDUSTRY FINANCING PROGRAM"
        classification = ''
        l_classification = self._is_classification_line(line)
        if l_classification:
            classification = l_classification
        
        # strip whitespace -- we're done with it
        line = line.strip()
        
        # identify whether this is a transaction line item; if so, retrieve its data
        line_item = self._process_transaction_line(line)
        
        #print line
        
        # was this a transaction line item?
        if line_item:            
            
            # create an empty row
            r = self.get_empty_record()
            
            line_item['institution_type'] = classification # simplifies some code below            
            
            # look for an existing institution that matches this one
            normalized_name = self._re_name_normalization.sub('',line_item['name'])
            possible_institution_matches = Institution.objects.filter(name__icontains=normalized_name, city=line_item['city'], state=line_item['state'])
            if possible_institution_matches.count()==0:
                r['institution_is_new'] = 'YES'
            else:
                r['institution_is_new'] = 'NO'
                r['institution_existing_id'] = possible_institution_matches[0].id
                r['institution_existing_name'] = possible_institution_matches[0].name
                r['institution_existing_city'] = possible_institution_matches[0].city
                r['institution_existing_state'] = possible_institution_matches[0].state
            for f in ['name', 'institution_type', 'city', 'state']:
                r['institution_%s' % f] = line_item[f]
            
            # copy line item contents into transaction record
            for f in ['date', 'transaction_type', 'description', 'price_paid', 'pricing_mechanism']:
                r['transaction_%s' % f] = line_item[f]
            
            # look for matching transactions if this is a known institution
            if r['institution_is_new']=='NO':
                possible_transaction_matches = Transaction.objects.filter(institution__id=r['institution_existing_id'], date=line_item['date'])
                if possible_transaction_matches.count()>0:
                    return False
            
            # check to see if the calculated row is in the ignore list
            for ignore_row in ignore:
                # convert r (dict) to row, accounting for types
                r_as_row = []
                for f in self.CSV_LAYOUT:
                    if type(r[f])==datetime.datetime:
                        r_as_row.append(r[f].isoformat(' '))
                    elif r[f]==None:
                        r_as_row.append('')
                    else:
                        r_as_row.append(r[f])

                if r_as_row==ignore_row:
                    return False

            # return the row
            return r
        
        else:
            return False    
        

    
    def _process_transaction_line(self,line):
        """ Tests whether the submitted line of the TARP report looks like a transaction. Returns a dict of strings. """
        m = self._re_is_transaction.match(line)
        if m:
            year = m.group(3).strip().replace('000','00') # Treasury = dumb
            date = datetime.datetime(int(year), int(m.group(1).strip()), int(m.group(2).strip()))
            name = m.group(4).strip()
            city = m.group(5).strip()
            state = m.group(6).strip()
            transaction_type = m.group(7).strip()
            description = m.group(8).strip()
            price_paid = m.group(9).replace(',','').strip()
            pricing_mechanism = m.group(10).strip()
            return {'date':date, 'name':name, 'city':city, 'state':state, 'transaction_type':transaction_type, 'description':description, 'price_paid':price_paid, 'pricing_mechanism':pricing_mechanism}
        else:
            return False

    
    def _is_classification_line(self,line):
        """ Tests whether the submitted line of the TARP report designates a new class of transations. If so, return the appropriate string. If not, return None. """
        m = self._re_is_classification_line.match(line)
        if m!=None:
            return m.group(1).strip()
        else:
            return False