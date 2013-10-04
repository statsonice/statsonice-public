"""
Classes to create a grand prix preview page
"""
from itertools import permutations
from datetime import date

from django.db.models import Count

from statsonice.models import Skater, Competitor, Competition, SkaterResult
from statsonice.backend.stats import *
from includes import stats

#-----------------------
# Competitor Stats Class
#-----------------------

# class to save details for a competitor so not continually querying them for matrices, tables, hths, and such
class CompetitorStats(object):
    def __init__(self,competitor):
        self.competitor = competitor
        if type(self.competitor.get_participants()) is Skater:
            if self.competitor.get_participants().dob:
                self.age = self.get_age()
            else:
                self.age = None
        self.skater_results = self.get_skater_results()
        self.competitions = self.get_competitions()
        self.scores = self.get_scores()
        self.recent_scores = self.get_recent_scores()
        self.highest_total_score = self.get_highest_total_score()
        self.slope, self.intercept = self.line_of_best_fit()
        self.next_score = self.get_next_score()
        self.consistency = self.get_consistency()

        # values dependent on which other competitors involved
        self.chance_win = None
        self.chance_medal = 1
        self.projected_placement = None
        self.hth_record = {}
        self.hth_probabilities = {}

    def get_age(self):
        born = self.competitor.get_participants().dob
        today = date.today()
        try:
            birthday = born.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, day=born.day-1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def get_skater_results(self):
        results = SkaterResult.objects.filter(competitor=self.competitor)
        results = results.exclude(final_rank=None, qualifying__isnull=True)
        results = results.annotate(programs=Count('program')).filter(programs__gt=1)
        results = results.order_by('competition__start_date')
        return results

    def get_competitions(self):
        competitions = [sr.competition for sr in self.skater_results]
        return competitions

    def get_scores(self):
        scores = list(self.skater_results.values_list('total_score', flat=True).filter(total_score__gt=0))
        return scores

    def get_recent_scores(self):
        return self.scores[-3:]

    def get_highest_total_score(self):
        highest_total_score = max(self.scores)
        return highest_total_score

    def line_of_best_fit(self):
        slope, intercept = stats.line_of_best_fit(self.recent_scores)
        slope, intercept = round(slope,1), round(intercept,1)
        return slope, intercept

    def get_next_score(self):
        next_score = stats.predict_next_value(self.recent_scores)
        return next_score

    def get_consistency(self):
        consistency = stats.estimate_consistency(self.recent_scores)
        return consistency

#--------------------------------
# Competition Preview Stats Class
#--------------------------------
class CompPreviewStats(object):
    def __init__(self,competition):
        self.competition = competition
        self.skater_results = SkaterResult.objects.filter(competition=competition)
        self.men = self.get_competitor_stats('MEN')
        self.ladies = self.get_competitor_stats('LADIES')
        self.pairs = self.get_competitor_stats('PAIRS')
        self.dance = self.get_competitor_stats('DANCE')
        print self.dance

    def get_competitor_stats(self, category):
        return [CompetitorStats(sr.competitor) for sr in self.skater_results.filter(category__category=category)]

    #-------------------------
    # HTH Matrix Methods
    #-------------------------

    # Find win/loss values for two competitors given their CompetitorStats
    #
    def get_hth(self, skater_stat1, skater_stat2):
        # intersecting competitions
        comps = [competition for competition in skater_stat1.competitions if competition in skater_stat2.competitions]

        # count head to head numbers
        res1 = skater_stat1.skater_results.filter(competition__in=comps).order_by('competition__id').values_list('total_score', flat=True)
        res2 = skater_stat2.skater_results.filter(competition__in=comps).order_by('competition__id').values_list('total_score', flat=True)

        i = 0
        s1_count, s2_count = 0, 0
        while i < len(res1):
            if res1[i] == 0 or res2[i] == 0:
                i += 1
                continue
            if res1[i] > res2[i]:
                s1_count += 1
            else:
                s2_count += 1
            i += 1

        skater_stat1.hth_record[skater_stat2] = s1_count
        skater_stat2.hth_record[skater_stat1] = s2_count

    # Calculate all the HTH raw values, probabilities, and win probabilities for every pair of competitors
    #
    def get_hth_records(self):
        for skater_stats in [self.men, self.ladies, self.pairs, self.dance]:
            normalization_total = 0.0
            for skater_stat1 in skater_stats:
                product = 1.0
                for skater_stat2 in skater_stats:
                    if skater_stat1 == skater_stat2:
                        continue
                    if skater_stat1 not in skater_stat2.hth_record:
                        self.get_hth(skater_stat1,skater_stat2)

                        prob1_win, prob2_win = determine_win_probability(skater_stat1.recent_scores,skater_stat2.recent_scores,len(skater_stats))
                        skater_stat1.hth_probabilities[skater_stat2.competitor] = prob1_win
                        skater_stat2.hth_probabilities[skater_stat1.competitor] = prob2_win

                    product *= skater_stat1.hth_probabilities[skater_stat2.competitor]/100.0
                skater_stat1.chance_win = product
                normalization_total += product
            for skater_stat1 in skater_stats:
                skater_stat1.chance_win /= normalization_total
                skater_stat1.chance_win = round(100.0*skater_stat1.chance_win,1)

    #-------------------------
    # Summary Stats Methods
    #-------------------------

    # Sort skaters by their projected score
    #
    def get_projected_placements(self):
        for category in [self.men,self.ladies,self.pairs,self.dance]:
            category.sort(key=lambda x:-x.next_score)
            i = 1
            for skater in category:
                skater.projected_placement = i
                i += 1

    # Compute the HTH probability for a permutation of skaters in a category
    #
    def compute_prob(self, permutation, category):
        product = 1.0
        i = 0
        while i < len(permutation):
            skater = permutation[i]
            for other_skater in permutation[i+1:]:
                product *= skater.hth_probabilities[other_skater.competitor]
            i += 1
        return product

    # Calculate probability of getting a medal
    #
    def calculate_medal_probability(self):
        for category in [self.men,self.ladies,self.pairs,self.dance]:
            if len(category) < 8:
                medal_threats = category
            else:
                non_threats = [skater for skater in category if skater.chance_win < 1]
                medal_threats = set(category).difference(non_threats)
            perms = set(permutations(medal_threats))
            normalization_constant = 0
            for perm in perms:
                prob = self.compute_prob(perm,category)
                normalization_constant += prob
                skaters = [s for s in medal_threats if s in perm[0:3]]
                for skater in skaters:
                    skater.chance_medal += prob
            for skater in medal_threats:
                if normalization_constant > 0:
                    skater.chance_medal /= normalization_constant
                    skater.chance_medal = round(100.0*skater.chance_medal,1)
        return

