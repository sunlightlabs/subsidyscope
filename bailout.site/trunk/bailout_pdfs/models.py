import sys, os
from django.db import models
from django.core.files.storage import FileSystemStorage
from sectors.models import *

def BailoutPDF_get_pdf_upload_path(instance, filename):
    return "pdf/%d/%d/%d/%s" % (instance.date.year, instance.date.month, instance.date.day, filename)

BailoutPDF_FileSystemStorage = FileSystemStorage(location=('%s/media' % os.path.abspath(os.path.dirname(sys.argv[0]))), base_url='/media/pdf')

class BailoutPDF(models.Model):    
    class Meta:
        verbose_name = 'Bailout PDF'
        ordering = ['-date']
    def __unicode__(self):
        return self.title
    title = models.CharField("Title",max_length=255)
    date = models.DateField("Date")
    sector = models.ForeignKey(Sector, null=False)
    link_url = models.URLField("Link", blank=True, default='')
    CHOICES = (
        ('PDF', 'PDF'),
        ('Link', 'Link'),
    )
    document_type = models.CharField("Type", max_length=15, choices=CHOICES, default='PDF', blank=True, null=True)
    source_name = models.CharField("Source Name", max_length=255, blank=True, default='')
    source_url = models.URLField("Source URL", blank=True, default='')
    scribd_url = models.URLField("Scribd URL", blank=True, default='')   
    #scribd_embed_code = models.TextField("Scribd Embed Code", blank=True, default='')
    #scribd_access_key = models.CharField("Scribd Document Access Key", max_length=255) 
    description = models.TextField("Description", blank=True, default='')
    local_copy = models.FileField("File", upload_to=BailoutPDF_get_pdf_upload_path, storage=BailoutPDF_FileSystemStorage, blank=True)
    AGENCY_CHOICES = (
        ('Federal Reserve', 'Federal Reserve'),
        ('Treasury Department', 'Treasury Department'),
        ('FDIC', 'Federal Deposit Insurance Corporation'),
        ('', 'Other')
    )
    agency = models.CharField("Agency", blank=True, max_length=100, default='', choices=AGENCY_CHOICES)
    
