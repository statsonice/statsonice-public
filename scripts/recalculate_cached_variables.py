#!/usr/bin/python
"""
This file creates fake data to be used when developing the website
"""
import os
import sys
parent_path = os.path.dirname(os.path.realpath(__file__))+'/../util/'
sys.path.append(parent_path)
from get_settings import load_settings
load_settings(sys.argv)
import gc

from statsonice.models import *
from includes import progressindicator

# Set up progress indicator
total_count = ResultIJS.objects.count() + SkaterResult.objects.count()*2
total_count += ElementScore.objects.count() + ProgramComponentScore.objects.count()
progress_indicator = progressindicator.ProgressIndicator(total_count)

# Recalculate ResultIJS
print "ResultIJS"
for resultijs in ResultIJS.objects.all():
    # These functions implicitly update the model themselves
    resultijs.calculate_tes()
    resultijs.calculate_pcs()
    resultijs.calculate_tss()
    resultijs.save()
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()

# Recalculate skater result
print "SkaterResult total score"
for skater_result in SkaterResult.objects.all():
    # These functions implicitly update the model themselves
    skater_result.calculate_total_score()
    skater_result.save()
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()
print "SkaterResult final rank"
for skater_result in SkaterResult.objects.all():
    # These functions implicitly update the model themselves
    skater_result.calculate_final_rank()
    skater_result.save()
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()

# Recalculate element score
print "ElementScore flag"
for element_score in ElementScore.objects.all():
    # These functions implicitly update the model themselves
    element_score.calculate_flag()
    element_score.save()
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()

# Recalculate program component score
print "ProgramComponentScore flag"
for program_component_score in ProgramComponentScore.objects.all():
    # These functions implicitly update the model themselves
    program_component_score.calculate_flag()
    program_component_score.save()
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()
