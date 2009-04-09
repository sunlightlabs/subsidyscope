import urllib

import os, sys, datetime, re
from decimal import Decimal, ROUND_HALF_DOWN
from django.db import models
from etl.models import DataRun
from geo.models import State, County
from django.core.files.storage import FileSystemStorage


def Institution_get_upload_path(instance, filename):
    r = re.compile('[^\w]')
    cleaned_institution_name = r.gsub('-',instance.name)
    return "tarp-logos/%s/%s" % (cleaned_institution_name,filename)

Institution_FileSystemStorage = FileSystemStorage(location=('%s/tarp-logos' % os.path.abspath(os.path.dirname(sys.argv[0]))), base_url='/media/tarp-logos')


class InstitutionManager(models.Manager):
    
    MATCH_FAILED_GEOGRAPHY = 'failed_geography'
    MATCH_FAILED_NAME = 'failed_name'
    MATCH_SUCCESS_EXACT = 'success_exact'
    MATCH_SUCCESS_PARTIAL = 'success_partial'

    
    def matchInstitution(self, name, city=None, state=None):
        
        # finds best match(es) for institutions based on name and geography (if available)
        # returns more than one record if criteria provided match multiple institutions
        # also returns data regarding match quality
        
        institution_filter = self.all()
        
        if state:
            institution_filter = institution_filter.filter(state__iexact=state)
        
        if city: 
            institution_filter = institution_filter.filter(city__iexact=city)
        
        if institution_filter.count() == 0:
            return None, self.MATCH_FAILED_GEOGRAPHY
        
        name = name.lower()
        
        institution_filter_name = institution_filter.filter(name__iexact=name)
        
        if institution_filter_name.count() >= 1:
            return institution_filter_name, self.MATCH_SUCCESS_EXACT
        
        else:
            # try and standardize name (at the moment by removing common suffixes) and do a partial match
            # this is not very smart - yet - just implementing as a place holder for better partial matching algorithm
            
            trimed_name = name.replace(' incorporated', '').replace(' inc', '').replace(' corporation', '').replace(' corp', '')
            
            trimed_name = re.sub('[^a-z]+$', '', trimed_name)
            
            institution_filter_name = institution_filter.filter(name__istartswith=trimed_name)
            
            if institution_filter_name.count() >= 1:
                return institution_filter_name, self.MATCH_SUCCESS_PARTIAL
            else:
                return None, self.MATCH_FAILED_NAME
            
            
    
    def updateStockPrices(self):
        
        for institution in self.all():
            
            if institution.stock_symbol and institution.hasStrikePrice():
                
                institution.updateStockPrice()
                
    def updateTARPParticipation(self):
        
        # updates denormalized data point regarding TARP participation for all organizations
        # this should be run after any data load
        
        for institution in self.all():
            institution.updateTARPParticipation()
    

