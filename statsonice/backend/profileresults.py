# this is a class for computing individual skater stats
from statsonice.models import Competitor, SkaterResult, Segment, Program, Qualifying
from datetime import date

class ProfileResults:

    def __init__(self,skater):
        self.SEGMENTS = [choice[0] for choice in Segment.SEGMENT_CHOICES][1:]
        self.ORDERED_COMPETITIONS = ['Olympic Games',
                                     'World Championships',
                                     'European Championships',
                                     'Four Continents Championships',
                                     'World Junior Championships',
                                     'Grand Prix Final',
                                     'Skate America',
                                     'Skate Canada',
                                     'Cup of China',
                                     'NHK Trophy',
                                     'Trophee Eric Bompard',
                                     'Cup of Russia',
                                     'Junior Grand Prix Final',
                                     'Junior Grand Prix ',
                                     'US Figure Skating Championships',
                                     ' Sectional',
                                     ' Regional',
                                     ' Championships']
        self.skater = skater
        self.competitor = Competitor.find_competitor(skater)
        self.skater_results = SkaterResult.objects.filter(competitor = self.competitor)

    # Get personal records by segment and total score for skaters
    # Returns a list of best competition/resultijs by segment and the best skater result
    #
    def get_best_isu_programs(self):
        # Get best resultijs and competition for each segment
        if self.competitor == None: return None, None
        best_programs = []
        programs = Program.objects.filter(skater_result__competitor__id = self.competitor.id)
        # TODO: This should use sql GROUP BY (I'm not sure of the django syntax right now)
        for segment in self.SEGMENTS:
            segment_programs = programs.filter(segment__segment = segment)
            segment_programs = segment_programs.filter(skater_result__competition__identifier__contains = 'isu_')
            segment_programs = segment_programs.order_by('resultijs__tss').reverse()
            if segment_programs.exists():
                best_program = segment_programs[0]
                best_programs.append([best_program.skater_result.competition, best_program.resultijs])

        best_programs.sort(key=lambda x:x[1].tss)

        # Get isu skater result with max total score
        skater_results = self.skater_results.filter(competition__identifier__contains = 'isu_')
        skater_results = skater_results.order_by('total_score').reverse()
        if len(skater_results) > 0:
            best_total = skater_results[0]
        else:
            best_total = None

        return best_programs, best_total

    # method to get isu results for a skater or team
    def get_isu_results_matrix(self):
        isu_results_matrix = []
        now = date.today()
        min_yr, max_yr = now.year, 0
        skater_results = self.skater_results.order_by('competition__name')
        skater_results = skater_results.filter(qualifying = Qualifying.objects.get(name=''),
                                               competition__end_date__lte = now,
                                               final_rank__gte = 1)

        used_competitions = []
        for ordered_competition in self.ORDERED_COMPETITIONS:
            for skater_result in skater_results:
                comp = skater_result.competition
                name = comp.name
                if ordered_competition in name:
                    if ordered_competition == 'Grand Prix Final' and 'Junior' in name:
                        continue
                    # adjust min and max years for matrix
                    year = comp.start_date.year
                    if year < min_yr:
                        min_yr = year
                    if year > max_yr:
                        max_yr = year

                    # add results to matrix
                    if name in used_competitions:
                        ind = used_competitions.index(name) # same as index for competition data in isu_results_matrix
                        res_dictionary = isu_results_matrix[ind][1]
                        if year not in res_dictionary:
                            res_dictionary[year] = (skater_result,comp)
                    else:
                        used_competitions.append(name)
                        res_dic = {}
                        res_dic[year] = (skater_result,comp)
                        isu_results_matrix.append([name,res_dic])

        for skater_result in skater_results:
            comp = skater_result.competition
            name = comp.name

            # adjust min and max years for matrix
            year = comp.start_date.year
            if year < min_yr:
                min_yr = year
            if year > max_yr:
                max_yr = year

            # add results to matrix
            if name in used_competitions:
                ind = used_competitions.index(name) # same as index for competition data in isu_results_matrix
                res_dictionary = isu_results_matrix[ind][1]
                if year not in res_dictionary:
                    res_dictionary[year] = (skater_result,comp)
            else:
                used_competitions.append(name)
                res_dic = {}
                res_dic[year] = (skater_result,comp)
                isu_results_matrix.append([name,res_dic])

        isu_years = range(min_yr,max_yr+1)
        return isu_results_matrix, isu_years
