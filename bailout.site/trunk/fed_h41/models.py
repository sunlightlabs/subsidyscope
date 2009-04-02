from django.db import models

# Create your models here.
class H41Snapshot(models.Model):

    def __unicode__(self):
        return str(self.date)
    class Meta:
        verbose_name = 'H41 Snapshot'
        ordering = ['-date']

    date = models.DateField("Date")
    
    # this field should sum to the others
    reserve_bank_credit = models.IntegerField("Reserve Bank credit", max_length=15, blank=True, null=True)
    
    repurchase_agreements = models.IntegerField("Repurchase agreements", max_length=15, blank=True, null=True)
    primary_credit = models.IntegerField("Primary credit", max_length=15, blank=True, null=True)
    secondary_credit = models.IntegerField("Secondary credit", max_length=15, blank=True, null=True)
    seasonal_credit = models.IntegerField("Seasonal credit", max_length=15, blank=True, null=True)
    other_credit_extensions = models.IntegerField("Other credit extensions", max_length=15, blank=True, null=True)
    mortgage_backed_securities = models.IntegerField("Mortgage-backed securities", max_length=15, blank=True, null=True)
    term_auction_credit = models.IntegerField("Term Auction credit", max_length=15, blank=True, null=True)
    primary_dealer_and_other_broker_dealer_credit = models.IntegerField("Primary dealer and other broker-dealer credit", max_length=15, blank=True, null=True)
    asset_backed_commercial_paper_money_market = models.IntegerField("Asset-backed Commercial Paper Money Market Mutual Fund Liquidity Facility", max_length=15, blank=True, null=True)
    credit_extended_to_aig = models.IntegerField("Credit extended to American International Group, Inc.", max_length=15, blank=True, null=True)
    commercial_paper_funding_facility = models.IntegerField("Net portfolio holdings of Commercial Paper Funding Facility LLC", max_length=15, blank=True, null=True)
    money_market_investor_funding_facility = models.IntegerField("Net portfolio holdings of LLCs funded through the Money market Investor Funding Facility", max_length=15, blank=True, null=True)
    maiden_lane_i = models.IntegerField("Net portfolio holdings of Maiden Lane LLC", max_length=15, blank=True, null=True)
    maiden_lane_ii = models.IntegerField("Net portfolio holdings of Maiden Lane II LLC", max_length=15, blank=True, null=True)
    maiden_lane_iii = models.IntegerField("Net portfolio holdings of Maiden Lane III LLC", max_length=15, blank=True, null=True)
    federal_agency_debt_securities = models.IntegerField("Federal agency debt securities", max_length=15, blank=True, null=True)
    term_facility = models.IntegerField("Term Facility", max_length=15, blank=True, null=True)
    talf = models.IntegerField("Term Asset-Backed Securities Loan Facility", max_length=15, blank=True, null=True)

    other_federal_reserve_assets = models.IntegerField("Other federal reserve assets", max_length=15, blank=True, null=True)
    central_bank_liquidity_swaps = models.IntegerField("Central bank liquidity swaps", max_length=15, blank=True, null=True)
    us_treasury_securities = models.IntegerField("U.S. Treasury securities", max_length=15, blank=True, null=True)
    
class FedNewsEvent(models.Model):
    
    def __unicode__(self):
        return '%s' % (self.date)
    class Meta:
        verbose_name = 'Fed News Event'
        ordering = ['-date']
    
    date = models.DateField("Date")
    text = models.TextField("Text", blank=False, default='', null=False)