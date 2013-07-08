"""
This script combines skaters and skater pairs into a single skater
"""

import os
import sys
parent_path = os.path.dirname(os.path.realpath(__file__))+'/../../util/'
sys.path.append(parent_path)
from get_settings import load_settings
load_settings(sys.argv)

from statsonice.models import *

def combine_skaters(skaters):
    correct_skater = skaters[0]
    skaters_to_combine = skaters[1:]

    # Check that skaters are all pairs or all singles
    skater_type = type(correct_skater)
    for skater in skaters_to_combine:
        if type(skater) != skater_type:
            raise ValueError("Cannot combine pairs and singles competitors")

    # Get competitors
    competitors = []
    for skater in list(skaters_to_combine)+[correct_skater]:
        competitors += skater.competitor_set.all()
    correct_competitor = competitors.pop()
    print "Using", correct_competitor
    if type(correct_skater) == Skater:
        correct_competitor.skater = correct_skater
    elif type(correct_skater) == SkaterPair:
        correct_competitor.skater_pair = correct_skater


    # Copy over skaterresults
    for competitor in competitors:
        for skaterresult in competitor.skaterresult_set.all():
            skaterresult.competitor = correct_competitor
            print "Changing ", skaterresult
            skaterresult.save()

    # Delete competitor
    for competitor in competitors:
        print "deleting", competitor
        competitor.delete()
    correct_competitor.save()

    if type(correct_skater) == Skater:
        # Merge skater pair values
        for skater_to_combine in skaters_to_combine:
            for coach in skater_to_combine.coach.all():
                if coach not in correct_skater.coach.all():
                    skater.coach.add(coach)
            for choreographer in skater_to_combine.choreographer.all():
                if choreographer not in correct_skater.coach.all():
                    correct_skater.choreographer.add(choreographer)
        # TODO
    elif type(correct_skater) == SkaterPair:
        # Merge skater values
        # TODO
        pass

    # Delete extra skaters
    for skater in skaters_to_combine:
        print "Deleting", skater
        skater.delete()
    correct_skater.save()