class Institution(models.Model):
    def __unicode__(self):
        if self.fdic_number:
            return "%s (FDIC: %i)" % (self.name, self.fdic_number)
        else:
            return self.name
    class Meta:
        verbose_name = 'TARP Institution'
        ordering = ['name'] 

    # account for admin interface being in thousands
    def total_assets_fixed(self):
        assets = self.getMostRecentTotalAssets()
        if assets == None:
            return None
        else:
            return assets * 1000

    name = models.CharField("Name", max_length=50)
    display_name = models.CharField("Display Name (if different)", max_length=100, blank=True, default='')
    
    fdic_number = models.IntegerField("FDIC ID", max_length=10, blank=True, null=True)
    fed_number = models.IntegerField("Fed RSS ID", max_length=10, blank=True, null=True)
    ots_number = models.CharField("OTS ID", max_length=10, blank=True, null=True, default='')
    
    TYPE_CHOICES = (
        ('bank','Bank'),
        ('holding company','Holding Company'),
        ('thrift holding company', 'Thrift Holding Company'), 
        ('savings and loan', 'Savings & Loan'),
        ('insurance company', 'Insurance Company'), 
        ('auto company', 'Auto Company'),
        ('other', 'Other')
    )
    
    type_of_institution = models.CharField("Institution Type", max_length=25, choices=TYPE_CHOICES, default='bank')
    
    parent_institution = models.ForeignKey('self', null=True)
 
    total_deposits = models.DecimalField("Total Deposits ($thousands)", max_digits=15, decimal_places=2, blank=True, null=True)
    total_assets = models.DecimalField("Total Assets ($thousands)", max_digits=15, decimal_places=2, blank=True, null=True)

    percentage_return_on_assets = models.DecimalField("Return On Assets (percentage)", max_digits=8, decimal_places=4, blank=True, null=True)
    
    REGULATOR_CHOICES = (
        ('Comptroller', 'Comptroller of the Currency'),
        ('FDIC', 'Federal Deposit Insurance Corporation'),
        ('Federal Reserve', 'Federal Reserve Board'),
        ('Thrift', 'Office of Thrift Supervision'),
        ('Other', 'Other')
    )
    regulator = models.CharField("Federal Regulator", max_length=15, choices=REGULATOR_CHOICES, blank=True, null=True)
    regulator_other = models.CharField("Federal Regulator (other)", max_length=50, blank=True, default='')


    institution_type = models.CharField("TARP Institution Type", max_length=50, blank=True)
    city = models.CharField("City", max_length=100, blank=True)
    
    #county = models.ForeignKey(County, null=True) 
    #state = models.ForeignKey(State) 
    state = models.CharField("State", max_length=2, blank=True)

    stock_symbol = models.CharField("Stock Symbol", max_length=10, blank=True)  
    logo = models.ImageField("Logo", upload_to=Institution_get_upload_path, storage=Institution_FileSystemStorage, blank=True)    

    crp_lobbying_total = models.DecimalField("Total Contributions and Lobbying", max_digits=15, decimal_places=2, blank=True, null=True)

    datarun = models.ForeignKey(DataRun)
    
    # denormalizing to allow quick filtering of fdic loaded institutions from tarp participants 
    # use updateTARPParticipation to set this value
    tarp_participant = models.BooleanField() 
    
    tlgp_participant = models.BooleanField()
    
    objects = InstitutionManager()
    
    
    def getTARPFundsReceived(self):
        
        total_funds = 0
        
        if self.transaction_set.count() > 0:
            
            for transaction in self.transaction_set.all():
                
                total_funds += transaction.price_paid
            
        return total_funds
    
    def getParentTARPFundsReceived(self):
        
        total_funds = 0
            
        if self.parent_institution:
            
            total_funds += self.parent_institution.getTotalTARPFundsReceived()
            
        return total_funds
    
    def getTotalTARPFundsReceived(self):
        
        return self.getTARPFundsReceived() + self.getParentTARPFundsReceived()
    
    
    def getMostRecentTotalAssets(self):
        
        try:
            return InstitutionAssetHistory.objects.filter(institution=self).order_by('-report_date')[0].total_assets
        except:
            return None
       
    def hasStrikePrice(self):
        
        for transaction in self.transaction_set.all():
            
            if transaction.warrant_reported_strike_price:
                return True
        
        return False
    
    def updateStockPrice(self):
        
        if self.tarp_participant:
 
            InstitutionDailyStockPrice.objects.importStockPrices(self)

            

        
    def updateTARPParticipation(self):
        
        if self.transaction_set.all().count() > 0:
            self.tarp_participant = True
            self.save()
        else:
            self.tarp_participant = False


class InstitutionAssetHistory(models.Model):    
    
    institution = models.ForeignKey(Institution)
    
    report_date = models.DateField()
    crawl_date = models.DateField()
    
    total_deposits = models.DecimalField("Total Deposits", max_digits=15, decimal_places=2, blank=True, null=True)
    total_assets = models.DecimalField("Total Assets", max_digits=15, decimal_places=2, blank=True, null=True)



class InstitutionBranch(models.Model):
    
    institution = models.ForeignKey(Institution)
    
    address = models.CharField("Address", max_length=100, blank=True)
    city = models.CharField("City", max_length=100, blank=True)
    zip = models.CharField("Zip", max_length=100, blank=True)
    
    county = models.ForeignKey(County)
    
    SERVICE_CHOICES = ((11, 'Full Service Brick and Mortar Office'),
                (12, ' Full Service Retail Office'),
                (13, 'Full Service Cyber Office'),
                (14, 'Full Service Mobile Office'),
                (15, 'Full Service Home/Phone Banking'),
                (16, 'Full Service Seasonal Office'),
                (21, 'Limited Service Administrative Office'),
                (22, 'Limited Service Military Facility '),
                (23, 'Limited Service Facility Office'),
                (24, 'Limited Service Loan Production Office'),
                (25, 'Limited Service Consumer Credit Office'),
                (26, 'Limited Service Contractual Office'),
                (27, 'Limited Service Messenger Office'),
                (28, 'Limited Service Retail Office'),
                (29, 'Limited Service Mobile Office'),
                (30, 'Limited Service Trust Office')
            )
    
    service = models.IntegerField('Service Type', choices=SERVICE_CHOICES, null=True)
    office_number = models.IntegerField('Office Number', null=True)
    unique_number = models.IntegerField('Unique Number', null=True)
    
    deposits = models.DecimalField('Deposits', max_digits=15, decimal_places=2, null=True)
    
    
    
