#!/bin/sh
export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=$PYTHONPATH:/Users/thomaslee/Projects/subsidyscope.git/bailout.site/trunk
python /Users/thomaslee/Projects/subsidyscope.git/bailout.site/trunk/manage.py sqlclear cfda | mysql -u root -D subsidyscope_staging && python /Users/thomaslee/Projects/subsidyscope.git/bailout.site/trunk/manage.py syncdb
cat CFDA.txt | python cfda_importer.py