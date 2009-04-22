from django.db import models

class Sector(models.Model):

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = 'Sector'

    name = models.CharField("Name", max_length=40)
