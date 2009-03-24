from django.db import models

class SubsidyRecord(models.Model):    
    def __unicode__(self):            
        return self.name
    class Meta:
        verbose_name = 'TARP Subsidy Record'
    name = models.CharField("Name", max_length=80)
    color = models.CharField("Color", max_length=6)
    amount_received = models.DecimalField("Amount Received", max_digits=10, decimal_places=2)
    estimated_subsidy = models.DecimalField("Estimated Subsidy", max_digits=10, decimal_places=2)
    subsidy_rate = models.DecimalField("Subsidy Rate", max_digits=10, decimal_places=2)