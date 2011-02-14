from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from bailout_pdfs.models import *
from sectors.models import *

info_dict = {
    'queryset': BailoutPDF.objects.all().order_by('sector', '-date'),
    'extra_context': {'sectors': Sector.objects.all()}
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', info_dict, name='bailoutpdf_index'),
    url(r'^(?P<pdf_id>\d+)/$', 'bailout_pdfs.views.detail', name='bailoutpdf_detail')
)


