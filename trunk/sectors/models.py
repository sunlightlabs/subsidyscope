from django.db import models
from django.conf import settings
from agency.models import Agency

from helpers.helpers import ManyToManyField_NoSyncdb

class Sector(models.Model):

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = 'Sector'

    name = models.CharField("Name", max_length=40)
    related_agencies = models.ManyToManyField(Agency, blank=True, null=True)
    launched = models.BooleanField("Launched?", default=False)
    
    budget_functions = ManyToManyField_NoSyncdb('budget_accounts.BudgetFunction', related_name='budget_functions', db_table='budget_accounts_budgetfunction_sectors')
    functional_indexes = ManyToManyField_NoSyncdb('cfda.ProgramFunctionalIndex', related_name='functional_indexes', db_table='cfda_programfunctionalindex_sectors')
    
    def image_url_small(self):        
        return settings.MEDIA_URL + 'images/sector_icons/' + str(self.id) + '_sm.png'

    def image_url_large(self):        
        return settings.MEDIA_URL + 'images/sector_icons/' + str(self.id) + '_lg.png'

    def binary_hash(self):
        return pow(2,(self.id-1))

class Subsector(models.Model):

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = 'Subsector'
        ordering = ['weight']
        
    name = models.CharField("Name", max_length=40)
    parent_sector = models.ForeignKey(Sector)
    weight = models.IntegerField("Weight", help_text="Controls ordering of Subsectors", blank=True, default=0)
    
        
# fund type

# budget function

# recipient type