class InstitutionDailyStockPriceManger(models.Manager):
    
    def getLastClosingPrice(self, institution):
        
        try:
            recentTransaction = self.filter(institution=institution).order_by('-date')[0]
            return recentTransaction.closing_price
        except:
            return None
        
    def getLastDate(self, institution):
        
        try:
            recentTransaction = self.filter(institution=institution).order_by('-date')[0]
            return recentTransaction.date
        except:
            return None
        
    def getLastUpdate(self):
        
        try:
            recentTransaction = self.filter().order_by('-date')[0]
            return recentTransaction.date
        except:
            return None
    
    def importStockPrices(self, institution):
        
        if institution.stock_symbol:
            
            # grab daily pricing info for institution.stock_symbol 
            url = 'http://ichart.yahoo.com/table.csv?s=%s&ignore=.csv' % institution.stock_symbol 
            
            last_date = self.getLastDate(institution)
            if last_date:
                
                # get only prices since last_date 
                
                next_date = last_date + datetime.timedelta(days=1)
                url += '&a=%s&' % str(next_date.month - 1) + \
                'b=%s&' % str(next_date.day) + \
                'c=%s' % str(next_date.year)
                
            else:
                
                # get all prices to 45 prior first transaction close date
                # historical prices are used for calculating trailing average for strike price
                
                last_transaction_date = Transaction.objects.getFirstTransactionDate(institution)
                if last_transaction_date:
                    next_date = last_transaction_date - datetime.timedelta(days=45)
                    url += '&a=%s&' % str(next_date.month - 1) + \
                    'b=%s&' % str(next_date.day) + \
                    'c=%s' % str(next_date.year)
            
            prices = urllib.urlopen(url).readlines()
                    
            if len(prices) == 0 or len(prices[0].split(',')) != 7:
                # no data
                return 
            
            for price in prices[1:]:
                
                price_parts = price.split(',')
                date_str = price_parts[0]
                date_obj = datetime.date(year=int(date_str[0:4]), month=int(date_str[5:7]), day=int(date_str[8:10]))
                closing_price = price_parts[4]
                self.create(institution=institution, date=date_obj, closing_price=Decimal(closing_price))


    
class InstitutionDailyStockPrice(models.Model):
    
    def __unicode__(self):
            millions = int(self.price_paid) / 1000000.0
            return '%s - %s - $%.1fm' % (self.date, self.institution.name, millions)
    class Meta:
        verbose_name = 'Institution Daily Stock Price'
        ordering = ['-date', 'institution']
        
    institution = models.ForeignKey(Institution)
    date = models.DateField("Date")

    closing_price = models.DecimalField("Price Paid", max_digits=6, decimal_places=2, blank=True, null=True)
    
    objects = InstitutionDailyStockPriceManger()
    
    
    
    
class TransactionManager(models.Manager):
    
    def calculateStrikePrices(self):
        
        transactions = self.all()
        
        for transaction in transactions:
            if transaction.institution.stock_symbol:
                print transaction.institution.stock_symbol
                transaction.calculateStrikePrice()
    
    def getLastTransactionDate(self, institution=None):
        
        try:
            if institution:
                recentTransaction = self.filter(institution=institution).order_by('-date')[0]
            else:
                recentTransaction = self.filter().order_by('-date')[0]
                    
            return recentTransaction.date
        
        except:
            return False
        
    def getFirstTransactionDate(self, institution):
        
        try:
            recentTransaction = self.filter(institution=institution).order_by('date')[0]
            return recentTransaction.date
        except:
            return False
    
    
