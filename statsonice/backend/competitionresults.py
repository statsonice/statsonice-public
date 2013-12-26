from statsonice.models import Competitor,Program, Level, Segment, Category, SkaterResult, ElementScore

# This class counts flags for a category/level/segment in a competition
#
class CatLevSegStats:
    def __init__(self,competition):
        programs = Program.objects.filter(skater_result__competition=competition)
        programs = programs.select_related('skater_result', 'resultijs')
        self.stats = []
        for program in programs:
            stat = {}
            stat['category'] = program.skater_result.category
            stat['level'] = program.skater_result.level
            stat['segment'] = program.segment
            flags = list(ElementScore.objects.filter(result = program.resultijs).values_list('flag', flat=True))
            stat['flag_ol'] = [flags.count('OL'),0]
            stat['flag_nc'] = [flags.count('NC'),0]
            stat['flag_pc'] = [flags.count('PC'),0]
            stat['flag_to'] = [flags.count('TO'),0]
            stat['num_elements'] = len(flags)
            self.stats.append(stat)
        for stat in self.stats:
            if stat['num_elements'] > 0:
                stat['flag_ol'][1] = round(stat['flag_ol'][0]*100.0/stat['num_elements'],1)
                stat['flag_nc'][1] = round(stat['flag_nc'][0]*100.0/stat['num_elements'],1)
                stat['flag_pc'][1] = round(stat['flag_pc'][0]*100.0/stat['num_elements'],1)
                stat['flag_to'][1] = round(stat['flag_to'][0]*100.0/stat['num_elements'],1)

class CountryCompStats:

    def __init__(self, competition, country):
        self.competition = competition
        self.country = country # country object, not country name

        self.gold_count, self.silver_count, self.bronze_count = self.get_medal_count()
        self.total_medal_count = self.get_total_medal_count()

    def get_medal_count(self):
        gold_count, silver_count, bronze_count = 0, 0, 0
        skater_results = SkaterResult.objects.filter(competition = self.competition, final_rank__in=[1,2,3])
	# TODO: fix following line bc it causes no medal stats for most comps (e.g. NHK Trophy 2010)
        skater_results = skater_results.exclude(qualifying__isnull=True)
        for skater_result in skater_results:
            if skater_result.competitor.is_team:
                if not skater_result.competitor.skater_team.country:
                    continue
                if skater_result.competitor.skater_team.country == self.country:
                    if skater_result.final_rank == 1:
                        gold_count += 1
                    elif skater_result.final_rank == 2:
                        silver_count += 1
                    elif skater_result.final_rank == 3:
                        bronze_count += 1
            else:
                if not skater_result.competitor.skater.country:
                    continue
                if skater_result.competitor.skater.country == self.country:
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
        self.CATEGORIES = Category.objects.values_list('category', flat=True)
        self.competition = competition

        #self.catlevseg_stats = CatLevSegStats(competition)
        #self.countries = self.get_countries()
        #self.country_comp_stats = self.get_country_comp_stats()

    def get_countries(self):
        competitors = Competitor.objects.filter(skaterresult__competition = self.competition).distinct()
        countries = []
        for competitor in competitors:
            if competitor.is_team:
                countries.append(competitor.skater_team.country)
            else:
                countries.append(competitor.skater.country)
        countries = set(countries)
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
                results[category][level] = {}
                results[category][level]['Final'] = []
            for result in self.competition.skaterresult_set.filter(category=category).select_related('level'):
                level = result.level.level
                qual = result.qualifying
                if qual:
                    if qual in results[category][level]:
                        results[category][level][qual].append(SortedSkaterResult(result))
                    else:
                        results[category][level][qual] = []
                        results[category][level][qual].append(SortedSkaterResult(result))
                else:
                    results[category][level]['Final'].append(SortedSkaterResult(result))
        return results

    # method to take sorted dictionary and return combined results
    #
    def get_combined_results(self, results_by_level):
        for level, qual_skater_results in results_by_level.items():
            for qual, skater_results in qual_skater_results.items():
                if len(skater_results) == 0:
                    del results_by_level[level][qual]
                    continue
                # sort by overall score to determine rank
                skater_results.sort(key=lambda sorted_skater_result: (sorted_skater_result.skater_result.final_rank,sorted_skater_result.skater_result.withdrawal))

                # move withdrawals behind other skater results
                skater_results.sort(key=lambda r: int(r.skater_result.withdrawal))
                results_by_level[level][qual] = skater_results
        return results_by_level


class SortedSkaterResult:
    def __init__(self,skater_result):
        self.skater_result = skater_result
        self.programs = list(self.skater_result.program_set.all())
        self.sort()

    def sort(self):
        program_heirarchy = {'SP':0,
                             'SD':1,
                             'CD':2,
                             'OD':3,
                             'FD':4,
                             'FS':5}
        self.programs.sort(key=lambda program:program_heirarchy[program.segment.segment])

class SegmentResults:
    def __init__(self, program):
        self.program = program
        self.competitor = self.program.skater_result.competitor
        if self.competitor.is_team:
            self.participant = self.competitor.skater_team
        else:
            self.participant = self.competitor.skater
        self.resultijs = self.program.resultijs
        self.pcs = self.resultijs.programcomponentscore_set.all()

    @staticmethod
    def get_results(programs):
        programs = programs.order_by('rank').select_related('skater_result__competitor', 'resultijs')
        return [SegmentResults(program) for program in programs]

