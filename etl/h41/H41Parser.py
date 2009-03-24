import re
import BeautifulSoup

class H41Parser(object):
    """docstring for H41Parser"""
    def __init__(self):
        super(H41Parser, self).__init__()
        self.collectors = [
            {'label': 'Reserve Bank credit', 're': re.compile(r'^Reserve bank credit\s{3,}',re.I), 'restrict_to_first_table': True},

            {'label': 'U.S. Treasury securities', 're': re.compile(r'^\s*U\.S\. Treasury', re.I), 'restrict_to_first_table': True},
            {'label': 'Repurchase agreements', 're': re.compile(r'^\s*Repurchase agreements', re.I), 'restrict_to_first_table': True},
            {'label': 'Primary credit', 're': re.compile(r'^\s*Primary credit', re.I), 'restrict_to_first_table': True},
            {'label': 'Secondary credit', 're': re.compile(r'^\s*Secondary credit', re.I), 'restrict_to_first_table': True},
            {'label': 'Seasonal credit', 're': re.compile(r'^\s*Seasonal credit', re.I), 'restrict_to_first_table': True},
            {'label': 'Other credit extensions', 're': re.compile(r'^\s*Other credit extensions', re.I), 'restrict_to_first_table': True},
            {'label': 'Other federal reserve assets', 're': re.compile(r'^\s*Other federal reserve assets', re.I), 'restrict_to_first_table': True},

            {'label': 'Mortgage-backed securities', 're': re.compile(r'^\s*Mortgage-backed securities', re.I), 'restrict_to_first_table': True}, # BAILOUT
            {'label': 'Term Auction credit', 're': re.compile(r'^\s*Term auction credit', re.I), 'restrict_to_first_table': True}, # BAILOUT
            {'label': 'Primary dealer and other broker-dealer credit', 're': re.compile(r'^\s*Primary dealer and other broker-dealer credit', re.I), 'restrict_to_first_table': True}, # BAILOUT
            {'label': 'Asset-backed Commercial Paper Money Market Mutual Fund Liquidity Facility', 're': re.compile(r'^\s*Mutual fund Liquidity Facility', re.I), 'restrict_to_first_table': True}, # BAILOUT
            {'label': 'Credit extended to American International Group, Inc.', 're': re.compile(r'^\s*Group\,\s*Inc\.', re.I), 'restrict_to_first_table': True}, # BAILOUT
            {'label': 'Net portfolio holdings of Commercial Paper Funding Facility LLC', 're': re.compile(r'^\s*Funding Facility LLC', re.I), 'restrict_to_first_table': True}, # BAILOUT
            {'label': 'Net portfolio holdings of LLCs funded through the Money market Investor Funding Facility', 're': re.compile(r'Money Market Investor Funding Facility', re.I), 'restrict_to_first_table': True}, # BAILOUT
            {'label': 'Net portfolio holdings of Maiden Lane LLC', 're': re.compile(r'^\s*Net portfolio holdings of Maiden Lane LLC', re.I), 'restrict_to_first_table': True}, # BAILOUT
            {'label': 'Net portfolio holdings of Maiden Lane II LLC', 're': re.compile(r'^\s*Net portfolio holdings of Maiden Lane II LLC', re.I), 'restrict_to_first_table': True}, # BAILOUT
            {'label': 'Net portfolio holdings of Maiden Lane III LLC', 're': re.compile(r'^\s*Net portfolio holdings of Maiden Lane III LLC', re.I), 'restrict_to_first_table': True}, # BAILOUT
            {'label': 'Federal agency debt securities', 're': re.compile(r'^\s*Federal agency( debt securities )?\(2\)', re.I), 'restrict_to_first_table': True}, # BAILOUT
            {'label': 'Central bank liquidity swaps', 're': re.compile(r'^\s*Central bank liquidity swaps\s+(\(\d+\))?\s+\d+', re.I), 'restrict_to_first_table': True}, # BAILOUT
            {'label': 'Securities lent to dealers', 're': re.compile(r'^\s*Securities lent to dealers', re.I), 'restrict_to_first_table': False}   # BAILOUT     
        ]
      
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
            'Securities lent to dealers'
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
            collected_values[f['label']] = None
        
        if str(pre):        
            for collector in self.collectors:                
                for line in str(pre).split("\n"):
                    if collector['restrict_to_first_table'] and self.outside_first_table(line):
                        break
                    else:
                        if collector['re'].search(line):
                            # if collector=='Net portfolio holdings of Maiden Lane LLC':
                            #                                 print '### %s' % line
                            amount = self.get_dollar_figure(line)
                            if amount!=None:
                                collected_values[collector['label']] = amount
                            break

        return collected_values