#!/usr/bin/python
"""
This file creates fake data to be used when developing the website
"""
from datetime import datetime
import os
import sys
parent_path = os.path.dirname(os.path.realpath(__file__))+'/../../util/'
sys.path.append(parent_path)
from get_settings import load_settings
load_settings(sys.argv)

from statsonice.models import *

# TODO
# program.segment issue

# Create city
print "Creating Cities"
City.objects.all().delete()
City(city_name='Boston', country=Country.objects.get(country_name='USA')).save()
City(city_name='Paris', country=Country.objects.get(country_name='FRA')).save()
City(city_name='Milan', country=Country.objects.get(country_name='ITA')).save()
City(city_name='Moscow', country=Country.objects.get(country_name='RUS')).save()

# Coaches
print "Creating Coaches"
Coach.objects.all().delete()
Coach(first_name='John', last_name='Doe').save()
Coach(first_name='Jane', last_name='Doe').save()
Coach(first_name='Mama', last_name='Bear').save()
Coach(first_name='Papa', last_name='Bear').save()
Coach(first_name='Baby', last_name='Bear').save()

# Create skaters
print "Creating Skaters"
Skater.objects.all().delete()
skater1 = Skater()
skater1.country = Country.objects.get(country_name='USA')
skater1.dob = datetime.strptime('January 2, 1993', '%B %d, %Y')
skater1.gender = 'M'
skater1.height = 100
skater1.home_city = City.objects.get(city_name='Boston', country=Country.objects.get(country_name='USA'))
skater1.training_city = City.objects.get(city_name='Moscow', country=Country.objects.get(country_name='RUS'))
skater1.start_year = 2010
skater1.save()
skater1.coach = [Coach.objects.get(first_name='Mama', last_name='Bear')]
skater1.choreographer = [Coach.objects.get(first_name='Papa', last_name='Bear')]
skater1.save()

skater2 = Skater()
skater2.country = Country.objects.get(country_name='FRA')
skater2.dob = datetime.strptime('February 29, 2000', '%B %d, %Y')
skater2.gender = 'F'
skater2.height = 50
skater2.home_city = City.objects.get(city_name='Paris', country=Country.objects.get(country_name='FRA'))
skater2.training_city = City.objects.get(city_name='Milan', country=Country.objects.get(country_name='ITA'))
skater2.start_year = 2002
skater2.save()
skater2.coach = [Coach.objects.get(first_name='John', last_name='Doe')]
skater2.choreographer = [Coach.objects.get(first_name='Jane', last_name='Doe')]
skater2.save()

# Create name
print "Creating Skater Names"
SkaterName.objects.all().delete()
SkaterName(skater=skater1, first_name='Female', last_name='Skater', is_default_name=True).save()
SkaterName(skater=skater1, first_name='Ghost', last_name='Buster', is_default_name=False).save()
SkaterName(skater=skater2, first_name='Male', last_name='Skater', is_default_name=True).save()
SkaterName(skater=skater2, first_name='Fight', last_name='Club', is_default_name=False).save()


# Create Skater Metadata
print "Creating Skater Metadata"
SkaterMetadata.objects.all().delete()
SkaterMetadata(skater=skater1, metadata_key='SP', metadata_value='asdf').save()
SkaterMetadata(skater=skater1, metadata_key='FS', metadata_value='asdf').save()
SkaterMetadata(skater=skater2, metadata_key='SP', metadata_value='asdf').save()
SkaterMetadata(skater=skater2, metadata_key='FS', metadata_value='asdf').save()

# Create Skater Pairs
print "Creating Skater Pairs"
SkaterPair.objects.all().delete()
pair = SkaterPair(female_skater=skater2, male_skater=skater1)
pair.save()

# Create Competitors
print "Creating Competitors"
Competitor.objects.all().delete()
a = Competitor()
a.set_participants(pair).save()
competitor1 = Competitor()
competitor1.set_participants(skater1).save()
competitor2 = Competitor()
competitor2.set_participants(skater2).save()


# Create competition stuff
print "Creating Competitions"
Competition.objects.all().delete()
a = Competition(name='Four Continents Figure Skating Championships 2012')
a.start_date = datetime.strptime('February 7, 2012', '%B %d, %Y')
a.end_date = datetime.strptime('February 12, 2012', '%B %d, %Y')
a.country = Country.objects.get(country_name='USA')
a.isu_identifier = 'fc2012'
a.url = 'http://www.isuresults.com/results/fc2012/'
a.save()

# SkaterResult data
print "Creating SkaterResults"
SkaterResult.objects.all().delete()
sr = SkaterResult(competitor=competitor1,
                  competition=a)
