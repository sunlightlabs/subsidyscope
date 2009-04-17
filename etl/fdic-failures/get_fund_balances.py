import re
import BeautifulSoup
import sys
import csv
from decimal import Decimal


class FDICFundBalanceParser(object):
    """FDIC-parsing class"""
    def __init__(self):
        super(FDICFundBalanceParser, self).__init__()
        self.re_number_table_cell = re.compile(r'>\s*([\-\$]{0,2}[\d\.\,]+)\s*<')
        self.re_ending_fund_balance = re.compile(r'Ending Fund Balance', re.I)
        self.re_money = re.compile(r'>(\-?[\d\,]+)<')
        self.re_fund_balance = re.compile(r'Fund Balance', re.I)
        self.re_savings_association_insurance_fund = re.compile(r'Savings Association Insurance Fund', re.I)
        self.re_reserve_ratio = re.compile(r'>\s*Reserve ratio', re.I)
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
        self.out_order = [
            'date',
            'fund balance',            
            'reserve ratio'
        ]
        
    def find_first_number_in_row(self, beautifulsoup_row):
        """Finds the number in the first column of a BeautifulSoup table row"""
        for td in beautifulsoup_row.findAll('td'):
            match = self.re_number_table_cell.search(str(td))
            if match:
                return match.group(1).replace(',','').replace('$','')
        
        return None
        
    def get_fund_balance_from_table(self, year, table_html):
        """docstring for parse_table"""
        fund_balance = None
        
        if year>=2006:
            b = BeautifulSoup.BeautifulSoup(table_html)
            for tr in b.findAll('tr'):
                for td in tr.findAll('td'):
                    if self.re_ending_fund_balance.search(str(td)):
                        fund_balance = self.find_first_number_in_row(tr)
                        break
                    # look for the reserve ratio
                    elif self.re_reserve_ratio.search(str(td)):
                        reserve_ratio = self.find_first_number_in_row(tr)                        
                        break
                
        else:
            bank_fund_balance = 0
            bank_reserve_ratio = 0
            savings_association_fund_balance = 0
            savings_association_reserve_ratio = 0
            found_savings_association_line_item = False
            b = BeautifulSoup.BeautifulSoup(table_html)
            for tr in b.findAll('tr'):

                # keep track of whether we're in the "savings association insurance fund" section of the table (exists pre-2007)
                if self.re_savings_association_insurance_fund.search(str(tr)):
                    found_savings_association_line_item = True           

                for td in tr.findAll('td'):
                    # look for the fund balance
                    if self.re_fund_balance.search(str(td)):
                        if not found_savings_association_line_item:
                            bank_fund_balance = self.find_first_number_in_row(tr)
                        else:
                            savings_association_fund_balance = self.find_first_number_in_row(tr)
                        break

                    # look for the reserve ratio
                    elif self.re_reserve_ratio.search(str(td)):
                        if not found_savings_association_line_item:
                            bank_reserve_ratio = self.find_first_number_in_row(tr)
                        else:
                            savings_association_reserve_ratio = self.find_first_number_in_row(tr)
                        break
                        
            fund_balance = int(bank_fund_balance) + int(savings_association_fund_balance)
            
            bank_component = Decimal(bank_reserve_ratio) * Decimal(bank_fund_balance) / Decimal('100.0')
            savings_association_component = Decimal(savings_association_reserve_ratio) * Decimal(savings_association_fund_balance) / Decimal('100.0')
            reserve_ratio = (bank_component + savings_association_component) / Decimal(fund_balance) * Decimal('100.0')

        return {'fund balance': fund_balance, 'reserve ratio': reserve_ratio}
        

def parse_local_files():
    MONTHS = [3, 6, 9, 12]
    parser = FDICFundBalanceParser()
    writer = csv.writer(sys.stdout)
    writer.writerow(parser.out_order)
    for y in range(2003, 2009):
        for m in MONTHS:
            f = open('./dep1b/%d%s.html' % (y, parser.month_map[m]), 'r')
            table_info = parser.get_fund_balance_from_table(year=y, table_html=''.join(f.readlines()))
            table_info['date'] = '%d-%d-1' % (y, m)
            row = []
            for field in parser.out_order:
                row.append(table_info[field])
            writer.writerow(row)
                    
            f.close()

if __name__ == '__main__':
    if '--local' in sys.argv:
        parse_local_files()