from django.db import models


class Airport(models.Model):
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name
    
    code = models.CharField("Airport code", max_length=6, primary_key=True )
    npias = models.CharField("NPIAS code", max_length=9, blank=False)
    name = models.CharField("Airport name", max_length=50, blank=False)
    city = models.CharField("City of Airport", max_length=50)
    state = models.CharField("State of Airport", max_length=2)
    ADO = models.CharField("ADO code of airport", max_length=6)


class GrantRecord(models.Model):
    def __unicode__(self):
        return "%s - %s - %s" % (self.airport, self.fiscal_year, self.amount)

    airport = models.ForeignKey(Airport, null=False)
    fiscal_year = models.IntegerField("Fiscal Year", null=False)
    amount = models.DecimalField("Grant Amount", null=False, decimal_places=2, max_digits=30)
    seq_number = models.IntegerField("Grant Sequence Number")
    description = models.CharField("Description of grant purpose", max_length=5000)
    service_level = models.CharField("Service level of airport (passenger or private)", max_length=5)
    region = models.CharField("Region code for airport", max_length=5)

class Enplanements(models.Model):
    class Meta:
        ordering=['airport', 'year']
    def __unicode__(self):
        return "%s - %s - %s" % (self.airport, self.year, self.amount)

    airport = models.ForeignKey(Airport, null=False)
    year = models.IntegerField("Calendar year of enplanement total", null=False)
    amount = models.IntegerField("Total enplanements for this year", null=False)

class Operations(models.Model):
    class Meta:
        ordering = ['airport', 'year']
    def __unicode__(self):
        return "%s - %s - %s" % (self.airport, self.year, self.operations)

    airport = models.ForeignKey(Airport, null=False)
    year = models.IntegerField("Calendar year of operation total", null=False)
    operations = models.IntegerField("Total operations for this year", null=False)




