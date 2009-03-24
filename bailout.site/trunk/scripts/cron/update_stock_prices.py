#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from bailout.models import * 

Institution.objects.updateStockPrices()