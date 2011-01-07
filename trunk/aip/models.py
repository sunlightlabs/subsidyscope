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
    service_level = models.CharField("Airport Service Level", max_length=4)  
    district = models.IntegerField("Congressional District of Airport")

class Record(models.Model):
    class Meta:
        abstract = True

    fiscal_year = models.IntegerField("Fiscal Year", null=False)
    description = models.CharField("Description of grant purpose", max_length=5000)

class GrantRecord(Record):
    def __unicode__(self):
        return "%s - %s - %s" % (self.airport, self.fiscal_year, self.total)
    
    grant_number = models.CharField("Unique grant id", primary_key=True, max_length=25)
    airport = models.ForeignKey(Airport, null=False)
    total = models.DecimalField("Total funding for this grant", null=False, blank=False, decimal_places=2, max_digits=15)
    entitlement_total = models.DecimalField("Total funding from entitlements", default=0, decimal_places=2, max_digits=15)
    discretionary_total = models.DecimalField("Total funding from discretionary funds", default=0, decimal_places=2, max_digits=15)
    stimulus_total = models.DecimalField("Total stimulus funding for this grant", default=0, decimal_places=2, max_digits=15)


class BlockGrant(Record):
    def __unicode__(self):
        return "%s - %s" % (self.fiscal_year, self.stateName)
    class Meta:
        ordering=['fiscal_year', 'stateName']
    state = models.CharField("State receiving grant", max_length=2, null=False)
    stateName = models.CharField("State name", max_length=20, null=False)

class Project(models.Model):
    def __unicode__(self):
        return "%s - %s - %s" % (self.grant, self.airport, self.total)
    fiscal_year = models.IntegerField("Fiscal Year", null=False, blank=False)
    grant = models.ForeignKey(GrantRecord, null=False, blank=False)
    airport = models.ForeignKey(Airport, null=False, blank=False)
    npr = models.IntegerField("National Priority Rating for this project", null=False, blank=False)
    description = models.CharField("Description of this project", max_length=900)
    total = models.DecimalField("Project total funding", null=False, blank=False, decimal_places=2,max_digits=15)
    stimulus = models.DecimalField("Stimulus money for this project", default=0, decimal_places=2, max_digits=15) 
    discretionary = models.DecimalField("Discretionary funding for this project", default=0, decimal_places=2, max_digits=15)
    entitlement = models.DecimalField("Entitlement funding for this project", default=0, decimal_places=2, max_digits=15)

class StateGrant(models.Model):
    def __unicode__(self):
        return "%s - %s - %s" % (self.fiscal_year, self.airport, self.state)
    class Meta:
        ordering=['fiscal_year', 'state']
    state = models.CharField("State", max_length=2, null=False, blank=False)
    city = models.CharField("City", max_length=30)
    airport = models.ForeignKey(Airport, null=False)
    fiscal_year = models.IntegerField("Fiscal Year")
    amount = models.DecimalField("Amount of Grant", decimal_places=2, max_digits=30)
    description = models.CharField("Description of Project", max_length=5000)

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



