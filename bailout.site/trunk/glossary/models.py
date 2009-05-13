from django.db import models
from django.contrib import admin

class Item(models.Model):
    slug       = models.SlugField(db_index=True, unique=True)
    term       = models.CharField(max_length=255, unique=True, db_index=True)
    definition = models.TextField()

admin.site.register(Item)
