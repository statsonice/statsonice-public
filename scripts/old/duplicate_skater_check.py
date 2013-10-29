#!/usr/bin/env python
"""
This script checks the database for duplicate skaters
"""

import os
import sys
parent_path = os.path.dirname(os.path.realpath(__file__))+'/../../util/'
sys.path.append(parent_path)
from get_settings import load_settings
load_settings(sys.argv)

from statsonice.models import *

found_skatername_ids = []
for skatername in SkaterName.objects.all():
    skaternames = SkaterName.objects.filter(first_name = skatername.first_name, last_name = skatername.last_name)
    skatername_ids = skaternames.values_list('skater',flat=True).distinct()
    if skatername_ids.count() > 1:
        already_found = False
        for skatername_id in skatername_ids:
            if skatername_id in found_skatername_ids:
                already_found = True
                break
        if already_found:
            continue
        print "DUPLICATE SKATERS FOUND!"
        print skaternames
        found_skatername_ids += skatername_ids

for skater in Skater.objects.all():
    if skater.skatername_set.count() == 0:
        print "NO NAME SKATER FOUND!"
        print skater
