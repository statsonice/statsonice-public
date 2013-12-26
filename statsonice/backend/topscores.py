"""
This is a class for computing the top scores within specified filters
"""
from statsonice.models import SkaterResult, ResultIJS
from datetime import datetime

# TODO: maybe flatten so each skater only listed once?

class TopScores:

    def __init__(self, segment, category, start_year):
        self.segment = segment
        self.category = category
        self.start_year = start_year
        self.now_year = datetime.now().year

        self.scores = self.get_top_scores()

    def get_top_scores(self):
        # Past year
        if self.start_year == 0:
            startdate = datetime(1900,1,1)
            enddate = datetime(2100,1,1)
        else:
            startdate = datetime(self.start_year,5,1)
            enddate = datetime(self.start_year+1,5,1)
        if self.segment == 'TOTAL':
            skater_results = SkaterResult.objects.filter(category__category=self.category,
                                                  competition__start_date__gt=startdate,
                                                  competition__start_date__lt=enddate,
                                                  total_score__gt = 0,
                                                  competition__identifier__startswith='isu').order_by('-total_score')[:100]
            results = []
            for skater_result in skater_results:
                result = {}
                result['score'] = skater_result.total_score
                result['url'] = skater_result.url()
                result['participant'] = skater_result.competitor.get_participants
                result['competition'] = skater_result.competition
                results.append(result)
        else:
            resultijss = ResultIJS.objects.filter(program__skater_result__category__category=self.category,
                                               program__skater_result__competition__start_date__gt=startdate,
                                               program__skater_result__competition__start_date__lt=enddate,
                                               program__skater_result__competition__identifier__startswith='isu',
                                               program__segment__segment=self.segment).order_by('-tss')[:100]
            results = []
            for resultijs in resultijss:
                result = {}
                result['score'] = resultijs.tss
                skater_result = resultijs.program.skater_result
                result['url'] = skater_result.url()
                result['participant'] = skater_result.competitor.get_participants
                result['competition'] = skater_result.competition
                results.append(result)
        return results

