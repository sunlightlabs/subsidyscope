#!/bin/sh
export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=$PYTHONPATH:/Users/thomaslee/Projects/subsidyscope/bailout.site/trunk
cat $1 | python tarp_import_from_csv.py