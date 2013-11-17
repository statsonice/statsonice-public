"""
This file validates that foreign keys are pointing to the correct location
"""

import os
import sys
parent_path = os.path.dirname(os.path.realpath(__file__))+'/../../util/'
sys.path.append(parent_path)
from get_settings import load_settings
load_settings(sys.argv)

from statsonice.models import *
from includes.progressindicator import ProgressIndicator

def get_values_list(model):
    return model.objects.values_list('pk', flat=True)


def check_foreign_keys(model, keys):
    for instance in model.objects.all():
        for (from_key, to_keys, special) in keys:
            if special == 'many':
                for pk in instance.__getattribute__(from_key).values_list('pk', flat=True):
                    if pk not in to_keys:
                        print instance, from_key
            else:
                if special == 'allow_none' and instance.__getattribute__(from_key) == None:
                    continue
                if instance.__getattribute__(from_key) not in to_keys:
                    print instance, from_key
        progress_indicator.next()

foreign_keys = {
    City : [
        ('country_id', get_values_list(Country), 'allow_none'),
    ],
    Skater : [
        ('country_id', get_values_list(Country), 'allow_none'),
        ('home_city_id', get_values_list(City), 'allow_none'),
        ('training_city_id', get_values_list(City), 'allow_none'),
        ('coach', get_values_list(Coach), 'many'),
        ('choreographer', get_values_list(Coach), 'many'),
    ],
    SkaterName : [
        ('skater_id', get_values_list(Skater), None),
    ],
    SkaterMetadata : [
        ('skater_id', get_values_list(Skater), None),
    ],
    SkaterTeam : [
        ('female_skater_id', get_values_list(Skater), None),
        ('male_skater_id', get_values_list(Skater), None),
        ('country_id', get_values_list(Country), 'allow_none'),
        ('coach', get_values_list(Coach), 'many'),
        ('choreographer', get_values_list(Coach), 'many'),
    ],
    Competitor : [
        ('skater_team_id', get_values_list(SkaterTeam), 'allow_none'),
        ('skater_id', get_values_list(Skater), 'allow_none'),
    ],
    Competition : [
        ('country_id', get_values_list(Country), 'allow_none'),
        ('cutoff_id', get_values_list(CompetitionCutoff), 'allow_none'),
    ],
    SkaterResult : [
        ('competitor_id', get_values_list(Competitor), None),
        ('competition_id', get_values_list(Competition), None),
        ('category_id', get_values_list(Category), None),
        ('level_id', get_values_list(Level), None),
    ],
    Program : [
        ('skater_result_id', get_values_list(SkaterResult), None),
        ('segment_id', get_values_list(Segment), None),
    ],
    ResultIJS : [
        ('program_id', get_values_list(Program), None),
    ],
    ElementScore : [
        ('result_id', get_values_list(ResultIJS), None),
        ('flag_id', get_values_list(Flag), 'allow_none'),
    ],
    Element : [
        ('element_score_id', get_values_list(ElementScore), None),
        ('base_element_id', get_values_list(BaseElement), None),
        ('modifiers', get_values_list(Modifier), 'many'),
    ],
    ProgramComponentScore : [
        ('result_id', get_values_list(ResultIJS), None),
        ('component_id', get_values_list(Component), None),
        ('flag_id', get_values_list(Flag), 'allow_none'),
    ],
    ProgramComponentJudge : [
        ('program_component_score_id', get_values_list(ProgramComponentScore), None),
    ],
}

total = 0
for model in foreign_keys:
    total += model.objects.count()
print 'Total:',total
progress_indicator = ProgressIndicator(total)


for model, keys in foreign_keys.items():
    print 'Starting', model
    check_foreign_keys(model, keys)
    print "\n"
    print 'Finished', model

