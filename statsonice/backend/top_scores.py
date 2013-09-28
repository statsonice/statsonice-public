# this is a class for computing the top scores
from statsonice.models import SkaterResult, Program, ResultIJS
from datetime import datetime
from time import time

# TODO: maybe flatten so each skater only listed once?

class TopScores:

    def __init__(self,segment,category,start_year):

        start = time()
        self.start_year = start_year
        self.now_month, self.now_year = self.get_now()
        print 'got date: ', time() - start

        self.scores = self.get_top_scores(segment,category,start_year)
        print 'got scores: ', time() - start

    def get_now(self):
        now = datetime.now()
        now = now.date()
        return now.month, now.year

    def get_top_scores(self,segment,category,start_year):
        if self.start_year is 0:
            if segment == 'TOTAL':
                cat_srs = SkaterResult.objects.filter(category__category=category,
                                                      competition__identifier__startswith='isu').order_by('-total_score')[:100]
            else:
                cat_srs = ResultIJS.objects.filter(program__skater_result__category__category=category,
                                                   program__skater_result__competition__identifier__startswith='isu',
                                                   program__segment__segment=segment).order_by('-tss')[:100]
        elif self.start_year < self.now_year:
            startdate = datetime(self.start_year,5,1)
            enddate = datetime(self.start_year+1,5,1)
            if segment == 'TOTAL':
                cat_srs = SkaterResult.objects.filter(category__category=category,
                                                      competition__start_date__gt=startdate,
                                                      competition__start_date__lt=enddate,
                                                      competition__identifier__startswith='isu').order_by('-total_score')[:100]
            else:
                cat_srs = ResultIJS.objects.filter(program__skater_result__category__category=category,
                                                   program__skater_result__competition__start_date__gt=startdate,
                                                   program__skater_result__competition__start_date__lt=enddate,
                                                   program__skater_result__competition__identifier__startswith='isu',
                                                   program__segment__segment=segment).order_by('-tss')[:100]
        else:
            startdate = datetime(self.start_year,5,1)
            if segment == 'TOTAL':
                startdate = datetime(self.now_year,5,1)
                cat_srs = SkaterResult.objects.filter(category__category=category,
                                                      competition__start_date__gt=startdate,
                                                      total_score__gt = 0,
                                                      competition__identifier__startswith='isu').order_by('-total_score')
            else:
                cat_srs = ResultIJS.objects.filter(program__skater_result__category__category=category,
                                                   program__skater_result__competition__start_date__gt=startdate,
                                                   program__skater_result__competition__identifier__startswith='isu',
                                                   program__segment__segment=segment).order_by('-tss')
            if len(cat_srs) > 100:
                cat_srs = cat_srs[:100]

        return cat_srs





