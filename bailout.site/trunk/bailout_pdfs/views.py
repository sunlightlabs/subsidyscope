import settings
from django.shortcuts import render_to_response, get_object_or_404
from bailout_pdfs.models import BailoutPDF
import datetime

# much of this configuration stuff should probably go live in local_settings.py
# otoh, it's still just a one-off...

def detail(request, pdf_id):
    pdf = get_object_or_404(BailoutPDF, pk=pdf_id)
    
    return render_to_response('bailout_pdfs/bailoutpdf_detail.html', {'pdf': pdf, 'scribd_publisher_id': settings.SCRIBD_PUBLISHER_ID})