class Transaction(models.Model):    
    
    def __unicode__(self):
        millions = int(self.price_paid) / 1000000.0
        return '%s - %s - $%.1fm' % (self.date, self.institution.name, millions)
    class Meta:
        verbose_name = 'TARP Transaction'
        ordering = ['-date', 'institution']    
        
    institution = models.ForeignKey(Institution)
    date = models.DateField("Date")
    price_paid = models.DecimalField("Price Paid", max_digits=15, decimal_places=2, blank=True, null=True)
    pricing_mechanism = models.CharField("Pricing Mechanism", max_length=50, blank=True, default='')
    description = models.CharField("Description", max_length=255, blank=True)
    transaction_type = models.CharField("Transaction Type", max_length=50)
    
    warrant_reported_strike_price = models.DecimalField("Warrant Strike Price", max_digits=6, decimal_places=2, blank=True, null=True)
    warrant_calculated_strike_price = models.DecimalField("Warrant Strike Price", max_digits=6, decimal_places=2, blank=True, null=True)
    warrants_issued = models.IntegerField("Warrant Issued", blank=True, null=True)
    
    PROGRAM_CHOICES = (
        ('CPP', 'Capital Purchase Program'),
        ('AGP', 'Asset Guarantee Program'),
        ('TIP', 'Targeted Investment Program'),
        ('AIFP', 'Automotive Industry Financing Program'),
        ('SSFI', 'Systematically Significant Failing Institutions'),
        ('TLGP', 'Temporary Liquidity Guarantee Program'),
        ('CBLIIP','Consumer and Business Lending Initiative Investment Program')
    )
    program = models.CharField("Program", max_length=50, choices=PROGRAM_CHOICES, blank=True, null=True, default='CPP')

    institution_call_option_price = models.DecimalField("Price of at-the-money call option with longest maturity on preceding date", max_digits=15, decimal_places=2, blank=True, null=True)
    institution_outstanding_shares = models.PositiveIntegerField("Outstanding shares as of last filing before transaction", blank=True, null=True)
    institution_dividend_per_share = models.DecimalField("Dividend per share as of last quarter before transaction", max_digits=15, decimal_places=2, blank=True, null=True)
    institution_preferred_yields = models.DecimalField("Preferred Yields", max_digits=15, decimal_places=2, blank=True, null=True)

    show_in_tracker = models.BooleanField()

    datarun = models.ForeignKey(DataRun)

    objects = TransactionManager()

    def calculateStrikePrice(self):
        
        #institution.updateStockPrice()
        
        # get last twenty days of pricing
        
        if self.program == 'CPP':
            
            prices = InstitutionDailyStockPrice.objects.filter(institution=self.institution, date__lt=self.date).order_by('-date')[0:20]
            
            
            if len(prices) == 20: 
            
                total = 0
                
                # calculate average on closing_price
                
                for price in prices:
                    total += price.closing_price
                
                average = total / len(prices)
            
                print average
            
                self.warrant_calculated_strike_price = average
                self.save()
        
    def getMoneyPercentage(self):
        
        stock = self.getLastClosingPrice()
        strike = self.warrant_reported_strike_price
            
        percent = (stock / strike).quantize(Decimal('0.01'), rounding=ROUND_HALF_DOWN) - 1
        
        return percent
         
        
    def getLastClosingPrice(self):
        
        return InstitutionDailyStockPrice.objects.getLastClosingPrice(self.institution)

    def getLastPriceUpdateDate(self):
        
        return InstitutionDailyStockPrice.objects.getLastDate(self.institution)
    

    def getMoneyPositionReportedStrikePrice(self):
        
        last_closing_price = InstitutionDailyStockPrice.objects.getLastClosingPrice(self.institution)
        
        if last_closing_price and self.warrant_reported_strike_price:
            return last_closing_price - self.warrant_reported_strike_price
        else:
            return None
        

    def isInMoneyReportedStrikePrice(self):
        
            if self.getMoneyPositionReportedStrikePrice() >= 0:
                return True
            else:
                return False

    def getMoneyPositionCalculatedStrikePrice(self):
        
        return InstitutionDailyStockPrice.objects.getLastClosingPrice(self.institution) - self.warrant_calculated_strike_price

    def isInMoneyCalculatedStrikePrice(self):
        
            if self.getMoneyPositionCalculatedStrikePrice() >= 0:
                return True
            else:
                return False
    
    def getSubsidyEstimate(self):
        if not hasattr(self,'SubsidyEstimate'):
            if SubsidyEstimate.objects.filter(transaction__id=self.id).count()>0:
                self.SubsidyEstimate = SubsidyEstimate.objects.filter(transaction__id=self.id)[0]
            else:
                # create a dummy object with the necessary attributes
                # irritating that we can't just use object() -- it has no __dict__, sadly
                class JunkClass(object):
                    pass
                self.SubsidyEstimate = JunkClass()
                self.SubsidyEstimate.__dict__.update({'date': None, 'source': None, 'subsidy_rate': None})

        return self.SubsidyEstimate
        
    def is_negative(self):
        """ returns true if the transaction amount is negative. convenience method for templating. """
        print self.price_paid, self.price_paid<0
        return self.price_paid<0
    
            
class SubsidyEstimate(models.Model):
    def __unicode__(self):
        return '%s - %d%% (%s)' % (self.transaction.institution.name, self.subsidy_rate, self.source)
    class Meta:
        verbose_name = 'Subsidy Estimate'
        ordering = ['-date']
    transaction = models.ForeignKey(Transaction)
    date = models.DateField("Estimate Date")
    source = models.CharField("Esimate Source", max_length=50)
    subsidy_rate = models.IntegerField("Subsidy Rate (Percentage)", max_length=3, blank=True, null=True)
