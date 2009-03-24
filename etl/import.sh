#!/bin/bash
export DJANGO_SETTINGS_MODULE='settings'
export PYTHONPATH=/Users/thomaslee/Projects/subsidyscope/bailout.site/trunk:$PYTHONPATH
python ./SubsidyExtractor.py $1 $2