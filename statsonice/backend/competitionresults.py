
from statsonice.models import Program, Level, Segment, Category, SkaterResult

# This class counts flags for a category/level/segment in a competition
#
class CatLevSegStats:
    def __init__(self,competition,category,level,segment):
        self.competition = competition
        self.category = category
        self.level = level
        self.segment = segment
        self.programs = Program.objects.filter(skater_result__competition=self.competition,
                                               skater_result__category=self.category,
                                               skater_result__level=self.level,
                                               segment=self.segment)
        flags = list(self.programs.values_list('resultijs__elementscore__flag', flat=True))
        self.flag_ol = flags.count('OL')
        self.flag_nc = flags.count('NC')
        self.flag_pc = flags.count('PC')
        self.flag_to = flags.count('TO')
        self.num_elements = len(flags)

        if self.num_elements > 0:
            self.flag_ol = (self.flag_ol, round(self.flag_ol*100.0/self.num_elements,1))
            self.flag_nc = (self.flag_nc, round(self.flag_nc*100.0/self.num_elements,1))
            self.flag_pc = (self.flag_pc, round(self.flag_pc*100.0/self.num_elements,1))
            self.flag_to = (self.flag_to, round(self.flag_to*100.0/self.num_elements,1))
        else:
            self.flag_ol = (0, 0)
            self.flag_nc = (0, 0)
            self.flag_pc = (0, 0)
            self.flag_to = (0, 0)

class CountryCompStats:

    def __init__(self, competition, country):
        self.competition = competition
        self.country = country # country object, not country name

        self.gold_count, self.silver_count, self.bronze_count = self.get_medal_count()
        self.total_medal_count = self.get_total_medal_count()

    def get_medal_count(self):
        gold_count, silver_count, bronze_count = 0, 0, 0
        skater_results = SkaterResult.objects.filter(competition = self.competition, final_rank__in=[1,2,3])
        skater_results = skater_results.exclude(category__category__contains='PRE')
        for skater_result in skater_results:
            if not skater_result.competitor.get_participants().country:
                continue
            if skater_result.competitor.get_participants().country.country_name == self.country:
                if skater_result.final_rank == 1:
                    gold_count += 1
                elif skater_result.final_rank == 2:
                    silver_count += 1
                elif skater_result.final_rank == 3:
                    bronze_count += 1
        return gold_count, silver_count, bronze_count

    def get_total_medal_count(self):
        return self.gold_count + self.silver_count + self.bronze_count
        
class CompResults:
    # comp results class takes a competition object
    #
    def __init__(self, competition):
        self.LEVELS = Level.objects.values_list('level', flat=True).reverse()
        self.SEGMENTS = Segment.objects.values_list('segment', flat=True)
        self.CATEGORIES = Category.objects.values_list('category', flat=True)
        self.CATEGORIES = [category.replace(' ','_') for category in self.CATEGORIES]
        self.competition = competition
        self.catlevseg_stats = [CatLevSegStats(competition,category,level,segment) for category in Category.objects.all() for level in Level.objects.all() for segment in Segment.objects.all()]

        self.countries = self.get_countries()
        self.country_comp_stats = self.get_country_comp_stats()

    def get_countries(self):
        countries = set([])
        skater_results = SkaterResult.objects.filter(competition = self.competition).select_related('competitor')
        for skater_result in skater_results:
            country = skater_result.competitor.get_participants().country
            countries.add(country)
        countries.discard(None)
        return countries

    def get_country_comp_stats(self):
        country_comp_stats = [CountryCompStats(self.competition, country) for country in self.countries]
        country_comp_stats = sorted(country_comp_stats, key=lambda x: (-x.total_medal_count,-x.gold_count,-x.silver_count,-x.bronze_count))
        return country_comp_stats

    # Get the programs grouped by category and level
    # results[category][level] = skaterresult_set
    #
    def get_results_by_category_and_level(self):
        results = {}
        for category in self.CATEGORIES:
            results[category] = {}
            for level in self.LEVELS:
                results[category][level] = []
            for result in self.competition.skaterresult_set.filter(category=category.replace('_',' ')).select_related('level'):
                level = result.level.level
                results[category][level].append(result)
        return results

    # method to take sorted dictionary and return combined results
    #
    def get_combined_results(self, results_by_level):
        for level, skater_results in results_by_level.items():
            if len(skater_results) == 0:
                del results_by_level[level]
                continue
            # sort by overall score to determine rank
            skater_results.sort(key=lambda skater_result: -skater_result.total_score)

            # move withdrawals behind other skater results
            skater_results.sort(key=lambda r: r.withdrawal())
            results_by_level[level] = skater_results
        return results_by_level

    # method to return results for a segment
    # returns a list where each item is
    # for pairs: [participant, female_skater, male_skater, country, result, [program component scores]]
    # for singles: [skater, country, result, [program component scores]]
    #
    def get_segment_results(self,category,level,segment):
        programs = Program.objects.filter(skater_result__competition = self.competition,
                                          skater_result__category__category = category.replace('_',' '),
                                          skater_result__level__level = level,
                                          segment__segment = segment)
        results = [x.resultijs for x in programs]
        ordered_results = []
        for result in results:
            inner_temp = []
            participant = result.program.skater_result.competitor.get_participants()
            country = ''
            if participant.country != None:
                country = participant.country.country_name
            if result.program.skater_result.competitor.is_pair:
                female_skater = participant.female_skater
                male_skater = participant.male_skater
                inner_temp.extend([participant,female_skater,male_skater,country,result])
            else:
                skater = participant
                inner_temp.extend([skater,country,result])
            component_arr = []
            for pcs in result.programcomponentscore_set.all():
                component_arr.append(pcs)
            inner_temp.append(component_arr)
            ordered_results.append(inner_temp)

        ordered_results.sort(key=lambda x:x[-2].program.rank)
        return ordered_results
