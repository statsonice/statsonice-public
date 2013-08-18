from django.core.exceptions import ValidationError

class LocationValidator:
    @staticmethod
    def validate_country(country):
        if country.get_country_name() == None:
            raise ValidationError("Country "+str(country.country_name)+" is not a valid country")

class PeopleValidator:
    @staticmethod
    def validate_gender(value):
        possible_genders = ['M','F']
        if value not in possible_genders:
            raise ValidationError(str(value)+" is not a valid gender")

    @staticmethod
    def validate_name_unique(skater_name):
        skater_names = type(skater_name).objects.filter(first_name=skater_name.first_name, last_name=skater_name.last_name)
        if skater_name.pk:
            skater_names = skater_names.exclude(pk=skater_name.pk)
        if skater_names.count() > 0:
            raise ValidationError("More than one skater name with the same name")

    @staticmethod
    def validate_name_periods(skater_name):
        if '.' in skater_name.first_name or '.' in skater_name.last_name:
            raise ValidationError("Periods are not allowed in names")

    @staticmethod
    def validate_skatername_default_name(skater):
        skater_names = skater.skatername_set.all()
        found_default_name = False
        for skater_name in skater_names:
            if skater_name.is_default_name:
                if found_default_name:
                    raise ValidationError("Must have exactly one default/common name for skater "+str(skater))
                found_default_name = True

    @staticmethod
    def validate_skaterteam(female_skater, male_skater):
        if female_skater.gender != 'F':
            raise ValidationError("Female Skater with id "+str(female_skater.id)+"must be female")
        if male_skater.gender != 'M':
            raise ValidationError("Male Skater with id "+str(male_skater.id)+"must be male")

    @staticmethod
    def validate_skaterteam_unique(skater_team):
        skater_teams = type(skater_team).objects.filter(female_skater=skater_team.female_skater, male_skater=skater_team.male_skater)
        if skater_team.pk:
            skater_teams = skater_teams.exclude(pk=skater_team.pk)
        if skater_teams.count() > 0:
            raise ValidationError("More than one skater team with the same name")

    @staticmethod
    def validate_competitor(competitor):
        if competitor.is_team and competitor.skater != None:
            raise ValidationError("Cannot have team competitor and single skater")
        if not competitor.is_team and competitor.skater_team != None:
            raise ValidationError("Cannot have team competitor and single skater")
        participant = competitor.get_participants()
        if participant == None:
            raise ValidationError("Competitor does not refer to a valid Skater or SkaterTeam")
        competitors = type(competitor).objects.filter(skater=competitor.skater, skater_team=competitor.skater_team)
        if competitor.pk:
            competitors = competitors.exclude(pk=competitor.pk)
        if competitors.count() > 0:
            raise ValidationError("Competitor is not unique")


class ModelValidator:
    @staticmethod
    def validate_competition_dates(start_date, end_date):
        if start_date == None:
            raise ValidationError("Competition must have a year")
        if end_date != None:
            if start_date > end_date:
                raise ValidationError("Start Date is after End Date")

    @staticmethod
    def validate_competition_name(name):
        if '-' in name:
            raise ValidationError("Competition names must not contain '-'")

    @staticmethod
    def validate_competition_unique(competition):
        competitions = type(competition).objects.filter(name=competition.name, start_date__year = competition.start_date.year)
        if competition.pk:
            competitions = competitions.exclude(pk=competition.pk)
        if competitions.count() > 0:
            raise ValidationError("More than one competition with the same name and year")

    @staticmethod
    def validate_element_panel_score(base_value,GOE,panel_score):
        # TODO: Ensure base value + GOE == panel score; need to account for modifiers
        # do not need to account for modifiers if base value scraped directly from protocols
        if round(base_value + GOE,2) != round(panel_score,2):
            raise ValidationError("The base value and GOE do not add up to "+ str(panel_score))
        # Create a separate validator for GOE from judge scores? I'm leaning towards no.

    @staticmethod
    def validate_element_judge_goe(goe):
        if goe not in range(-3, 4):
            raise ValidationError("The element judge grade of execution must be within [-3,3]")

    @staticmethod
    def validate_pc_judge_goe(goe):
        if goe > 10 or goe < 0:
            raise ValidationError("The program component judge grade of execution must be within [0,10]")

    @staticmethod
    def validate_program(competitor, category):
        if category.category == 'MEN' or category.category == 'LADIES':
            if competitor.is_team:
                raise ValidationError("Programs for "+category.category+" cannot be for skater teams")
        if category.category == 'PAIRS' or category.category == 'DANCE':
            if not competitor.is_team:
                raise ValidationError("Programs for "+category.category+" cannot be for individual skaters")


class EnumValidator:
    @staticmethod
    def validate_enum(chosen, choices):
        for choice, human_readable in choices:
            if chosen == choice:
                return
        raise ValidationError(chosen+" is not a valid choice")

def validate_isu_identifier(isu_identifier):
    # TODO: Curran, this one's all you
    pass

def validate_number_of_judges():
    # TODO: Ensure that the same number of element/program_component scores are stored for each judge per result
    #       OR ensure that each element/program_component score per result has the same number of judges
    pass

def validate_combination(combination):
    # this assumes combination is stored as a string, not an array, e.g. '3T+2T+2Lo'
    if '<' in combination: combination.replace('<','')
    if not (is_jump_combination(combination) or is_jump_sequence(combination)):
        raise ValidationError(str(combination)+" is not a valid combination.")
    # TODO: Ensure that combination modifiers only modify valid elements
    #       e.g. * can only modify jumps (right?)

