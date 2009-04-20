#!/bin/sh
export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=$PYTHONPATH:/Users/thomaslee/Projects/subsidyscope/bailout.site/trunk
pdftotext -layout $1 - | python tarp_process_pdf.py --parse