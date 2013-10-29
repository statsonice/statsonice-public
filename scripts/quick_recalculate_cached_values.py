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


num_comps = 1
comps = Competition.objects.all()
comps = comps[len(comps)-num_comps:]

#comps = Competition.objects.filter(name='Skate America',start_date__year=2013)
skater_results = [c.skaterresult_set.all() for c in comps]
skater_results = [sr for skater_result in skater_results for sr in skater_result]
programs = [sr.program_set.all() for sr in skater_results]
results = [p.resultijs for program in programs for p in program]
element_scores = [es for r in results for es in r.elementscore_set.all()]
program_component_scores = [pcs for r in results for pcs in r.programcomponentscore_set.all()]

# Set up progress indicator
total_count = len(list(results)) + len(list(skater_results*2))
total_count += len(list(element_scores)) + len(list(program_component_scores))
progress_indicator = progressindicator.ProgressIndicator(total_count)

# Recalculate ResultIJS
print "ResultIJS"
for resultijs in results:
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
for skater_result in skater_results:
    # These functions implicitly update the model themselves
    skater_result.calculate_withdrawal()
    skater_result.calculate_total_score()
    skater_result.save()
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()

print "SkaterResult final rank"
for skater_result in skater_results:
    # These functions implicitly update the model themselves
    skater_result.calculate_final_rank()
    skater_result.save()
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()

# Recalculate element score
print "ElementScore flag"
for element_score in element_scores:
    # These functions implicitly update the model themselves
    element_score.calculate_flag()
    element_score.save()
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()

# Recalculate program component score
print "ProgramComponentScore flag"
for program_component_score in program_component_scores:
    # These functions implicitly update the model themselves
    program_component_score.calculate_flag()
    program_component_score.save()
    progress_indicator.next()
    if progress_indicator.count % 1000 == 0:
        gc.collect()
