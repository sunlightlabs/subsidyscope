from django.db import models

class DataSource(models.Model):
    def __unicode__(self):
        return self.name    
    class Meta:
        verbose_name = "Data Source"
    name = models.CharField("Name", max_length=50)
    url = models.CharField("URL", max_length=255, blank=True)
    
class DataRun(models.Model):
    def __unicode__(self):
        return '%s - %s' % (self.source.name, str(self.date))
    class Meta:
        verbose_name = "Data Run"
    source = models.ForeignKey(DataSource)
    date = models.DateTimeField(auto_now_add=True)
    records_inserted = models.IntegerField("Records Inserted", blank=True, default=0 )
    records_updated = models.IntegerField("Records Updated", blank=True, default=0)
    records_deleted = models.IntegerField("Records Deleted", blank=True, default=0)
        