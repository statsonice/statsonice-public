from decimal import *

from django.db import models
from django.core.urlresolvers import reverse

from statsonice.models.enums import *
from statsonice.models.location import *
from statsonice.models.people import *
from statsonice.models.other import *
from statsonice.models.models_validator import ModelValidator
from includes.stats import *
from includes.memcached import cached_function

# By default, every class automatically creates an auto-incrementing, unique id column
class CompetitionCutoff(models.Model):
    singles = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0.0)
    pairs = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0.0)
    dance = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0.0)
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(CompetitionCutoff)'

class Qualifying(models.Model):
    name = models.CharField(max_length = 20)
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Qualifying %s)' % (self.name)

class Competition(models.Model):
    name = models.CharField(max_length = 100)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    link = models.CharField(max_length = 500, null=True, blank=True)
    identifier = models.CharField(max_length = 100, null=True, blank=True)
    cutoff = models.ForeignKey(CompetitionCutoff, null=True, blank=True)

    @cached_function
    def view_name(self):
        return self.name + ' ('+str(self.end_date.year)+')'
    @cached_function
    def url(self):
        return reverse('competition_profile', kwargs={
                'competition_name': self.name.replace(' ','-'),
                'competition_year': self.start_date.year
        })
    def preview_url(self):
        return reverse('competition_preview_detailed', kwargs={
                'competition_name': self.name.replace(' ','-'),
                'competition_year': self.start_date.year
        })
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Competition %s)' % (self.name)
    def clean(self):
        ModelValidator.validate_competition_dates(self.start_date, self.end_date)
        ModelValidator.validate_competition_name(self.name)
        ModelValidator.validate_competition_unique(self)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Competition, self).save(*args, **kwargs)

