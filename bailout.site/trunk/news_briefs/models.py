from django.db import models

class NewsBrief(models.Model):
    date = models.DateField("Date")
    source = models.CharField("Source", max_length=128, default='')
    text = models.TextField("Text", default='')
    link = models.URLField("URL")
    def __unicode__(self):
        return "%s - %s" % (self.date, self.link)