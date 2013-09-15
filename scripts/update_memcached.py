#!/usr/bin/python
"""
This file updates memcached with cached data from models
"""
import os
import sys
parent_path = os.path.dirname(os.path.realpath(__file__))+'/../util/'
sys.path.append(parent_path)
from get_settings import load_settings
load_settings(sys.argv)
import traceback

from django.conf import settings

from statsonice.models import *
from includes import progressindicator

if 'dummy' in settings.CACHES['default']['BACKEND']:
    print 'Running dummy backend - not caching'
    sys.exit()

total_count = Competition.objects.count()
total_count += SkaterResult.objects.count()
total_count += Program.objects.count()
total_count += ElementScore.objects.count()
total_count += Skater.objects.count()
total_count += SkaterName.objects.count()
total_count += SkaterTeam.objects.count()
progress_indicator = progressindicator.ProgressIndicator(total_count)

try:
    print "Competition"
    for competition in Competition.objects.all():
        competition.view_name()
        competition.url()
        progress_indicator.next()

    print "SkaterResult"
    for skaterresult in SkaterResult.objects.all():
        skaterresult.url()
        skaterresult.withdrawal()
        progress_indicator.next()

    print "Program"
    for program in Program.objects.all():
        program.view_name()
        program.url_segment_summary()
        progress_indicator.next()

    print "ElementScore"
    for elementscore in ElementScore.objects.all():
        elementscore.get_element_name()
        progress_indicator.next()

    print "Skater"
    for skater in Skater.objects.all():
        skater.view_name()
        skater.url()
        progress_indicator.next()

    print "SkaterName"
    for skatername in SkaterName.objects.all():
        skater.view_name()
        skater.url_name()
        progress_indicator.next()

    print "SkaterTeam"
    for skaterteam in SkaterTeam.objects.all():
        skaterteam.view_name()
        skaterteam.url_name()
        skaterteam.url()
        skaterteam.is_dance()
        progress_indicator.next()
except:
    log_file_location = '/home/albertyw/memcached_log'
    log_file = open(log_file_location,'w')
    traceback.print_exc(file=log_file)
    log_file.close()
