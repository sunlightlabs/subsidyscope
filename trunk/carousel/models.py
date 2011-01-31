from django.db import models
from sectors.models import *
import settings

class CarouselEntry(models.Model):
    def __unicode__(self):
        if not self.published:
            return '%s (draft)' % self.title
        else:
            return self.title
        
    class Meta:
        verbose_name = 'Carousel Entry'
        verbose_name_plural = 'Carousel Entries'
        ordering = ['weight'] 

    def _get_image_upload_path(instance, filename):
        return 'images/carousel_image_%s' % filename
    
    def _get_weight_choices():
        r = ()
        for i in range(-10,10):
            r += ((i,i),)
        return r
    
    title = models.CharField('Title', max_length=100)
    link = models.CharField("Link", max_length=200, blank=True, default='')
    image = models.CharField('Image', blank=True, max_length=100)
    date = models.DateField('Date', blank=True, null=True)
    text = models.TextField('Text', default='')    
    weight = models.IntegerField("Weight", default=0, blank=False, choices=_get_weight_choices())
    published = models.BooleanField('Published?', default=False)
    sector = models.ForeignKey(Sector, blank=True, null=True)
