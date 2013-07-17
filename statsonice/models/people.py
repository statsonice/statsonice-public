import urllib

from django.core.urlresolvers import reverse
from django.db import models
from django.http import Http404

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
    image = models.FileField(upload_to='/skater_images/', blank=True)
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
    def find_skater_by_url_name(skater_first_name, skater_last_name):
        skater_first_name = urllib.unquote(skater_first_name).replace('.', ' ')
        skater_last_name = urllib.unquote(skater_last_name).replace('.', ' ')
        try:
            return Skater.objects.distinct().get(skatername__first_name=skater_first_name, skatername__last_name=skater_last_name)
        except:
            raise Http404
    def get_default_skater_name(self):
        return self.skatername_set.get(is_default_name=True)
    def pairs(self):
        if self.gender == 'M':
            return SkaterPair.objects.filter(male_skater__id = self.id)
        else:
            return SkaterPair.objects.filter(female_skater__id = self.id)
    def competitor(self):
        return Competitor.find_competitor(self)
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Skater #%s)' % (self.id)
    def clean(self):
        PeopleValidator.validate_gender(self.gender)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Skater, self).save(*args, **kwargs)


class SkaterName(models.Model):
    skater = models.ForeignKey(Skater)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    is_default_name = models.BooleanField()

    def view_name(self):
        return self.first_name + ' ' + self.last_name
    def url_name(self):
        return (self.first_name.replace(' ','.'), self.last_name.replace(' ','.'))
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

    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(SkaterMetaData #%s for Skater #%s)' % (self.id, self.skater.id)
    def clean(self):
        EnumValidator.validate_enum(self.metadata_key, SkaterMetadata.METADATA_CHOICES)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(SkaterMetadata, self).save(*args, **kwargs)


class SkaterPair(models.Model):
    female_skater = models.ForeignKey(Skater, related_name = 'female_skater')
    male_skater = models.ForeignKey(Skater, related_name = 'male_skater')
    country = models.ForeignKey(Country, null=True, blank=True, related_name = 'team_country')
    coach = models.ManyToManyField(Coach, related_name='pair_coach')
    choreographer = models.ManyToManyField(Coach, related_name='pair_choreographer')
    start_year = models.PositiveIntegerField(null=True, blank=True)
    end_year = models.PositiveIntegerField(null=True, blank=True)

    @cached_function
    def view_name(self):
        return self.female_skater.view_name() + ' & ' + self.male_skater.view_name()
    def url_name(self):
        return (self.female_skater.url_name(), self.male_skater.url_name())
    @cached_function
    def url(self):
        female_skater_url_name = self.female_skater.get_default_skater_name().url_name()
        male_skater_url_name = self.male_skater.get_default_skater_name().url_name()
        return reverse('pair_profile', kwargs={\
            'first_skater_first_name':female_skater_url_name[0], \
            'first_skater_last_name':female_skater_url_name[1], \
            'second_skater_first_name':male_skater_url_name[0], \
            'second_skater_last_name':male_skater_url_name[1]\
        })
    @staticmethod
    def find_skater_pair_by_url_name(first_skater_first_name, first_skater_last_name, second_skater_first_name, second_skater_last_name):
        first_skater = Skater.find_skater_by_url_name(first_skater_first_name, first_skater_last_name)
        second_skater = Skater.find_skater_by_url_name(second_skater_first_name, second_skater_last_name)
        return SkaterPair.objects.get(female_skater=first_skater, male_skater=second_skater)
    def competitor(self):
        return Competitor.find_competitor(self)
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(SkaterPair of Skaters #%s and #%s)' % (self.female_skater.id, self.male_skater.id)
    def clean(self):
        PeopleValidator.validate_skaterpair(self.female_skater, self.male_skater)
        PeopleValidator.validate_skaterpair_unique(self)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(SkaterPair, self).save(*args, **kwargs)


class Competitor(models.Model):
    # Do not access these fields directly; use the functions below
    skater_pair = models.ForeignKey(SkaterPair, null=True, blank=True)
    skater = models.ForeignKey(Skater, null=True, blank=True)
    is_pair = models.BooleanField()

    # Set the skater or skaterpair for this Competitor
    def set_participants(self, participant):
        if type(participant) == SkaterPair:
            self.is_pair = True
            self.skater = None
            self.skater_pair = participant
        elif type(participant) == Skater:
            self.is_pair = False
            self.skater = None
            self.skater = participant
        else:
            raise TypeError("Cannot set Competitor for a "+str(participant))
        return self
    # Get the skater or skaterpair for this competitor
    def get_participants(self):
        if self.is_pair:
            return self.skater_pair
        else:
            return self.skater
    def url_name(self):
        return self.get_participants().url_name()
    @staticmethod
    def find_competitor(participant):
        try:
            if type(participant) == SkaterPair:
                return Competitor.objects.get(is_pair=True, skater_pair=participant)
            elif type(participant) == Skater:
                return Competitor.objects.get(is_pair=False, skater=participant)
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