class SkaterResult(models.Model):
    # total_score can be null for 6.0 competitions or IJS comps w/o scores
    competitor = models.ForeignKey(Competitor)
    competition = models.ForeignKey(Competition)
    category = models.ForeignKey(Category)
    level = models.ForeignKey(Level)
    qualifying = models.ForeignKey(Qualifying, null=True, blank=True)
    # Don't save into total_score, final_rank, withdrawal
    total_score = models.DecimalField(max_digits = 5, decimal_places = 2, null=True, blank=True, db_index=True)
    final_rank = models.PositiveIntegerField(null=True, blank=True)
    withdrawal = models.BooleanField(default=False)
    override_total_score = models.DecimalField(max_digits = 5, decimal_places = 2, null=True, blank=True)
    override_final_rank = models.PositiveIntegerField(null=True, blank=True)
    override_withdrawal = models.NullBooleanField()

    @cached_function
    def url(self):
        if self.competitor.is_team:
            return reverse('skater_result_profile_team', kwargs={\
                'competition_name':self.competition.name.replace(' ','-'), \
                'competition_year':self.competition.start_date.year, \
                'first_skater_first_name':self.competitor.url_name()[0][0], \
                'first_skater_last_name':self.competitor.url_name()[0][1], \
                'second_skater_first_name':self.competitor.url_name()[1][0], \
                'second_skater_last_name':self.competitor.url_name()[1][1]
            })
        else:
            return reverse('skater_result_profile_single', kwargs={\
                'competition_name':self.competition.name.replace(' ','-'), \
                'competition_year':self.competition.start_date.year, \
                'skater_first_name':self.competitor.url_name()[0], \
                'skater_last_name':self.competitor.url_name()[1]
            })
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(SkaterResult #%s for %s)' % (self.id, self.competition)
    def calculate_withdrawal(self):
        # Find how many programs there are supposed to be
        other_skater_results = self.competition.skaterresult_set.filter(category=self.category, qualifying=self.qualifying, level=self.level)
        expected_programs = max([skater_result.program_set.count() for skater_result in other_skater_results])
        if self.program_set.count() < expected_programs:
            self.withdrawal = True
        else:
            self.withdrawal = False
        return self.withdrawal
    def calculate_total_score(self):
        if self.override_total_score != None:
            self.total_score = self.override_total_score
        else:
            total = 0
            # rules for qual rounds at worlds change year by year
            # sometimes no qual rounds, other times do not count towards total score, etc.
            programs = self.program_set.all().select_related('resultijs')
            for program in programs:
                total += program.resultijs.tss * program.resultijs.multiplier
            self.total_score = total
        return self.total_score
    def calculate_final_rank(self):
        if self.override_final_rank:
            self.final_rank = self.override_final_rank
        else:
            skater_results = self.competition.skaterresult_set.filter(category = self.category, level = self.level, qualifying = self.qualifying)
            results = []
            for sr in skater_results:
                results.append([sr, sr.total_score])
            results.sort(key=lambda x:-x[1])
            comp_name = self.competition.name
            # TODO: This should not be here
            comp_names = ['World Championships', 'World Junior Championships', 'Four Continents Championships', 'European Championships']
            if comp_name in comp_names:
                # decide wd/fnr
                cutoff_num = 20
                category = self.category.category
                if category == 'MEN' or category == 'LADIES':
                    if self.competition.start_date.year != 2010 and 'World' not in comp_name:
                        cutoff_num = 24
                elif category == 'PAIRS':
                    if 'World' in comp_name:
                        cutoff_num = 16
                elif category == 'DANCE':
                    if 'World' not in comp_name:
                        cutoff_num = 24

                # set final_rank to none if the skater/team withdrew
                for sr, score in results:
                    full_set_programs = len(sr.program_set.all())
                    break
                skater_programs = len(self.program_set.all())
                if skater_programs < full_set_programs and skater_programs > 0:
                    prog = self.program_set.all()[0]
                    if prog.rank <= cutoff_num:
                        self.final_rank = None
                        return self.final_rank
            final_rank = results.index([self,self.calculate_total_score()])+1
            self.final_rank = final_rank
        return self.final_rank


class Program(models.Model):
    skater_result = models.ForeignKey(SkaterResult)
    segment = models.ForeignKey(Segment)
    starting_number = models.PositiveIntegerField()
    rank = models.PositiveIntegerField()
    # Most names will be None, except for named compulsary dances
    name = models.CharField(max_length = 100, default='')

    @cached_function
    def view_name(self):
        name = self.skater_result.competitor.get_participants().view_name()
        name += ' at '
        name += self.skater_result.competition.view_name()
        return name
    @cached_function
    def url_segment_summary(self):
        if self.skater_result.qualifying == None:
            return reverse('segment_summary', kwargs={\
                'competition_name':self.skater_result.competition.name.replace(' ','-'), \
                'competition_year':self.skater_result.competition.start_date.year, \
                'category': self.skater_result.category.category, \
                'qualifying': 'final', \
                'level': self.skater_result.level.level, \
                'segment': self.segment.segment, \
            })
        return reverse('segment_summary', kwargs={\
            'competition_name':self.skater_result.competition.name.replace(' ','-'), \
            'competition_year':self.skater_result.competition.start_date.year, \
            'category': self.skater_result.category.category, \
            'qualifying': self.skater_result.qualifying.name, \
            'level': self.skater_result.level.level, \
            'segment': self.segment.segment, \
        })

    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Program #%s for %s)' % (self.id, self.skater_result.competition)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Program, self).save(*args, **kwargs)


class ResultIJS(models.Model):
    program = models.OneToOneField(Program)
    deductions = models.PositiveIntegerField()
    # Don't save into tes, pcs, tss
    tes = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True, db_index=True)
    pcs = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True)
    tss = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True)
    override_tes = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True)
    override_pcs = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True)
    override_tss = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True)
    multiplier = models.DecimalField(max_digits = 5, decimal_places = 2, default = 1.0)

    def calculate_tes(self):
        if self.override_tes:
            self.tes = self.override_tes
        else:
            self.tes = sum(self.elementscore_set.values_list('panel_score', flat=True))
        return self.tes
    def calculate_pcs(self):
        if self.override_pcs:
            self.pcs = self.override_pcs
        else:
            total = Decimal(0)
            scores = self.programcomponentscore_set.values_list('factor', 'panel_score')
            for factor, panel_score in scores:
                if str(factor)[-1] == '5':
                    factor = Decimal(str(factor)+'001')
                    total += (self.multiplier*factor*panel_score).quantize(Decimal('0.01'))
                else:
                    total += (self.multiplier*factor*panel_score).quantize(Decimal('0.01'))
            self.pcs = total
        return self.pcs
    def calculate_tss(self):
        if self.override_tss:
            self.tss = self.override_tss
        else:
            self.tss = self.tes + self.pcs - self.deductions
        return self.tss
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(ResultIJS #%s for Competition %s)' % (self.id, self.program.skater_result.competition)

class ElementScore(models.Model):
    result = models.ForeignKey(ResultIJS)
    execution_order = models.PositiveIntegerField()
    base_value = models.DecimalField(max_digits = 10, decimal_places = 3)
    grade_of_execution = models.DecimalField(max_digits = 10, decimal_places = 3)
    panel_score = models.DecimalField(max_digits = 10, decimal_places = 3) # total element score
    flag = models.ForeignKey(Flag, null=True, blank=True)

    # grade of execution is icky to calculate from sub-elements, so we just scrape them
    # TODO
    def calculate_panel_score(self):
        pass
    def calculate_flag(self):
        goes = self.elementjudge_set.values_list('judge_grade_of_execution', flat=True)
        if len(goes) == 0:
            return
        goe_range = max(goes)-min(goes)
        goe_std = std_dev(goes)
        if goe_range >= 3 and goe_std <= 0.8:
            self.flag = Flag.objects.get(flag = 'OL')
        elif goe_range >= 2 and goe_std > 0.8:
            self.flag = Flag.objects.get(flag = 'NC')
        elif goe_range == 0 and goes[0] != -3:
            self.flag = Flag.objects.get(flag = 'PC')
        elif goe_range == 2 and goe_std <= 0.75:
            if (1 in goes and 3 in goes) or (-1 in goes and -3 in goes):
                self.flag = Flag.objects.get(flag = 'TO')
        else:
            self.flag = None
        return self.flag
    @cached_function
    def get_element_name(self):
        MODIFIES_ONE = ['<','<<']
        MODIFIES_AFTER = ['SEQ','COMBO','TRANS','kpNNN','kpYNN','kpNYN','kpNNY','kpYYN','kpYNY','kpNYY','kpYYY']
        elements = self.element_set.all()
        combo = []
        for element in elements:
            b_elem = element.base_element.element_name
            if element.modifiers:
                modifiers = element.modifiers.all()
                mods = modifiers.filter(modifier__in=MODIFIES_ONE).values_list('modifier', flat=True)
                mod_after = modifiers.filter(modifier__in=MODIFIES_AFTER).values_list('modifier', flat=True)
                b_elem += ''.join(mods)
                combo.append(b_elem)
        combo_temp = '+'.join(combo)
        for mod in mod_after:
            combo_temp += '+'+mod
        return combo_temp
            
    def clean(self):
        ModelValidator.validate_element_panel_score(self.base_value, self.grade_of_execution, self.panel_score)
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(ElementScore #%s)' % (self.id)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(ElementScore, self).save(*args, **kwargs)


class ElementJudge(models.Model):
    element_score = models.ForeignKey(ElementScore)
    judge = models.PositiveIntegerField()
    judge_grade_of_execution = models.IntegerField()

    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(ElementJudge #%s %s)' % (self.id, self.judge)
    def clean(self):
        ModelValidator.validate_element_judge_goe(self.judge_grade_of_execution)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(ElementJudge, self).save(*args, **kwargs)


# Provides additional details about the base element (e.g. modifiers)
# and allows the representation of combinations
class Element(models.Model):
    element_score = models.ForeignKey(ElementScore)
    base_element = models.ForeignKey(BaseElement)
    modifiers = models.ManyToManyField(Modifier)
    combination_order = models.IntegerField(null=True)

    def is_combination(self):
        if self.combination_order == 0:
            return False
        else:
            return True
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Element #%s)' % (self.id)


class ProgramComponentScore(models.Model):
    result = models.ForeignKey(ResultIJS)
    component = models.ForeignKey(Component)
    factor = models.DecimalField(max_digits = 10, decimal_places = 3)
    panel_score = models.DecimalField(max_digits = 10, decimal_places = 3)
    flag = models.ForeignKey(Flag, null=True, blank=True)

    def calculate_flag(self):
        # TODO write in flags conditions here
        pass

    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(ProgramComponentScore #%s)' % (self.id)
    def save(self, *args, **kwargs):
        super(ProgramComponentScore, self).save(*args, **kwargs)

class ProgramComponentJudge(models.Model):
    program_component_score = models.ForeignKey(ProgramComponentScore)
    judge = models.PositiveIntegerField()
    judge_grade_of_execution = models.DecimalField(max_digits = 10, decimal_places = 3)

    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(ProgramComponentJudge #%s %s)' % (self.id, self.judge)
    def clean(self):
        ModelValidator.validate_pc_judge_goe(self.judge_grade_of_execution)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(ProgramComponentJudge, self).save(*args, **kwargs)


