from django.db import models
import csv

class NAICSManager(models.Manager):

    def load_naics(self, infile=None):
        if not infile:
            f = csv.reader(open("data/naics/naics_codes.csv"))
        else:
            f = csv.reader(open(infile))

        f.next() #header line
        for l in f:
            code = l[1]
            desc = l[2]

            try:
                code = int(code)
            except:
                continue #not a valid code
            
            try:
                n = NAICS.objects.get(code=code, description=desc)

            except:
                n = NAICS(code=code, description=desc)
                n.save()

class NAICS(models.Model):
    code = models.IntegerField("NAICS Code", blank=False, null=False, primary_key=True)
    description = models.CharField("Code Description", max_length=255)
   
    objects = NAICSManager()
     
    def __unicode__(self):
        return "%s - %s" % (self.code, self.description)

class PSCManager(models.Manager):

    def load_psc(self, infile=None):
        if not infile:
            f = csv.reader(open("data/psc/psc_codes.csv"))
        else:
            f = csv.reader(open(infile))

        f.next() #header line
        for l in f:
            code = l[0]
            desc = l[1]
            try:
                code = int(code)
            except:
                continue #not a valid code
            try:
                p = PSC.objects.get(code=code, description=desc)

            except:
                p = PSC(code=code, description=desc)
                p.save()
       

class PSC(models.Model):
    code = models.IntegerField("Product and Service Code", blank=False, null=False, primary_key=True)
    description = models.CharField("Code Description", max_length=255)

    objects = PSCManager()

    def __unicode__(self):
        return "%s - %s" % (self.code, self.description)


