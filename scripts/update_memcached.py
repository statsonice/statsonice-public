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
from django import db

from statsonice.models import *
from includes import progressindicator

if 'dummy' in settings.CACHES['default']['BACKEND']:
    print 'Running dummy backend - not caching'
    sys.exit()

total_count = SkaterResult.objects.count()
total_count += Program.objects.count()
total_count += ElementScore.objects.count()
total_count += Skater.objects.count()
total_count += SkaterName.objects.count()
total_count += SkaterTeam.objects.count()
progress_indicator = progressindicator.ProgressIndicator(total_count, db)

try:
    print "SkaterResult"
    for skaterresult in SkaterResult.objects.iterator():
        skaterresult.url()
        progress_indicator.next()

    print "Program"
    for program in Program.objects.iterator():
        program.view_name()
        program.url_segment_summary()
        progress_indicator.next()

    print "ElementScore"
    for elementscore in ElementScore.objects.iterator():
        elementscore.get_element_name()
        progress_indicator.next()

    print "Skater"
    for skater in Skater.objects.iterator():
        skater.view_name()
        skater.url()
        progress_indicator.next()

    print "SkaterTeam"
    for skaterteam in SkaterTeam.objects.iterator():
        skaterteam.view_name()
        skaterteam.url_name()
        skaterteam.url()
        skaterteam.is_dance()
        progress_indicator.next()
except:
    subject = 'Update Memcached Script Failure'
    message = traceback.format_exc()
    from_email = 'bot@statsonice.com'
    recipient_list = ['team@statsonice.com']
    send_mail(subject, message, from_email, recipient_list)
