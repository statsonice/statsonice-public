"""
This file prepopulates the database with all the choices from each enum table
"""
import os
import sys
parent_path = os.path.dirname(os.path.realpath(__file__))+'/../util/'
sys.path.append(parent_path)
from get_settings import load_settings
load_settings(sys.argv)

from statsonice.models.location import Country
from statsonice.models.enums import *

def load_model_from_choices(model, field, choices):
    for abbreviation, full in choices:
        a = model(**{field:abbreviation})
        a.save()

print 'Loading Country Enums'
load_model_from_choices(Country, 'country_name', Country.COUNTRY_CHOICES)

print 'Loading Category Enums'
load_model_from_choices(Category, 'category', Category.CATEGORY_CHOICES)

print 'Loading Component Enums'
load_model_from_choices(Component, 'component', Component.COMPONENT_CHOICES)

print 'Loading Level Enums'
load_model_from_choices(Level, 'level', Level.LEVEL_CHOICES)

print 'Loading Modifier Enums'
load_model_from_choices(Modifier, 'modifier', Modifier.MODIFIER_CHOICES)

print 'Loading Segment Enums'
load_model_from_choices(Segment, 'segment', Segment.SEGMENT_CHOICES)

print 'Loading BaseElement Enums'
load_model_from_choices(BaseElement, 'element_name', BaseElement.BASE_ELEMENT_CHOICES)
