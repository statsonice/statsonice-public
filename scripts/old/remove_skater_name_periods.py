"""
This hacked up script removes periods from skater names
"""

import os
import sys
parent_path = os.path.dirname(os.path.realpath(__file__))+'/../../util/'
sys.path.append(parent_path)
from get_settings import load_settings
load_settings(sys.argv)

from statsonice.models import *
for skater_name in SkaterName.objects.filter(last_name__contains='.'):
    skater_name.last_name = skater_name.last_name.replace('.','')
    orig_last_name = skater_name.last_name
    try:
        if skater_name.last_name[1] == ' ':
            skater_name.last_name = skater_name.last_name[2:]

        skater_name.save()
    except:
        skater_name.last_name = orig_last_name
        skater_name.save()
    print skater_name

