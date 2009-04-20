from managers import MorselManager
from exceptions import LockedError

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from rcsfield.fields import RcsTextField
from rcsfield.manager import RevisionManager

class Morsel(models.Model):
    url = models.CharField(_('url'), max_length=100, db_index=True, unique=True,
        help_text=_("""
            The URL of the page in which this morsel should be shown, followed by an optional
            name. Examples: '/', '/contact/', '/contact/sidebar'.
            Make sure to have leading and trailing slashes for the page url, but no slash
            after the morsel name."""))
    title = models.CharField(_('title'), max_length=80, blank=True)
    
    content = RcsTextField()    
    objects = RevisionManager()
    
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    locked = models.BooleanField(_('locked'), default=False,
        help_text=_("""
            Locked morsels cannot be deleted. Think twice before unlocking a morsel,
            as there is likely to be a good reason for it to be locked."""))

    objects = MorselManager()

    class Meta:
        verbose_name = _('morsel')
        verbose_name_plural = _('morsels')
        ordering = ('url',)

    def __unicode__(self):
        return u'%s -- %s' % (self.url, self.title)

    def delete(self):
        if self.locked:
            raise LockedError('Morsel "%s" cannot be deleted.' % self)
        super(Morsel, self).delete()
