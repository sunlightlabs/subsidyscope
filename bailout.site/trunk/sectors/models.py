from django.db import models
from django.conf import settings

class Sector(models.Model):

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = 'Sector'

    name = models.CharField("Name", max_length=40)
    
    def image_url_small(self):
        
        return settings.MEDIA_URL + 'images/sector/' + str(self.id) + '_sm.png'

    def image_url_large(self):
        
        return settings.MEDIA_URL + 'images/sector/' + str(self.id) + '_lg.png'

# fund type

# budget function

