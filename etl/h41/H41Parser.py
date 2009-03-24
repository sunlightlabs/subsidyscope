import re
import BeautifulSoup

class H41Parser(object):
    """docstring for H41Parser"""
    def __init__(self):
        super(H41Parser, self).__init__()
        self.collectors = {
            'Reserve Bank credit': re.compile(r'^Reserve bank credit\s{3,}', re.I),
            'Mortgage-backed securities': re.compile(r'^\s*Mortgage-backed securities', re.I), # BAILOUT
            'Term Auction credit': re.compile(r'^\s*Term auction credit', re.I), # BAILOUT
            'Primary dealer and other broker-dealer credit': re.compile(r'^\s*Primary dealer and other broker-dealer credit', re.I), # BAILOUT
            'Asset-backed Commercial Paper Money Market Mutual Fund Liquidity Facility': re.compile(r'^\s*Mutual fund Liquidity Facility', re.I), # BAILOUT
            'Credit extended to American International Group, Inc.': re.compile(r'^\s*Group\,\s*Inc\.', re.I), # BAILOUT
            'Net portfolio holdings of Commercial Paper Funding Facility LLC': re.compile(r'^\s*Funding Facility LLC', re.I), # BAILOUT
            'Net portfolio holdings of LLCs funded through the Money market Investor Funding Facility': re.compile(r'Money Market Investor Funding Facility', re.I), # BAILOUT
            'Net portfolio holdings of Maiden Lane LLC': re.compile(r'Maiden Lane LLC', re.I), # BAILOUT
            'Net portfolio holdings of Maiden Lane II LLC': re.compile(r'Maiden Lane II LLC', re.I), # BAILOUT
            'Net portfolio holdings of Maiden Lane III LLC': re.compile(r'Maiden Lane III LLC', re.I), # BAILOUT
            'Federal agency debt securities': re.compile(r'^\s*Federal agency( debt securities )?\(2\)', re.I), # BAILOUT
            'Central bank liquidity swaps': re.compile(r'^\s*Central bank liquidity swaps', re.I), # BAILOUT
            'U.S. Treasury securities': re.compile(r'^\s*U\.S\. Treasury', re.I),
            'Repurchase agreements': re.compile(r'^\s*Repurchase agreements', re.I),
            'Primary credit': re.compile(r'^\s*Primary credit', re.I),
            'Secondary credit': re.compile(r'^\s*Secondary credit', re.I),
            'Seasonal credit': re.compile(r'^\s*Seasonal credit', re.I),
            'Other credit extensions': re.compile(r'^\s*Other credit extensions', re.I),
            'Other federal reserve assets': re.compile(r'^\s*Other federal reserve assets', re.I)
        }
        self._non_bailout_line_items = [
            'U.S. Treasury securities',
            'Federal agency debt securities',
            'Repurchase agreements',
            'Primary credit',
            'Secondary credit',
            'Seasonal credit',
            'Other credit extensions',
            'Other federal reserve assets',
        ]
        self.out_order = [
            'Reserve Bank credit',

            'U.S. Treasury securities',
            'Repurchase agreements',
            'Primary credit',
            'Secondary credit',
            'Seasonal credit',
            'Other credit extensions',
            'Other federal reserve assets',
            
            'Mortgage-backed securities',
            'Term Auction credit',
            'Primary dealer and other broker-dealer credit',
            'Asset-backed Commercial Paper Money Market Mutual Fund Liquidity Facility',
            'Credit extended to American International Group, Inc.',
            'Net portfolio holdings of Commercial Paper Funding Facility LLC',
            'Net portfolio holdings of LLCs funded through the Money market Investor Funding Facility',
            'Net portfolio holdings of Maiden Lane LLC',
            'Net portfolio holdings of Maiden Lane II LLC',
            'Net portfolio holdings of Maiden Lane III LLC',
            'Federal agency debt securities',
            'Central bank liquidity swaps',
        ]
        self._re_table_start = re.compile('^(\d)\.')
        self._re_figure = re.compile('\s(\-?[\d\,]+)\s')        

    def get_dollar_figure(self, line):
        m = self._re_figure.search(line)
        if not m:
            return None
        else:
            amount = m.group(1).replace(',','')
            return int(amount)

    def outside_first_table(self, line):
        """Checks to see whether the parser has left Table 1"""
        m = self._re_table_start.match(line)
        if m:
            if int(m.group(1))>1:
                return True
        return False

    def process_e41(self, html):
        """process HTML document containing E.4.1 report"""
        b = BeautifulSoup.BeautifulSoup(html)
        pre = b.find('pre')
        if not pre:
            return False

        collected_values = {}
        for f in self.collectors:
            collected_values[f] = None
        
        if str(pre):        
            for collector in self.collectors:                
                for line in str(pre).split("\n"):
                    if self.outside_first_table(line):
                        break
                    else:
                        if self.collectors[collector].search(line):  
                            amount = self.get_dollar_figure(line)
                            if amount!=None:
                                collected_values[collector] = amount
                            break

        return collected_values