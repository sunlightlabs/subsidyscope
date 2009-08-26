from bailout.models import Transaction, InstitutionDailyStockPrice
from fdic_bank_failures.models import BankFailure, QBPSnapshot
from fed_h41.models import H41Snapshot
from csv_generator import CSVFile, manager  

last_date = InstitutionDailyStockPrice.objects.getLastUpdate()



class TransactionCSV(CSVFile):
    
    # meta
    app_name = 'bailout'
    filename = 'tarp_transactions'
    description = 'TARP Transactions data.'
    
    # order rows by - passed into a .order_by() call on model
    
    order_by = '-date'
    
    # fields defined as a list of tuples
    # each field is defined as 
    # (column header, model attribute/function, documentation string, [optional lamda transform])
    
    fields = [
            ('Date', 'date',
             'TARP Transaction Date'),
            ('Name', 'institution.name',
             'Recipient Institution Name'),
            ('Price Paid', 'price_paid',
             ''),
            ('Pricing Mechanism', 'pricing_mechanism',
             ''),
            ('Description', 'description',
             ''),
            ('Transaction Type', 'transaction_type',
             ''),
            ('FDIC Number', 'institution.fdic_number',
             ''),
            ('OTS Number', 'institution.ots_number',
             ''),            
            ('Type of Institution', 'institution.type_of_institution',
             ''),
            ('Total Assets (Q4 2008)', 'institution.total_assets_fixed',
             ''),
            ('Regulator', 'institution.regulator',
             ''),
            ('City', 'institution.city',
             ''),
            ('State', 'institution.state',
             ''),
            ('Stock Symbol', 'institution.stock_symbol',
             ''),
            ('Program', 'program',
             ''),
            ('Warrant Strike Price', 'warrant_reported_strike_price',
             ''),
            ('Warrant Received', 'warrants_issued',
             ''),
            ('Warrant Disposed', 'warrants_disposed',
             ''),
            ('Stock Price (as of close %s)' % last_date, 'getLastClosingPrice',
             ''),
            ('In/Out of Money (as of close %s)' % last_date, 'getMoneyPositionReportedStrikePrice',
             ''),
            ('Subsidy Rate Estimate (percentage)', 'getSubsidyEstimate.subsidy_rate',
             ''),
            ('Subsidy Rate Estimate Date', 'getSubsidyEstimate.date',
             ''),
            ('Subsidy Rate Estimate Source', 'getSubsidyEstimate.source',
             '')
            ]
    
    
class FDICBankFailureCSV(CSVFile):
    
    app_name = 'bailout'
    
    filename = 'fdic_bank_failures'
    
    description = 'FDIC Bank Failures'
    
    order_by = 'closing_date'
 
    fields = [
        ('Failed Institution', 'name', 
        ''),
        ('City', 'city',
         ''),
        ('State', 'state',
         ''),
        ('Date of Bank Closure', 'closing_date',
         ''),
        ('Estimated Loss to the Deposit Insurance Fund (exact)', 'exact_amount',
         '', lambda x: x * 1000000),
        ('Estimated Loss to the Deposit Insurance Fund (lower range)', 'range_low',
         '', lambda x: x * 1000000),
        ('Estimated Loss to the Deposit Insurance Fund (upper range)', 'range_high',
         '', lambda x: x * 1000000),
        ('Notes', 'notes',
         ''),
        ('Report', 'ig_report',
         '')
        ]


class FDICQBPSnapshotCSV(CSVFile):
    
    app_name = 'bailout'
    
    filename = 'fdic_qbp_snapshot'
    
    description = 'FDIC QBP Snapshot'
    
    order_by = 'date'

    fields = [
        ('Date', 'date',
         ''),
        ('Number of Problem Institutions', 'problem_institutions', 
        ''),
        ('Reserve Ratio (percent)', 'reserve_ratio',
         ''),
        ('Fund Balance', 'fund_balance',
         '', lambda x: x * 1000000),
        ]


class FedH41SnapshotCSV(CSVFile):
    
    app_name = 'bailout'
    
    filename = 'federal_reserve_h41'
    
    description = 'Federal Reserve H41 Snapshot'
    
    order_by = 'date'
    
    fields = [('Date', 'date',
               ''),
               ('Reserve Bank credit', 'reserve_bank_credit',
               '', lambda x: x * 1000000),
               ('Repurchase agreements', 'repurchase_agreements',
               '', lambda x: x * 1000000),
               ('Primary credit', 'primary_credit',
               '', lambda x: x * 1000000),
               ('Secondary credit', 'secondary_credit',
               '', lambda x: x * 1000000),
               ('Seasonal credit', 'seasonal_credit',
               '', lambda x: x * 1000000),
               ('Other credit extensions', 'other_credit_extensions',
               '', lambda x: x * 1000000),
               ('Mortgage-backed securities', 'mortgage_backed_securities',
               '', lambda x: x * 1000000),
               ('Term Auction credit', 'term_auction_credit',
               '', lambda x: x * 1000000),
               ('Primary dealer and other broker-dealer credit', 'primary_dealer_and_other_broker_dealer_credit',
               '', lambda x: x * 1000000),
               ('Asset-backed Commercial Paper Money Market Mutual Fund Liquidity Facility', 'asset_backed_commercial_paper_money_market',
               '', lambda x: x * 1000000),
               ('Credit extended to American International Group, Inc.', 'credit_extended_to_aig',
               '', lambda x: x * 1000000),
               ('Net portfolio holdings of Commercial Paper Funding Facility LLC', 'commercial_paper_funding_facility',
               '', lambda x: x * 1000000),
               ('Net portfolio holdings of Maiden Lane LLC', 'maiden_lane_i',
               '', lambda x: x * 1000000),
               ('Net portfolio holdings of Maiden Lane II LLC', 'maiden_lane_ii',
               '', lambda x: x * 1000000),
               ('Net portfolio holdings of Maiden Lane III LLC', 'maiden_lane_iii',
               '', lambda x: x * 1000000),
               ('Federal agency debt securities', 'federal_agency_debt_securities',
               '', lambda x: x * 1000000),
               ('Term Facility', 'term_facility',
               '', lambda x: x * 1000000),
               ('Term Asset-Backed Securities Loan Facility', 'talf',
               '', lambda x: x * 1000000),
               ('Term Asset-Backed Securities Loan Facility', 'talf',
               '', lambda x: x * 1000000),
               ('Other federal reserve assets', 'other_federal_reserve_assets',
               '', lambda x: x * 1000000),
               ('Central bank liquidity swaps', 'central_bank_liquidity_swaps',
               '', lambda x: x * 1000000),
               ('U.S. Treasury securities', 'us_treasury_securities',
               '', lambda x: x * 1000000)
              ]

manager.register(Transaction, TransactionCSV)
manager.register(BankFailure, FDICBankFailureCSV)
manager.register(QBPSnapshot, FDICQBPSnapshotCSV)
manager.register(H41Snapshot, FedH41SnapshotCSV)
