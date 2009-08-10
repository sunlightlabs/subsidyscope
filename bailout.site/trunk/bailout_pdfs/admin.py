from bailout_pdfs.models import *
from django.contrib import admin

class BailoutPDFAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['document_type', 'agency', 'sector', 'date', 'title', 'description', 'link_url', 'local_copy']}),
        ('Source', {'fields': ['source_name', 'source_url']}),
        #('Scribd', {'fields': ['scribd_url']}),
        
    ]

admin.site.register(BailoutPDF, BailoutPDFAdmin)
