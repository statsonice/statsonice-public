"""
This file tries to render every model that has a page associated with it
"""

import os
import sys
parent_path = os.path.dirname(os.path.realpath(__file__))+'/../../util/'
sys.path.append(parent_path)
from get_settings import load_settings
load_settings(sys.argv)
import gc

from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response

from statsonice.models import *
from includes.progressindicator import ProgressIndicator

def load_url(url):
    #print url
    view, args, kwargs = resolve(url)
    kwargs['request'] = None
    view(*args, **kwargs)

total = Skater.objects.count() + SkaterPair.objects.count()
total += Competition.objects.count() + Program.objects.count()*2
progress_indicator = ProgressIndicator(total)

for skater in Skater.objects.all():
    url = skater.url()
    load_url(url)
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()
print 'Skater tests done'

for skater_pair in SkaterPair.objects.all():
    url = skater_pair.url()
    load_url(url)
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()
print 'Skater pair tests done'

for competition in Competition.objects.all():
    url = competition.url()
    load_url(url)
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()
print 'Competition tests done'

for program in Program.objects.all():
    url = program.url()
    load_url(url)
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()
    url = program.url_segment_summary()
    load_url(url)
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()