sr.category = Category.objects.get(category='MEN')
sr.level = Level.objects.get(level='SR')
sr.save()

# Program data
print "Creating Programs"
Program.objects.all().delete()
a = Program(skater_result=sr)
a.segment = Segment.objects.get(segment='SP')
a.starting_number = 7
a.rank = 2
a.save()

# ResultIJS
print "Creating ResultIJS"
ResultIJS.objects.all().delete()
result1 = ResultIJS(program=a)
result1.deductions = 1
result1.save()

# ElementScore
print "Creating Element Score"
ElementScore.objects.all().delete()
elemscore1 = ElementScore(result=result1)
elemscore1.execution_order = 1
elemscore1.base_value = 3.3
elemscore1.grade_of_execution = 1.0
elemscore1.panel_score = 4.3
elemscore1.save()
elemscore2 = ElementScore(result=result1)
elemscore2.execution_order = 2
elemscore2.base_value = 7.3
elemscore2.grade_of_execution = -1.0
elemscore2.panel_score = 6.3
elemscore2.save()
elemscore3 = ElementScore(result=result1)
elemscore3.execution_order = 3
elemscore3.base_value = 3.3
elemscore3.grade_of_execution = 0.7
elemscore3.panel_score = 4
elemscore3.save()
elemscore4 = ElementScore(result=result1)
elemscore4.execution_order = 4
elemscore4.base_value = 5.3
elemscore4.grade_of_execution = 0.0
elemscore4.panel_score = 5.3
elemscore4.save()
elemscore5 = ElementScore(result=result1)
elemscore5.execution_order = 5
elemscore5.base_value = 6.0
elemscore5.grade_of_execution = -0.5
elemscore5.panel_score = 5.5
elemscore5.save()

# ElementJudge
print "Creating Element Judge"
ElementJudge.objects.all().delete()
elemjudge11 = ElementJudge(element_score = elemscore1)
elemjudge11.judge_grade_of_execution = 1.0
elemjudge12 = ElementJudge(element_score = elemscore1)
elemjudge12.judge_grade_of_execution = 0.0
elemjudge13 = ElementJudge(element_score = elemscore1)
elemjudge13.judge_grade_of_execution = 1.0
elemjudge14 = ElementJudge(element_score = elemscore1)
elemjudge14.judge_grade_of_execution = 2.0
elemjudge21 = ElementJudge(element_score = elemscore2)
elemjudge21.judge_grade_of_execution = -1.0
elemjudge22 = ElementJudge(element_score = elemscore2)
elemjudge22.judge_grade_of_execution = -0.0
elemjudge23 = ElementJudge(element_score = elemscore2)
elemjudge23.judge_grade_of_execution = -1.0
elemjudge24 = ElementJudge(element_score = elemscore2)
elemjudge24.judge_grade_of_execution = -2.0
elemjudge31 = ElementJudge(element_score = elemscore3)
elemjudge31.judge_grade_of_execution = 0.5
elemjudge32 = ElementJudge(element_score = elemscore3)
elemjudge32.judge_grade_of_execution = 0.0
elemjudge33 = ElementJudge(element_score = elemscore3)
elemjudge33.judge_grade_of_execution = 1.2
elemjudge34 = ElementJudge(element_score = elemscore3)
elemjudge34.judge_grade_of_execution = 2.0
elemjudge41 = ElementJudge(element_score = elemscore4)
elemjudge41.judge_grade_of_execution = 0.0
elemjudge42 = ElementJudge(element_score = elemscore4)
elemjudge42.judge_grade_of_execution = 0.0
elemjudge43 = ElementJudge(element_score = elemscore4)
elemjudge43.judge_grade_of_execution = -1.0
elemjudge44 = ElementJudge(element_score = elemscore4)
elemjudge44.judge_grade_of_execution = 1.0
elemjudge51 = ElementJudge(element_score = elemscore5)
elemjudge51.judge_grade_of_execution = -1.0
elemjudge52 = ElementJudge(element_score = elemscore5)
elemjudge52.judge_grade_of_execution = 0.0
elemjudge53 = ElementJudge(element_score = elemscore5)
elemjudge53.judge_grade_of_execution = 1.0
elemjudge54 = ElementJudge(element_score = elemscore5)
elemjudge54.judge_grade_of_execution = -2.0

