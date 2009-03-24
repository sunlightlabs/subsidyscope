from django.db import models
import datetime
import md5
import random

class Recipient(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=5, blank=True, null=True)
    subscribed = models.BooleanField(default=True)
    hashcode = models.CharField(max_length=128, blank=True)
    def save(self):
        if not self.id:
            if self.email:
                self.hashcode = md5.new(self.email).hexdigest()
        super(Recipient, self).save()
    def __unicode__(self):
        return "%s %s" % (self.email, self.zipcode)