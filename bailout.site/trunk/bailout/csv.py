from bailout.models import Transaction, InstitutionDailyStockPrice
from csv_generator import CSVFile, manager  

last_date = InstitutionDailyStockPrice.objects.getLastUpdate()

class TransactionCSV(CSVFile):
    
    # meta
    
    filename = 'tarp_transactions'
    
    description = 'TARP Transactions data.'
    
    # order rows by - passed into a .order_by() call on model
    
    order_by = '-date'
    
    # fields defined as a list of tuples
    # each field is defined as 
    # (column header, model attribute/function, documentation string)
    
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
    
    
manager.register(Transaction, TransactionCSV)