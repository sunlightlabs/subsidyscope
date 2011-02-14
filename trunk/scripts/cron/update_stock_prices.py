#!/usr/bin/env python
import os, sys

sys.path.append('/home/subsidyscope/lib/python/subsidyscope/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from bailout.models import * 

Institution.objects.updateTARPParticipation()
Institution.objects.updateStockPrices()