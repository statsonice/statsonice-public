# classes to compute element stats
# TODO: modify classes to return data in format that the d3 file uses
from time import time
import math

from includes.stats import *
from statsonice.models import ElementScore, Element, BaseElement, Category, Skater, Competitor

# TODO: completely redo element competitor stats
'''
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
'''

class ElementStats:
    # TODO:
    #   - IMPROVE SPEED
    #   - method to return skater/team statistics
    #   - method to return </<</e/! statistics
    #   - add ability to search 4* for all quads
    #   - have way to click on a goe bar and get a readout of the skaters who did the element and a link to
    #     the protocols for the elements (make another div under the element_stats div to show detailed skater stats table)
    #     have standard django template table with data display or maybe a d3 table is easier...
    #   - add optional skater/team second argument? (e.g. 4S, Javier Fernandez)
    def __init__(self, element_name, skater_name, category_name):
        self.start = time()
        self.MODIFIERS_TO_REMOVE = ['<','+COMBO']
        self.nums = ['0','1','2','3','4','5','6','7','8','9']

        self.element_name = self.remove_modifiers(element_name)
        self.competitor = self.get_competitor(skater_name)
        self.category_name = category_name

        self.category = self.get_category() # returns category object
        self.element_names = self.get_element_names() # array of names split by '+'
        print 'element_names: ', self.element_names
        self.leveled = self.get_leveled_boolean() # array matching element_names to determine whether
                                                  # to check icontains or exact match for element name

        self.element_scores = self.get_element_scores()

        for es in self.element_scores:
            print es.get_element_name()

        # data to be displayed
        self.detailed_goe_stats = None # element score objects associated with goe bars
                                       # default is None but if < 200 element scores, calculate it
        self.goe_stats = self.get_goe_stats()
        self.years = self.get_years()
        self.flatten_goe_stats()
        self.level_stats = self.get_level_stats()
        # self.modifier_stats = self.get_modifier_stats() # NEEDS TO BE FIXED
        self.attempts_time_series = self.get_attempts_time_series()

        print 'elapsed time for element query: ', time() - self.start # keep in for a little while bc I'm concerned about slow queries

    def get_competitor(self, skater_name):
        try:
            skater_name = skater_name.split(' ')
            first_name = skater_name[0]
            last_name = ' '.join(skater_name[1:])

            skater = Skater.find_skater_by_url_name(first_name,last_name)
            competitor = Competitor.find_competitor(skater)
            return competitor
        except:
            return None

    def get_category(self):
        try:
            category = Category.objects.get(category=self.category_name.upper().strip())
        except:
            category = None
        return category

    def remove_modifiers(self, element_name):
        for modifier in self.MODIFIERS_TO_REMOVE:
            element_name = element_name.replace(modifier,'')
        return element_name

    def get_element_names(self):
        new_names = []
        if len(self.element_name) == 0:
            return []
        print self.element_name, type(self.element_name)
        if 'and' in self.element_name:
            self.element_name = self.element_name.split(' and ')
        if type(self.element_name) == str or type(self.element_name) == unicode:
            new_names.append(self.element_name)
        else:
            for elem_name in self.element_name:
                sub_new_names = []
                for el in elem_name.split('+'):
                    if el[-1] in self.nums:
                        el = el[:-1]
                    sub_new_names.append(el)
                new_names.append(sub_new_names)
        return new_names

    def get_leveled_boolean(self):
        l_boolean = []
        for element in self.element_names:
            for el_name in element:
                if str(el_name) + '1' in dict(BaseElement.BASE_ELEMENT_CHOICES):
                    l_boolean.append(1)
                else:
                    l_boolean.append(0)
        return l_boolean

    def get_element_scores(self):
        tot_element_scores = []
        if len(self.element_names) > 1:
            for element in self.element_names:
                ind = -1
                element_scores = None
                for element_name in element:
                    if len(element) == 1:
                        combo_order = 0
                    else:
                        ind += 1
                        combo_order = ind + 1
                    if element_name == '*':
                        continue
                    else:
                        if self.competitor:
                            if self.leveled[ind] == 1:
                                elements = list(Element.objects.filter(base_element__element_name__icontains=element_name,combination_order=combo_order,element_score__result__program__skater_result__competitor=self.competitor))
                            else:
                                elements = list(Element.objects.filter(base_element__element_name=element_name,combination_order=combo_order,element_score__result__program__skater_result__competitor=self.competitor))
                        else:
                            if self.leveled[ind] == 1:
                                elements = list(Element.objects.filter(base_element__element_name__icontains=element_name,combination_order=combo_order))
                            else:
                                elements = list(Element.objects.filter(base_element__element_name=element_name,combination_order=combo_order))
                        if self.category != None:
                            elements = [el for el in elements if el.element_score.result.program.skater_result.category == self.category]
                        e_scores = [el.element_score for el in elements]
                    if element_scores == None:
                        if e_scores == None:
                            continue
                        else:
                            element_scores = e_scores
                    else:
                        element_scores = set(e_scores).intersection(element_scores)

                # take intersection or difference with set of elements with combo order 3
                element_scores_3 = [es.element_score for es in Element.objects.filter(combination_order=3)]
                if len(element) == 2:
                    element_scores = set(element_scores).difference(element_scores_3)
                elif len(element) == 3:
                    element_scores = set(element_scores).intersection(element_scores_3)
                tot_element_scores.extend(list(element_scores))
        else:
            element_name = self.element_names[0]
            if self.competitor:
                if self.leveled[0] == 1:
                    elements = list(Element.objects.filter(base_element__element_name__icontains=element_name,combination_order=0,element_score__result__program__skater_result__competitor=self.competitor))
                else:
                    elements = list(Element.objects.filter(base_element__element_name=element_name,combination_order=0,element_score__result__program__skater_result__competitor=self.competitor))
            else:
                if self.leveled[0] == 1:
                    elements = list(Element.objects.filter(base_element__element_name__icontains=element_name,combination_order=0))
                else:
                    elements = list(Element.objects.filter(base_element__element_name=element_name,combination_order=0))
            if self.category != None:
                elements = [el for el in elements if el.element_score.result.program.skater_result.category == self.category]
            e_scores = [el.element_score for el in elements]
            element_scores = e_scores
            tot_element_scores = list(element_scores)

        #tot_element_scores = list(tot_element_scores)
        tot_element_scores.sort(key=lambda x:x.result.program.skater_result.competition.start_date)

        return tot_element_scores

    # methods to retrieve element data
    # TODO: find a better work around for bad data in calculate_goe
    def calculate_goe(self, element_judges):
        try:
            element_judges = list(element_judges)
            element_judges.sort(key=lambda x:x.judge_grade_of_execution)
            element_judges = element_judges[1:-1]
            element_goes = [x.judge_grade_of_execution for x in element_judges]
            tot = sum(element_goes)
            return float(tot)/len(element_goes)
        except:
            return -3 # find a better fix than this

    def get_goe_stats(self):
        goe_stats = {}
        if len(self.element_scores) < 300:
            detailed = True
        else:
            detailed = False
        goe_detailed_stats = {}
        for es in self.element_scores:
            year = es.result.program.skater_result.competition.start_date.year
            goe = self.calculate_goe(es.elementjudge_set.all())
            goe_range = math.floor(goe)
            if goe_range == 3:
                goe_range = 2
            if year in goe_stats:
                if detailed:
                    goe_detailed_stats[year][goe_range].append(es)
                goe_stats[year][goe_range] += 1
            else:
                goe_stats[year] = {
                    -3:0,
                    -2:0,
                    -1:0,
                    0:0,
                    1:0,
                    2:0
                    }
                goe_stats[year][goe_range] += 1
                if detailed:
                    goe_detailed_stats[year] = {
                        -3:[],
                        -2:[],
                        -1:[],
                        0:[],
                        1:[],
                        2:[]
                        }
                    goe_detailed_stats[year][goe_range].append(es)

        if detailed:
            self.detailed_goe_stats = goe_detailed_stats
        return goe_stats

    def get_years(self):
        years = []
        for key, value in self.goe_stats.items():
            if key not in years:
                years.append(key)
        years.sort()
        return years

    def flatten_goe_stats(self):
        flattened_stats = [(year, key, value) for year, dic in self.goe_stats.items() for key, value in dic.items()]
        flattened_stats.sort(key=lambda x:(x[0],x[1]))
        flattened_stats = [value for year, key, value in flattened_stats]
        self.goe_stats = flattened_stats

    def get_level_stats(self):
        # condition: solo element
        if len(self.element_names) > 1 or not self.leveled[0]:
            return None
        else:
            level_stats = {}
            levels = ['B','1','2','3','4']
            for es in self.element_scores:
                year = es.result.program.skater_result.competition.start_date.year
                level = es.element_set.all()[0].base_element.element_name[-1]
                if level not in levels:
                    continue
                if year in level_stats:
                    level_stats[year][level] += 1
                else:
                    level_stats[year] = {
                            '0':0,
                            'B':0,
                            '1':0,
                            '2':0,
                            '3':0,
                            '4':0
                        }
                    level_stats[year][level] += 1

        return level_stats

    # TODO: fix; many to many query here is wrong
    def get_modifier_stats(self):
        modifiers = ['<<','<','!','e','*']
        modifier_stats = {}
        for es in self.element_scores:
            year = es.result.program.skater_result.competition.start_date.year
            elems = es.element_set.all()
            mods = []
            for elem in elems:
                mods += elem.modifiers # NOT CORRECT
            for mod in mods:
                if mod in modifiers:
                    if year in modifier_stats:
                        modifier_stats[year][mod] += 1
                    else:
                        modifier_stats[year] = {
                                '<<':0,
                                '<':0,
                                '!':0,
                                'e':0,
                                '*':0
                            }
                        modifier_stats[year][mod] += 1

        return modifier_stats

    def get_attempts_time_series(self):
        num_years = len(self.years)
        attempts = []
        for i in range(num_years):
            year_attempts = sum(self.goe_stats[i*6:(i+1)*6])
            attempts.append(year_attempts)
        return attempts

    def get_competitor_stats(self):
        pass
