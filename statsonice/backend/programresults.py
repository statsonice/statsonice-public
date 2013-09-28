"""
These classes encapsulate logic surrounding skater results and program results
"""
from statsonice.models import SkaterResult
from includes import stats

class SkaterResults:
    def __init__(self, competition, competitor):
        self.competition = competition
        self.competitor = competitor
        self.skater_results = {}
        for skater_result in SkaterResult.objects.filter(competition=competition, competitor=competitor):
            self.skater_results[skater_result] = None

    def load_program_results(self):
        for skater_result in self.skater_results.keys():
            programs = skater_result.program_set.all()
            programs = [ProgramResults(program) for program in programs]
            [program.calculate_variables() for program in programs]
            self.skater_results[skater_result] = programs

class ProgramResults:
    # initialize class with a program object
    #
    def __init__(self, program):
        self.program = program
        self.element_scores = self.program.resultijs.elementscore_set.all().select_related()
        self.pc_scores = self.program.resultijs.programcomponentscore_set.all().select_related()
        self.goes_by_elementscore = {}
        self.goes = []
        self.programcomponentscores = []
        self.elementscores = []
        self.totals = []
        self.bonus = []
        self.MODIFIES_ONE = ['<','<<']
        self.MODIFIES_AFTER = ['SEQ','COMBO','TRANS','kpNNN','kpYNN','kpNYN','kpNNY','kpYYN','kpYNY','kpNYY','kpYYY']
        self.MODIFIES_ALL = ['*','!','e','x']


    # Calculate values for programs
    #
    def calculate_variables(self):
        self.goes_by_elementscore = self.elementscore_GOE()
        self.goes = ProgramResults.get_stats(self.GOE())
        self.programcomponentscores = self.compute_programcomponent_scores()
        self.elementscores = self.compute_element_scores()
        self.totals = self.get_grade_sums()
        self.bonus = self.second_half_bonus()


    # Given a list, returns tuple of median, average, and std dev
    #
    @staticmethod
    def get_stats(arr, remove_outlier_judges = False):
        if len(arr) == 0:
            return {'median': None, 'average':None, 'std_dev':None}
        if remove_outlier_judges:
            arr.sort()
            arr = arr[1:-1]
        median = round(stats.median(arr), 2)
        average = round(stats.average(arr), 2)
        std_dev = round(stats.std_dev(arr), 2)
        return {'median':median, 'average':average, 'std_dev':std_dev}



    #### Element score ####

    # get the grade of executions for an elementscore
    #
    def elementscore_GOE(self):
        goes_by_elementscore = {}
        for element_score in self.element_scores:
            goes_by_elementscore[element_score] = element_score.elementjudge_set.values_list('judge_grade_of_execution', flat=True)
        return goes_by_elementscore

    # get the grade of executions for a program
    #
    def GOE(self):
        return [goe for goes in self.goes_by_elementscore.values() for goe in goes]

    # sums of different grade values
    #
    def get_grade_sums(self):
        grades = self.element_scores.values_list('base_value','grade_of_execution')
        sums = {}
        sums['program_base_value_sum'] = sum([i[0] for i in grades])
        sums['program_goe_sum'] = sum([i[1] for i in grades])
        return sums

    # return element name given queryset of elements, with modifiers and all properly formatted
    #
    def get_el_name(self,elements):
        combo = []
        for element in elements:
            b_elem = element.base_element.element_name
            if element.modifiers:
                modifiers = element.modifiers.all()
                mods = modifiers.filter(modifier__in=self.MODIFIES_ONE).values_list('modifier', flat=True)
                mod_after = modifiers.filter(modifier__in=self.MODIFIES_AFTER).values_list('modifier', flat=True)
                mod_all = modifiers.filter(modifier__in=self.MODIFIES_ALL).exclude(modifier='x').values_list('modifier', flat=True)
                b_elem += ''.join(mods)
                combo.append(b_elem)
        combo_temp = '+'.join(combo)
        for mod in mod_after:
            combo_temp += '+'+mod
        for mod in mod_all:
            combo_temp += ' ('+mod+')'
        return combo_temp

    # returns element scores with median/average/stddev goe, base value, and element name
    #
    def compute_element_scores(self):
        for elementscore in self.element_scores:
            elements = elementscore.element_set.all()
            elementscore.element_name = self.get_el_name(elements)
            bv = str(elementscore.base_value)
            if elements[0].modifiers.filter(modifier='x').count() > 0:
                bv += ' x'
            elementscore.base_value_x = bv
            elementscore.judge_scores = self.goes_by_elementscore[elementscore]
            stats = ProgramResults.get_stats(elementscore.judge_scores)
            elementscore.median_goe = stats['median']
            elementscore.average_goe = stats['average']
            elementscore.std_dev_goe = stats['std_dev']
        return self.element_scores




    #### Program Component Score ####

    # get the grade of executions for an elementscore
    #
    @staticmethod
    def programcomponentscore_GOE(programcomponentscore):
        return programcomponentscore.programcomponentjudge_set.values_list('judge_grade_of_execution', flat=True)

    # get grade of execution for all program component scores
    #
    def PCS(self):
        goes = []
        for pc_score in self.pc_scores:
            goes += ProgramResults.programcomponentscore_GOE(pc_score)
        return goes

    # max PCS range for a PCS
    # Return range and the component name
    #
    def max_PCS_range(self):
        max_range = -1
        max_programcomponentscore = None
        for pc_score in self.pc_scores:
            goes = ProgramREsults.programcomponentscore_GOE(pc_score)
            temp_range = max(goes) - min(goes)
            if temp_range > max_range:
                max_range = temp_range
                max_programcomponentscore = pc_score
        return max_range, max_programcomponentscore.component.component

    # method to get total 2nd half bonus for program
    #
    def second_half_bonus(self):
        bonus = 0
        num = 0
        for elementscore in self.element_scores:
            element = elementscore.element_set.all()[0]
            if element.modifiers.filter(modifier='x').count() > 0:
                num += 1
                bonus += round(float(elementscore.base_value)*0.1/1.1, 2)
        return {'number_of_elements':num, 'bonus':bonus}

    # Return programcomponent score with goes and median/average/std_dev
    #
    def compute_programcomponent_scores(self):
        for programcomponentscore in self.pc_scores:
            programcomponentscore.goes = ProgramResults.programcomponentscore_GOE(programcomponentscore)
            stats = ProgramResults.get_stats(ProgramResults.programcomponentscore_GOE(programcomponentscore))
            programcomponentscore.median = stats['median']
            programcomponentscore.average = stats['average']
            programcomponentscore.std_dev = stats['std_dev']
        return self.pc_scores

