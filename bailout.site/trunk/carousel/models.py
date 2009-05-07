from django.db import models
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
        return settings.MEDIA_ROOT + 'images/carousel_image_%s' % filename
    
    def _get_weight_choices():
        r = ()
        for i in range(-10,10):
            r += ((i,i),)
        return r
    
    title = models.CharField('Title', max_length=100)
    link = models.CharField("Link", max_length=200, blank=True, default='')
    image = models.ImageField('Image', upload_to=_get_image_upload_path, blank=True, null=True, help_text='415 x 241px')
    date = models.DateField('Date')
    text = models.TextField('Text', default='')    
    weight = models.IntegerField("Weight", default=0, blank=False, choices=_get_weight_choices())
    published = models.BooleanField('Published?', default=False)
