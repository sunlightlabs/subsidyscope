from managers import MorselManager, PageManager
from exceptions import LockedError

from django.db import models
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from rcsfield.fields import RcsTextField
from rcsfield.manager import RevisionManager
from sectors.models import Sector 

class Page(models.Model):
    
    class Meta:
        verbose_name = 'Morsel Page'
        ordering = ['url']
    
    sector = models.ForeignKey(Sector, blank=True, null=True)
    
    url = models.CharField(_('url'), max_length=100, db_index=True, unique=True,
        help_text=_("""
            The URL of the page in which this morsel should be shown, followed by an optional
            name. Examples: '/', '/contact/', '/contact/sidebar'.
            Make sure to have leading and trailing slashes for the page url, but no slash
            after the morsel name."""))
    
    title = models.CharField(_('title'), max_length=255, blank=True)

    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    
    objects = PageManager()
    
    def __unicode__(self):
        
        return u'%s' % (self.url)
    

class Morsel(models.Model):
    
    page = models.ForeignKey(Page) 
    
    name = models.CharField(_('name'), max_length=100, db_index=True)
    
    content = RcsTextField("Content")    
    # objects = RevisionManager()
    
    locked = models.BooleanField(_('locked'), default=False,
        help_text=_("""
            Locked morsels cannot be deleted. Think twice before unlocking a morsel,
            as there is likely to be a good reason for it to be locked."""))

    objects = MorselManager()

    class Meta:
        verbose_name = _('morsel')
        verbose_name_plural = _('morsels')
        ordering = ('name',)

    def __unicode__(self):
        return u'%s -- %s' % (self.page.url, self.name)

    def get_flat_text(self):
        import lxml.html
    
        c = Context()
        t = Template(self.content)
        raw_output = t.render(c)
    
        return raw_output

    def delete(self):
        if self.locked:
            raise LockedError('Morsel "%s" cannot be deleted.' % self)
        super(Morsel, self).delete()


#class OldMorselManager(models.Manager):
#    
#    def update_morsels(self):
#
#        site = Site.objects.get(pk=1)
#
#        for morsel in self.all():
#            
#            url_parts = morsel.url.split('/')
#            
#            morsel_name = url_parts.pop()
#            
#            page_url = '/'.join(url_parts)
#            
#            try:
#                page = Page.objects.get(url=page_url)
#            except Page.DoesNotExist:
#                
#                page = Page.objects.create(url=page_url)
#                page.sites.add(site)
#                page.save()
#                
#            
#            Morsel.objects.create(page=page, content=morsel.content, name=morsel_name)
#            
#            
#            
#            
#            
#
#
#class OldMorsel(models.Model):
#    url = models.CharField(_('url'), max_length=100, db_index=True, unique=True,
#        help_text=_("""
#            The URL of the page in which this morsel should be shown, followed by an optional
#            name. Examples: '/', '/contact/', '/contact/sidebar'.
#            Make sure to have leading and trailing slashes for the page url, but no slash
#            after the morsel name."""))
#    title = models.CharField(_('title'), max_length=80, blank=True)
#    
#    content = RcsTextField("Content")    
#    # objects = RevisionManager()
#    
#    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
#    locked = models.BooleanField(_('locked'), default=False,
#        help_text=_("""
#            Locked morsels cannot be deleted. Think twice before unlocking a morsel,
#            as there is likely to be a good reason for it to be locked."""))
#
#    objects = OldMorselManager()
#
#    class Meta:
#        verbose_name = _('morsel')
#        verbose_name_plural = _('morsels')
#        ordering = ('url',)
#
#    def __unicode__(self):
#        return u'%s -- %s' % (self.url, self.title)
#
#    def delete(self):
#        if self.locked:
#            raise LockedError('Morsel "%s" cannot be deleted.' % self)
#        super(Morsel, self).delete()
