from django.db import models
from sectors.models import Sector, Subsector

class SubsidyType(models.Model):
    
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        
        return self.name
    

class ProjectUpdate(models.Model):
    def __unicode__(self):
        if not self.published:
            return '%s (draft)' % self.title
        else:
            return self.title
        
    class Meta:
        verbose_name = 'Project Update'
        ordering = ['-date'] 

    def _get_image_upload_path(instance, filename):
        return 'images/project_update_image_%s' % filename
        
    @models.permalink
    def get_absolute_url(self):
        return ('project_update_permalink', (), {
            'entry_year': self.date.year,
            'entry_month': self.date.month,
            'entry_day': self.date.day,
            'entry_slug': self.slug})
    
    title = models.CharField('Title', max_length=100)
    link = models.CharField("Link", max_length=200, blank=True, default='')
    image = models.CharField('Image', blank=True, max_length=100)
    date = models.DateField('Date')
    text = models.TextField('Text', default='')
    extended_text = models.TextField('Extended Text', default='', blank=True)
    slug = models.SlugField('Slug', default='')
 
   
    subsidy_type = models.ManyToManyField(SubsidyType, blank=True)
    
    sectors = models.ManyToManyField(Sector, blank=True)
    subsector = models.ManyToManyField(Subsector, blank=True)
    
    published = models.BooleanField('Published?', default=False)
