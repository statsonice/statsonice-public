# this is a class for computing the top scores
from statsonice.models import SkaterResult, Program
from datetime import datetime
from time import time

# TODO: maybe flatten so each skater only listed once?

class TopScores:

    def __init__(self,category,start_year):

        start = time()
        self.start_year = start_year
        self.now_month, self.now_year = self.get_now()
        print 'got date: ', time() - start

        self.scores = self.get_top_scores(category,start_year)
        print 'got scores: ', time() - start

    def get_now(self):
        now = datetime.now()
        now = now.date()
        return now.month, now.year

    def get_top_scores(self,category,start_year):
        print 'start year, self.now_year', start_year, self.now_year, start_year < self.now_year, type(start_year), type(self.now_year)

        if self.start_year is 0:
            cat_srs = SkaterResult.objects.filter(category__category=category,
                                                  competition__identifier__startswith='isu').order_by('-total_score')[:100]
        elif self.start_year < self.now_year:
            startdate = datetime(self.start_year,5,1)
            enddate = datetime(self.start_year+1,5,1)
            cat_srs = SkaterResult.objects.filter(category__category=category,
                                                  competition__start_date__gt=startdate,
                                                  competition__start_date__lt=enddate,
                                                  competition__identifier__startswith='isu').order_by('-total_score')[:100]

        else:
            startdate = datetime(self.now_year,5,1)
            cat_srs = SkaterResult.objects.filter(category__category=category,
                                                  competition__start_date__gt=startdate,
                                                  total_score__gt = 0,
                                                  competition__identifier__startswith='isu').order_by('-total_score')
            if len(cat_srs) > 100:
                cat_srs = cat_srs[:100]

        return cat_srs





