# this is a class for computing individual skater stats
from statsonice.models import Competitor, SkaterResult
from datetime import datetime

class ProfileResults:

    def __init__(self,skater):
        self.SEGMENTS = ['SP','FS','CD','OD','SD','FD']
        self.skater = skater
        self.competitor = Competitor.find_competitor(skater)
        self.skater_results = SkaterResult.objects.filter(competitor = self.competitor)
        self.programs = [program for skater_result in self.skater_results for program in skater_result.program_set.all()]

    # get personal records by segment and total score for skaters
    def get_best_isu_programs(self):
        programs_by_segment = {}
        best_programs = []
        for segment in self.SEGMENTS:
            programs_by_segment[segment] = []
            for program in self.programs:
                if program.segment.segment == segment and 'isu_' in program.skater_result.competition.identifier:
                    programs_by_segment[segment].append(program)
            if segment in programs_by_segment and programs_by_segment[segment] != []:
                programs_by_segment[segment].sort(key=lambda x:-x.resultijs.tss)
                result = programs_by_segment[segment][0].resultijs
                comp = result.program.skater_result.competition
                best_programs.append([comp, result])

        best_totals = []
        for sr in self.skater_results:
            if 'isu_' in sr.competition.identifier:
                if not sr.total_score:
                    sr.calculate_total_score()
                best_totals.append([sr,sr.total_score])

        best_total = 0
        if len(best_totals) > 0:
            best_totals.sort(key=lambda x:-x[1])
            best_total = best_totals[0][0]

        return best_programs, best_total

    # method to get isu results for a skater or team
    def get_isu_results_matrix(self):
        isu_results_matrix = []
        min_yr, max_yr = 2013, 0
        now = datetime.now()
        now = now.date()
        skater_results = list(self.skater_results)
        skater_results.sort(key=lambda x:x.competition.name)
        ordered_competitions = ['Olympic Games','World Championships','European Championships','Four Continents Championships','World Junior Championships','GPF','JGPF', 'GP ', 'JGP ']
        used_competitions = []
        for ordered_competition in ordered_competitions:
            for skater_result in skater_results:
                if skater_result.competition.start_date > now or 'PRE' in skater_result.category.category:
                    continue
                comp = skater_result.competition
                name = comp.name
                if ordered_competition in name:
                    # adjust min and max years for matrix
                    year = comp.start_date.year
                    if comp.identifier:
                        if 'isu_' in comp.identifier:
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
            if skater_result.competition.start_date > now or 'PRE' in skater_result.category.category:
                continue
            comp = skater_result.competition
            name = comp.name
            
            # adjust min and max years for matrix
            year = comp.start_date.year
            if comp.identifier:
                if 'isu_' in comp.identifier:
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
