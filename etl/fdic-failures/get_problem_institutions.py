import re
import BeautifulSoup
import sys
import csv
from decimal import Decimal


class FDICProblemInstitutionParser(object):
    """FDIC-parsing class"""
    def __init__(self):
        super(FDICProblemInstitutionParser, self).__init__()
        self.re_number_table_cell = re.compile(r'>\s*([\-\$]{0,2}[\d\.\,]+)\s*<')
        self.re_problem_institutions_label = re.compile(r'>\s*Problem Institutions\s*<', re.I)
        self.re_number_of_institutions = re.compile(r'>\s*Number of institutions', re.I)
        
        self.month_map = {
            1: 'jan',
            2: 'feb',
            3: 'mar',
            4: 'apr',
            5: 'may',
            6: 'jun',
            7: 'jul',
            8: 'aug',
            9: 'sep',
            10: 'oct',
            11: 'nov',
            12: 'dec'
        }
        
        
    def find_first_number_in_row(self, beautifulsoup_row):
        """Finds the number in the first column of a BeautifulSoup table row"""
        for td in beautifulsoup_row.findAll('td'):
            match = self.re_number_table_cell.search(str(td))
            if match:
                return match.group(1).replace(',','').replace('$','')
        
        return None
        
    def get_problem_institution_data_from_table(self, table_html):
        """docstring for get_problem_institution_data_from_table"""
        b = BeautifulSoup.BeautifulSoup(table_html)
        found_problem_institutions_label = False
        found_num_institutions = False
        num_problem_institutions = 0
        for tr in b.findAll('tr'):
            if self.re_problem_institutions_label.search(str(tr)):
                found_problem_institutions_label = True
                continue
            if found_problem_institutions_label:
                for td in tr.findAll('td'):
                    if self.re_number_of_institutions.search(str(td)):
                        num_problem_institutions = self.find_first_number_in_row(tr)
                        found_num_institutions = True
            if found_num_institutions:
                break
                
        return num_problem_institutions
        

def parse_local_files():
    MONTHS = [3, 6, 9, 12]
    parser = FDICProblemInstitutionParser()
    writer = csv.writer(sys.stdout)
    writer.writerow(['date', 'number of problem institutions'])
    for y in range(2003, 2009):
        for m in MONTHS:
            f = open('./dep2b/%d%s.html' % (y, parser.month_map[m]), 'r')

            num_problem_institutions = parser.get_problem_institution_data_from_table(table_html=''.join(f.readlines()))
            row = ['%d-%d-1' % (y, m), num_problem_institutions]
            writer.writerow(row)                    

            f.close()

if __name__ == '__main__':
    if '--local' in sys.argv:
        parse_local_files()