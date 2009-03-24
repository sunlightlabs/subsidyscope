from django.db import models
from etl.models import DataRun
from bailout.models import Institution

class StandardAndPoorQuote(models.Model):
    def __unicode__(self):
        return '%s - $%.2f' % (self.date, self.close_price_adjusted)
    class Meta:
        verbose_name = 'S&P 500 Quote'
        ordering = ['-date'] 
    date = models.DateField("Date", unique=True)
    open_price = models.DecimalField("Open Price", max_digits=10, decimal_places=2, blank=True, null=True)
    low_price = models.DecimalField("Low Price", max_digits=10, decimal_places=2, blank=True, null=True)
    high_price = models.DecimalField("High Price", max_digits=10, decimal_places=2, blank=True, null=True)
    close_price = models.DecimalField("Close Price", max_digits=10, decimal_places=2, blank=True, null=True)
    close_price_adjusted = models.DecimalField("Adjusted Close Price", max_digits=10, decimal_places=2, blank=True, null=True)
    volume = models.IntegerField("Trading Volume", blank=True, null=True)
    datarun = models.ForeignKey(DataRun, related_name='zingales_data_StandardAndPoorQuote')
    
class TreasuryThreeYearBondQuote(models.Model):
    def __unicode__(self):
        if self.price==None:
            formatted_price = '.'
        else:
            formatted_price = '$%.2f' % self.price
        return '%s - %s' % (self.date, formatted_price)
    class Meta:
        verbose_name = "Treasury 3-year Constant Maturity Bond Quote"
        ordering = ['-date'] 
    date = models.DateField("Date", unique=True)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2, blank=True, null=True)
    datarun = models.ForeignKey(DataRun, related_name='zingales_data_TreasuryThreeYearBondQuote')    
 
class TreasuryTenYearBondQuote(models.Model):
    def __unicode__(self):
        if self.price==None:
            formatted_price = '.'
        else:
            formatted_price = '$%.2f' % self.price
        return '%s - %s' % (self.date, formatted_price)    
        ordering = ['-date'] 
    class Meta:
        verbose_name = "Treasury 10-year Constant Maturity Bond Quote"
    date = models.DateField("Date", unique=True)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2, blank=True, null=True)
    datarun = models.ForeignKey(DataRun, related_name='zingales_data_TreasuryTenYearBondQuote')    

class InstitutionStockQuote(models.Model):
    def __unicode__(self):
            return '%s - %s - $%.2f' % (self.institution.stock_symbol, self.date, self.price)
    class Meta:
        verbose_name = "Stock Quote"
        ordering = ['-date','institution'] 
    institution = models.ForeignKey(Institution, related_name='zingales_data_InstitutionStockQuote')
    date = models.DateField("Date")
    price = models.DecimalField("Price", max_digits=10, decimal_places=2, blank=True, null=True)
    datarun = models.ForeignKey(DataRun, related_name='zingales_data_InstitutionStockQuote')