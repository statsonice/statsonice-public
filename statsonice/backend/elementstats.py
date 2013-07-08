# classes to compute element stats
import math

from statsonince.includes.stats import *

class ElementCompetitorStats:
    def __init__(self, element_name, competitor, element_scores=None):
        self.element_name = element_name

        self.competitor = competitor
        self.element_scores = element_scores
        if self.element_scores == None:
            self.element_scores = self.get_element_scores()

        self.average_score = 0
        self.std_dev_scores = 0
        self.average_score, self.std_dev_scores = self.compute_ave_std_dev_stats()

        self.num_attempts = len(self.element_scores)

        # ???
        self.single_dg = 0
        self.double_dg = 0

        # Number of elementscores where the average grade of execution falls
        # within a given bucket
        self.goe_ranges = {
            -3: 0, # between -3 and -2
            -2: 0,
            -1: 0,
             0: 0,
             1: 0,
             2: 0,
        }
        self.compute_modifier_goe_stats()

    def get_element_scores(self):
        return ElementScore.objects.filter(result__program__skater_result__competitor = self.competitor)

    def compute_ave_std_dev_stats(self):
        scores = list(self.element_scores.values_list('panel_score'))
        return (average(scores), std_dev(scores,average))

    def compute_modifier_goe_stats(self):
        for element_score in self.element_scores:
            # find downgrade statistics
            modifiers = list(element_score.element_set.values_list('modifiers', flat=True).distinct())
            if '<<' in modifiers:
                self.double_dg += 1
            elif '<' in modifiers:
                self.single_dg += 1

            # find goe statistics
            judge_goes = element_score.elementjudge_set.values_list('judge_grade_of_execution', flat=True).order_by('judge_grade_of_execution')
            judge_goes = list(judge_goes)[1:-1]
            average_goe = average(judge_goes)
            average_goe = int(math.floor(average_goe))
            self.goe_ranges[average_goe] += 1  # assumes that average_goe will be between -3 and 3

class ElementCategoryStats:
    # element_name is a string passed via the search feature (text box)
    # category is an object selected via drop down menu
    def __init__(self, element_name, category):
        self.MODIFIERS_TO_REMOVE = ['<','+COMBO']
        self.element_name = self.remove_modifiers(element_name)
        self.category = category

        self.element_scores = []
        self.competitor_scores = {} # dictionary with competitor object, [list of element scores]
        self.competitor_stats = []

        self.element_scores = self.get_element_scores()
        self.competitor_scores = self.get_competitor_scores()
        self.competitor_stats = [ElementCompetitorStats(self.element_name,competitor,element_scores) for competitor,element_scores in self.competitor_scores]

    def remove_modifiers(self, element_name):
        for modifier in self.MODIFIERS_TO_REMOVE:
            element_name = element_name.replace(modifier,'')
        return element_name

    def get_element_scores(self):
        element_scores = ElementScores.objects.filter(result__program__skater_result__category = self.category)
        element_scores = [es for es in element_scores if self.element_name in self.remove_modifiers(es.get_element_name())]
        return element_scores

    def get_competitor_scores(self):
        competitor_scores = {}
        for es in self.element_scores:
            competitor = es.result.program.skater_result.competitor
            if competitor not in competitor_scores:
                competitor_scores[competitor] = [es]
            else:
                competitor_scores[competitor].append(es)
        return competitor_scores
