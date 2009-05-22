# r"""
# >>> from morsels.models import Morsel
# 
# # remove typogrify and sites apps for testing
# >>> from django.conf import settings
# >>> original_INSTALLED_APPS = settings.INSTALLED_APPS
# >>> if 'typogrify' in settings.INSTALLED_APPS: settings.INSTALLED_APPS.remove('typogrify')
# >>> if 'sites' in settings.INSTALLED_APPS: settings.INSTALLED_APPS.remove('sites')
# 
# # test creating a morsel
# >>> m1 = Morsel.objects.create(url='/', title='M1', content='Morsel 1')
# >>> m1
# <Morsel: / -- M1>
# 
# # create a few more morsels
# >>> m2 = Morsel.objects.create(url='/section1/info', title='M2', content='Morsel 2')
# >>> m3 = Morsel.objects.create(url='/section1/page1/info', title='M3', content='Morsel 3')
# >>> m4 = Morsel.objects.create(url='/section1/page1/', title='M4', content='Morsel 4')
# 
# # morsel url must be unique
# >>> m5 = Morsel.objects.create(url='/section1/page1/info', content='Morsel 5')
# Traceback (most recent call last):
#     ...
# IntegrityError: ...
# 
# # create a locked morsel
# >>> m6 = Morsel.objects.create(url='/section1/page2/', locked=True)
# >>> m6.delete()
# Traceback (most recent call last):
#     ...
# LockedError: Morsel "/section1/page2/ -- " cannot be deleted.
# 
# >>> m6.locked = False
# >>> m6.save()
# >>> m6.delete()
# 
# # set up a dummy request context, for rendering templates at specific url's
# >>> from django.template import Context
# >>> from django.template.loader import get_template_from_string
# >>> from django.http import HttpRequest
# >>> r = HttpRequest()
# >>> c = Context({'request': r})
# 
# # the simplest morsel tag - find morsel by page url only
# >>> t = get_template_from_string('{% load morsel_tags %}{% morsel %}')
# >>> r.path = '/'
# >>> t.render(c)
# u'Morsel 1'
# 
# >>> r.path = '/section1/'
# >>> t.render(c)
# u''
# 
# >>> r.path = '/section1/page1/'
# >>> t.render(c)
# u'Morsel 4'
# 
# # tag variation - find morsel with a custom name (url suffix)
# >>> t = get_template_from_string('{% load morsel_tags %}{% morsel info %}')
# >>> r.path = '/'
# >>> t.render(c)
# u''
# 
# >>> r.path = '/section1/'
# >>> t.render(c)
# u'Morsel 2'
# 
# >>> r.path = '/section1/page1/'
# >>> t.render(c)
# u'Morsel 3'
# 
# # another variation - find morsel with inheritance
# >>> t = get_template_from_string('{% load morsel_tags %}{% morsel inherit %}')
# >>> r.path = '/section1/page1/'
# >>> t.render(c)
# u'Morsel 4'
# 
# >>> r.path = '/section1/'
# >>> t.render(c)
# u'Morsel 1'
# 
# >>> r.path = '/section1/page2/'
# >>> t.render(c)
# u'Morsel 1'
# 
# >>> r.path = '/section1/page1/subpage/'
# >>> t.render(c)
# u'Morsel 4'
# 
# # test inserting morsel into context
# >>> t = get_template_from_string('{% load morsel_tags %}{% morsel as var %}{{ var.title }}')
# >>> r.path = '/section1/page1/'
# >>> t.render(c)
# u'M4'
# 
# >>> c
# [{u'var': <Morsel: /section1/page1/ -- M4>, ...
# ...
# 
# >>> r.path = '/section1/page2/'
# >>> c = Context({'request': r}) # new context to remove previous morsel
# >>> t.render(c)
# u''
# 
# # test withmorsel tag
# >>> t = get_template_from_string('{% load morsel_tags %}{% withmorsel %}{{ morsel.content }}{% endwithmorsel %}')
# >>> r.path = '/section1/page1/'
# >>> c = Context({'request': r})
# >>> t.render(c)
# u'Morsel 4'
# 
# # ... and with custom name and 'as'
# >>> t = get_template_from_string('{% load morsel_tags %}{% withmorsel info as var %}{{ var.content }}{% endwithmorsel %}')
# >>> r.path = '/section1/'
# >>> t.render(c)
# u'Morsel 2'
# 
# # ... and with inheritance
# >>> t = get_template_from_string('{% load morsel_tags %}{% withmorsel inherit %}{{ morsel.content }}{% endwithmorsel %}')
# >>> r.path = '/section1/'
# >>> t.render(c)
# u'Morsel 1'
# 
# # test morsel lookup with Sites enabled
# >>> from django.contrib.sites.models import Site
# >>> settings.INSTALLED_APPS.append('sites')
# >>> s = Site.objects.get_current()
# >>> m = Morsel.objects.create(url='/site/', title='AM', content='A Morsel')
# >>> m.sites.add(s)
# >>> r.path = '/site/'
# >>> t.render(c)
# u'A Morsel'
# 
# # cleanup
# >>> settings.INSTALLED_APPS = original_INSTALLED_APPS
# """
