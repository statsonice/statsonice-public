import urllib
import datetime

from django.core.urlresolvers import reverse
from django.db import models

from statsonice.models.location import *
from statsonice.models.models_validator import PeopleValidator, EnumValidator
from includes.memcached import cached_function

class Coach(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)

    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Coach %s %s)' % (self.first_name, self.last_name)


class Skater(models.Model):
    country = models.ForeignKey(Country, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length = 1) # M or F
    height = models.PositiveIntegerField(null=True, blank=True)
    home_city = models.ForeignKey(City, related_name = 'home_city', null=True, blank=True)
    training_city = models.ForeignKey(City, related_name = 'training_city', null=True, blank=True)
    start_year = models.PositiveIntegerField(null=True, blank=True)
    coach = models.ManyToManyField(Coach, related_name='coach')
    choreographer = models.ManyToManyField(Coach, related_name='choreographer')

    @cached_function
    def view_name(self):
        first_name, last_name = self.skatername_set.filter(is_default_name=True).values_list('first_name', 'last_name')[0]
        return first_name + ' ' + last_name
    def url_name(self):
        return self.get_default_skater_name().url_name()
    @cached_function
    def url(self):
        skater_name = self.get_default_skater_name()
        return reverse('skater_profile', kwargs={\
            'skater_first_name':skater_name.url_name()[0], \
            'skater_last_name':skater_name.url_name()[1]\
        })
    @staticmethod
    def find_skater_by_url_name(first_name, last_name):
        skater = Skater.objects.distinct()
        first_name = SkaterName.get_search_string(first_name)
        if len(first_name) == 1:
            skater = skater.filter(skatername__first_name=first_name[0])
        else:
            for name in first_name:
                skater = skater.filter(skatername__first_name__contains=name)
        last_name = SkaterName.get_search_string(last_name)
        if len(last_name) == 1:
            skater = skater.get(skatername__last_name=last_name[0])
        else:
            for name in last_name[0:-1]:
                skater = skater.filter(skatername__last_name__contains=name)
            skater = skater.get(skatername__last_name__contains=last_name[-1])
        return skater
    def get_default_skater_name(self):
        return self.skatername_set.get(is_default_name=True)
    def teams(self):
        if self.gender == 'M':
            return SkaterTeam.objects.filter(male_skater__id = self.id)
        else:
            return SkaterTeam.objects.filter(female_skater__id = self.id)
    def age(self):
        if self.dob == None:
            return None
        today = datetime.date.today()
        try:
            birthday = self.dob.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = self.dob.replace(year=today.year, day=self.bob.day-1)
        if birthday > today:
            return today.year - self.dob.year - 1
        else:
            return today.year - self.dob.year
    def competitor(self):
        return Competitor.find_competitor(self)
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Skater #%s)' % (self.id)
    def clean(self):
        PeopleValidator.validate_gender(self)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Skater, self).save(*args, **kwargs)


