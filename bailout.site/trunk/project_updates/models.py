from django.db import models
import sectors.models
import sunlightcore.management.commands.mediasync

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

    PROJECT_CHOICES = (
        ('Bailout', 'The Financial Bailout'),
    )
    title = models.CharField('Title', max_length=100)
    link = models.CharField("Link", max_length=200, blank=True, default='')
    image = models.ImageField('Image', upload_to=_get_image_upload_path, blank=True, null=True)
    date = models.DateField('Date')
    text = models.TextField('Text', default='')
    extended_text = models.TextField('Extended Text', default='', blank=True)
    slug = models.SlugField('Slug', default='')
    #project = models.CharField("Project", max_length=50, choices=PROJECT_CHOICES, blank=True, null=True, default='Bailout')
    sectors = models.ManyToManyField(sectors.models.Sector, blank=True)
    published = models.BooleanField('Published?', default=False)
