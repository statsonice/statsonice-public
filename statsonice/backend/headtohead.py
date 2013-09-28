# head to head results
from statsonice.models import Skater, Competitor, Competition, SkaterResult
from stats import *
from includes import stats

# TODO: make compatible with 6.0 results or incomplete IJS results

class HeadToHead:

    def __init__(self, competitor1, competitor2):
        self.competitor1 = competitor1
        self.competitor2 = competitor2

    def get_head_to_head_results(self):
        hth_results = []
        s1_count = 0
        s2_count = 0
        skater1_skater_results = [sr for sr in SkaterResult.objects.filter(competitor = self.competitor1) if sr.qualifying.name == '' and len(sr.program_set.all()) is not 1 and sr.final_rank is not None]
        skater2_skater_results = [sr for sr in SkaterResult.objects.filter(competitor = self.competitor2) if sr.qualifying.name == '' and len(sr.program_set.all()) is not 1 and sr.final_rank is not None]
        skater1_competitions = [x.competition for x in skater1_skater_results]
        skater2_competitions = [x.competition for x in skater2_skater_results]
        competitions = set(skater1_competitions).intersection(set(skater2_competitions))
        for competition in competitions:
            for skater_result in skater1_skater_results:
                if skater_result.competition == competition:
                    skater1_res = skater_result
            for skater_result in skater2_skater_results:
                if skater_result.competition == competition:
                    skater2_res = skater_result
            if skater1_res.total_score == 0:
                continue
            if skater1_res.total_score > skater2_res.total_score:
                s1_count += 1
            else:
                s2_count += 1
            diff = abs(skater1_res.total_score - skater2_res.total_score)
            hth_results.append([competition,skater1_res,skater2_res,diff])

        hth_results.sort(key=lambda x:x[0].start_date)
        hth_results.reverse()
        
        self.hth_results = hth_results

        return s1_count, s2_count, hth_results

    def get_hth_graph_stats(self):

        s1_scores = []
        s2_scores = []
        date = []
        for comp, s1_res, s2_res, diff in self.hth_results:
            s1_scores.append(float(s1_res.total_score))
            s2_scores.append(float(s2_res.total_score))
            # TODO: str does not work with chart.js for some reason for the labels
            # need to keep precision for dates (e.g. 4.10 instead of 4.1)
            date.append(comp.start_date.year)

        s1_scores.reverse()
        s2_scores.reverse()

        date.reverse()

        return s1_scores, s2_scores, date


    def get_hth_table_stats(self):

        table_stats = {}

        # chance win
        # TODO: figure out how to calculate
        table_stats['chance_win'] = (50,50)

        # average win margin
        s1_count, s2_count = 0, 0
        s1_total, s2_total = 0, 0
        pt_gap = 0
        for comp, s1_res, s2_res, diff in self.hth_results:
            if s1_res.total_score > s2_res.total_score:
                s1_count += 1
                s1_total += s1_res.total_score - s2_res.total_score
                pt_gap += s1_res.total_score - s2_res.total_score
            else:
                s2_count += 1
                s2_total += s2_res.total_score - s1_res.total_score
                pt_gap -= s2_res.total_score - s1_res.total_score
        if s1_count > 0:
            s1_ave_win = round(s1_total/s1_count,2)
        else:
            s1_ave_win = '-'
        if s2_count > 0:
            s2_ave_win = round(s2_total/s2_count,2)
        else:
            s2_ave_win = '-'
            
        table_stats['ave_win'] = (s1_ave_win,s2_ave_win)

        # total point gap
        if pt_gap > 0:
            table_stats['pt_gap'] = (1,abs(pt_gap))
        else:
            table_stats['pt_gap'] = (2,abs(pt_gap))

        # recent trend
        s1_results = SkaterResult.objects.filter(competitor=self.competitor1).order_by('competition__start_date')
        s2_results = SkaterResult.objects.filter(competitor=self.competitor2).order_by('competition__start_date')
        s1_results = [sr for sr in s1_results if len(sr.program_set.all()) > 1 and sr.final_rank != None]
        s2_results = [sr for sr in s2_results if len(sr.program_set.all()) > 1 and sr.final_rank != None]

        s1_recent = [s.total_score for s in s1_results if s.total_score != 0][-3:]
        s1_trend,s1_intercept = stats.line_of_best_fit(s1_recent)

        s2_recent = [s.total_score for s in s2_results if s.total_score != 0][-3:]
        s2_trend,s2_intercept = stats.line_of_best_fit(s2_recent)
        
        table_stats['recent_trend'] = (s1_trend,s2_trend)

        # highest total score
        s1_max_score, s2_max_score = None,None
        if s1_results:
            s1_max_score = max([x.total_score for x in s1_results])
        if s2_results:
            s2_max_score = max([x.total_score for x in s2_results])

        table_stats['max_score'] = (s1_max_score,s2_max_score)

        # chance win
        s1_recent = [s.total_score for s in s1_results if s.total_score != 0][-3:]
        s2_recent = [s.total_score for s in s2_results if s.total_score != 0][-3:]
        if s1_recent and s2_recent:
            s1_chance_win, s2_chance_win = determine_win_probability(s1_recent,s2_recent)
            table_stats['chance_win'] = (s1_chance_win,s2_chance_win)
        
        return table_stats
            