class SkaterName(models.Model):
    skater = models.ForeignKey(Skater)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    is_default_name = models.BooleanField()

    URL_NAME_CHARACTERS_TO_REPLACE = [' ', '\'', ',']
    REPLACEMENT_CHAR = '.'

    def view_name(self):
        return self.first_name + ' ' + self.last_name
    @cached_function
    def url_name(self):
        first_name = self.first_name
        last_name = self.last_name
        for char in SkaterName.URL_NAME_CHARACTERS_TO_REPLACE:
            first_name = first_name.replace(char, SkaterName.REPLACEMENT_CHAR)
            last_name = last_name.replace(char, SkaterName.REPLACEMENT_CHAR)
        return (first_name, last_name)
    @staticmethod
    def get_search_string(url_name):
        url_name = urllib.unquote(url_name)
        url_name = url_name.split(SkaterName.REPLACEMENT_CHAR)
        url_name = [x for x in url_name if x != '']
        return url_name
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(SkaterName %s %s for Skater #%s)' % (self.first_name, self.last_name, self.skater.id)
    def clean(self):
        PeopleValidator.validate_name_unique(self)
        PeopleValidator.validate_name_periods(self)
        PeopleValidator.validate_skatername_default_name(self.skater)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(SkaterName, self).save(*args, **kwargs)


class SkaterMetadata(models.Model):
    METADATA_CHOICES = (
        ('', ''),
        ('END_YEAR', 'End Year'),
        ('PROFESSION', 'Profession'),
        ('HOBBIES', 'Hobbies'),
        ('SP', 'Short Program'),
        ('FS', 'Free Skating'),
    )
    skater = models.ForeignKey(Skater)
    metadata_key = models.CharField(max_length = 100, choices = METADATA_CHOICES, default = '')
    metadata_value = models.CharField(max_length = 100)
    start_date = models.DateField(null=True, blank=True, default=datetime.date(1,1,1))
    end_date = models.DateField(null=True, blank=True, default=datetime.date(3000,1,1))

    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(SkaterMetaData #%s for Skater #%s)' % (self.id, self.skater.id)
    def clean(self):
        EnumValidator.validate_enum(self.metadata_key, SkaterMetadata.METADATA_CHOICES)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(SkaterMetadata, self).save(*args, **kwargs)


class SkaterTeam(models.Model):
    female_skater = models.ForeignKey(Skater, related_name = 'female_skater')
    male_skater = models.ForeignKey(Skater, related_name = 'male_skater')
    country = models.ForeignKey(Country, null=True, blank=True, related_name = 'team_country')
    coach = models.ManyToManyField(Coach, related_name='team_coach')
    choreographer = models.ManyToManyField(Coach, related_name='team_choreographer')
    start_year = models.PositiveIntegerField(null=True, blank=True)
    end_year = models.PositiveIntegerField(null=True, blank=True)

    @cached_function
    def view_name(self):
        return self.female_skater.view_name() + ' & ' + self.male_skater.view_name()
    @cached_function
    def url_name(self):
        return (self.female_skater.url_name(), self.male_skater.url_name())
    @cached_function
    def url(self):
        female_skater_url_name = self.female_skater.get_default_skater_name().url_name()
        male_skater_url_name = self.male_skater.get_default_skater_name().url_name()
        return reverse('team_profile', kwargs={\
            'first_skater_first_name':female_skater_url_name[0], \
            'first_skater_last_name':female_skater_url_name[1], \
            'second_skater_first_name':male_skater_url_name[0], \
            'second_skater_last_name':male_skater_url_name[1]\
        })
    @cached_function
    def is_dance(self):
        try:
            skater_result = self.competitor().skaterresult_set.all()[0]
            category = skater_result.category.category
            if 'DANCE' in category:
                return True
            else:
                return False
        except:
            return None
    def competitor(self):
        return Competitor.find_competitor(self)
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(SkaterTeam of Skaters #%s and #%s)' % (self.female_skater.id, self.male_skater.id)
    def clean(self):
        PeopleValidator.validate_skaterteam(self.female_skater, self.male_skater)
        PeopleValidator.validate_skaterteam_unique(self)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(SkaterTeam, self).save(*args, **kwargs)


class Competitor(models.Model):
    skater_team = models.ForeignKey(SkaterTeam, null=True, blank=True, unique=True)
    skater = models.ForeignKey(Skater, null=True, blank=True, unique=True)
    is_team = models.BooleanField()

    # Set the skater or SkaterTeam for this Competitor
    def set_participants(self, participant):
        if type(participant) == SkaterTeam:
            self.is_team = True
            self.skater = None
            self.skater_team = participant
        elif type(participant) == Skater:
            self.is_team = False
            self.skater = None
            self.skater = participant
        else:
            raise TypeError("Cannot set Competitor for a "+str(participant))
        return self
    # Get the skater or SkaterTeam for this competitor
    def get_participants(self):
        if self.is_team:
            return self.skater_team
        else:
            return self.skater
    def url_name(self):
        return self.get_participants().url_name()
    @staticmethod
    def find_competitor(participant):
        try:
            if type(participant) == SkaterTeam:
                return Competitor.objects.get(is_team=True, skater_team=participant)
            elif type(participant) == Skater:
                return Competitor.objects.get(is_team=False, skater=participant)
        except:
            return None
        raise TypeError("Cannot find competitor for a "+str(participant))
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Competitor #%s %s)' % (self.id, self.get_participants())
    def clean(self):
        PeopleValidator.validate_competitor(self)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Competitor, self).save(*args, **kwargs)