# Element
print "Creating Element"
Element.objects.all().delete()
elem1 = Element(element_score=elemscore1)
elem1.base_element = BaseElement.objects.get(element_name='2A')
elem1.combination_order = 0
elem1.save()
# elem2 and elem3 are a combination
elem2 = Element(element_score=elemscore2)
elem2.base_element = BaseElement.objects.get(element_name='3Lz')
elem2.combination_order = 1
elem2.save()
elem3 = Element(element_score=elemscore2)
elem3.base_element = BaseElement.objects.get(element_name='2T')
elem3.combination_order = 2
elem3.save()
elem4 = Element(element_score=elemscore3)
elem4.base_element = BaseElement.objects.get(element_name='2A')
elem4.combination_order = 0
elem4.save()
elem5 = Element(element_score=elemscore4)
elem5.base_element = BaseElement.objects.get(element_name='3F')
elem5.combination_order = 0
elem5.save()
elem6 = Element(element_score=elemscore5)
elem6.base_element = BaseElement.objects.get(element_name='3Lz')
elem6.combination_order = 0
elem6.save()

# ProgramComponentScore
print "Creating ProgramComponentScore"
ProgramComponentScore.objects.all().delete()
pcs1 = ProgramComponentScore(result=result1)
pcs1.component = Component.objects.get(component='SS')
pcs1.factor = 1
pcs1.panel_score = 7.5
pcs1.save()
pcs2 = ProgramComponentScore(result=result1)
pcs2.component = Component.objects.get(component='TR')
pcs2.factor = 1
pcs2.panel_score = 6.5
pcs2.save()
pcs3 = ProgramComponentScore(result=result1)
pcs3.component = Component.objects.get(component='PE')
pcs3.factor = 1
pcs3.panel_score = 7.00
pcs3.save()
pcs4 = ProgramComponentScore(result=result1)
pcs4.component = Component.objects.get(component='CH')
pcs4.factor = 1
pcs4.panel_score = 7.5
pcs4.save()
pcs5 = ProgramComponentScore(result=result1)
pcs5.component = Component.objects.get(component='IN')
pcs5.factor = 1
pcs5.panel_score = 7.00
pcs5.save()

# ProgramComponentJudge
print "Creating ProgramComponentJudge"
ProgramComponentJudge.objects.all().delete()
pcj11 = ProgramComponentJudge(program_component_score = pcs1)
pcj11.judge_grade_of_execution = 7
pcj12 = ProgramComponentJudge(program_component_score = pcs1)
pcj12.judge_grade_of_execution = 8
pcj13 = ProgramComponentJudge(program_component_score = pcs1)
pcj13.judge_grade_of_execution = 7.25
pcj14 = ProgramComponentJudge(program_component_score = pcs1)
pcj14.judge_grade_of_execution = 7.75
pcj21 = ProgramComponentJudge(program_component_score = pcs2)
pcj21.judge_grade_of_execution = 6
pcj22 = ProgramComponentJudge(program_component_score = pcs2)
pcj22.judge_grade_of_execution = 7
pcj23 = ProgramComponentJudge(program_component_score = pcs2)
pcj23.judge_grade_of_execution = 6.25
pcj24 = ProgramComponentJudge(program_component_score = pcs2)
pcj24.judge_grade_of_execution = 6.75
pcj31 = ProgramComponentJudge(program_component_score = pcs3)
pcj31.judge_grade_of_execution = 7
pcj32 = ProgramComponentJudge(program_component_score = pcs3)
pcj32.judge_grade_of_execution = 7
pcj33 = ProgramComponentJudge(program_component_score = pcs3)
pcj33.judge_grade_of_execution = 7.25
pcj34 = ProgramComponentJudge(program_component_score = pcs3)
pcj34.judge_grade_of_execution = 6.75
pcj41 = ProgramComponentJudge(program_component_score = pcs4)
pcj41.judge_grade_of_execution = 7.5
pcj42 = ProgramComponentJudge(program_component_score = pcs4)
pcj42.judge_grade_of_execution = 7.5
pcj43 = ProgramComponentJudge(program_component_score = pcs4)
pcj43.judge_grade_of_execution = 7.75
pcj44 = ProgramComponentJudge(program_component_score = pcs4)
pcj44.judge_grade_of_execution = 7.25
pcj51 = ProgramComponentJudge(program_component_score = pcs5)
pcj51.judge_grade_of_execution = 7
pcj52 = ProgramComponentJudge(program_component_score = pcs5)
pcj52.judge_grade_of_execution = 7
pcj53 = ProgramComponentJudge(program_component_score = pcs5)
pcj53.judge_grade_of_execution = 6.25
pcj54 = ProgramComponentJudge(program_component_score = pcs5)
pcj54.judge_grade_of_execution = 7.25




























