"""
Score Cards classes/methods
"""

from statsonice.models import Program
from decimal import *

class ScoreCard:

    SINGLES_PAIRS_COMPONENTS = ['Skating Skills','Transitions','Performance/Execution','Choreography/Composition','Interpretation']
    DANCE_COMPONENTS = {'SD':['Skating Skills','Linking Footwork/Movement','Performance','Choreography','Interpretation/Timing'],
                        'FD':['Skating Skills','Transitions','Performance/Execution','Composition/Choreography','Interpretation/Timing']}

    def __init__(self,competitor,category,segment):
        self.competitor = competitor
        self.category = category # MEN, LADIES, etc.
        self.segment = segment # SD, FS, etc.

        self.program = self.get_program()

        if self.program is None:
            self.element_names = None
            self.pcs = None
        else:
            self.element_names = self.get_elements()
            self.pcs = self.get_pcs() # tuple: component score names, component scores

    def get_program(self):
        programs = Program.objects.filter(skater_result__competitor=self.competitor,
                                          segment__segment=self.segment,
                                          skater_result__category__category=self.category).order_by('-skater_result__competition__start_date')
        if len(programs) == 0:
            return None

        return programs[0]

    def get_elements(self):
        element_scores = self.program.resultijs.elementscore_set.all()
        element_names = []
        for element_score in element_scores:
            bonus = False
            print element_score
            if str(element_score.base_value)[-1] != '0':
                bonus = True
            name = element_score.get_element_name()
            element_names.append((name,bonus))

        return element_names

    def get_pcs(self):
        if self.category == 'DANCE':
            component_names = self.DANCE_COMPONENTS[self.segment]
        else:
            component_names = self.SINGLES_PAIRS_COMPONENTS
        component_scores = [pc.panel_score for pc in self.program.resultijs.programcomponentscore_set.all()]

        pcs = []
        for component_name in component_names:
            ind = component_names.index(component_name)
            pcs.append((component_name,component_scores[ind]))
        return pcs

class ScoreCardOutput:

    SEGMENT_MULTIPLIER = {'MEN': {'SP': { 'Skating Skills':1.00,
                                          'Transitions':1.00,
                                          'Performance/Execution':1.00,
                                          'Choreography/Composition':1.00,
                                          'Interpretation':1.00
                                         },
                                  'FS':{ 'Skating Skills':2.00,
                                          'Transitions':2.00,
                                          'Performance/Execution':2.00,
                                          'Choreography/Composition':2.00,
                                          'Interpretation':2.00
                                         }
                          },
                          'LADIES': {'SP': { 'Skating Skills':0.80,
                                          'Transitions':0.80,
                                          'Performance/Execution':0.80,
                                          'Choreography/Composition':0.80,
                                          'Interpretation':0.80
                                         },
                                      'FS':{ 'Skating Skills':1.60,
                                          'Transitions':1.60,
                                          'Performance/Execution':1.60,
                                          'Choreography/Composition':1.60,
                                          'Interpretation':1.60
                                         }
                          },
                          'PAIRS': {'SP': { 'Skating Skills':0.80,
                                          'Transitions':0.80,
                                          'Performance/Execution':0.80,
                                          'Choreography/Composition':0.80,
                                          'Interpretation':0.80
                                         },
                                      'FS':{ 'Skating Skills':1.60,
                                          'Transitions':1.60,
                                          'Performance/Execution':1.60,
                                          'Choreography/Composition':1.60,
                                          'Interpretation':1.60
                                         }
                          },
                          'DANCE': {'SD': {'Skating Skills':0.80,
                                       'Linking Footwork/Movement':0.70,
                                       'Performance':0.70,
                                       'Choreography':0.80,
                                       'Interpretation/Timing':1.00
                                        },
                                    'FD': {'Skating Skills':1.25,
                                       'Transitions':1.75,
                                       'Performance/Execution':1.00,
                                       'Composition/Choreography':1.00,
                                       'Interpretation/Timing':1.00
                                    }
                                }
                          }


    # loaded with singles and pairs elements so fars
    ELEMENT_BV_GOEPLUS_GOEMINUS = {'5TLi1': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '4.5'}, 'PiF': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '2.2'}, '5SLiB': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '4.0'}, '4ATw4': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '9.0'}, '1ATwB': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '0.9'}, '5SLi4': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '6.0'}, '4ATw1': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '7.5'}, 'PCoSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.5'}, 'FoDs2': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '3.5'}, 'FCoSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, '3LiB': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '2.0'}, 'FCoSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.5'}, 'FCoSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, '4ATw3': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '8.5'}, 'FCoSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.0'}, '5SLi3': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '5.5'}, '1TwB': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '0.9'}, '5ALiB': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '4.5'}, 'USp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.2'}, 'USp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.5'}, 'USp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.9'}, 'USp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.4'}, 'FiDs1': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '2.8'}, '2Li3': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '2.4'}, 'FiDs3': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '3.2'}, '4LzTh': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '9.0'}, 'FoDs1': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '3.0'}, 'FiDs4': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '3.5'}, '2LoTh': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '2.8'}, 'BiDsB': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '2.6'}, 'CSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.1'}, '5RLiB': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.0'}, '2T': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '1.3'}, 'FCCoSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, '1Li3': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.5'}, '2S': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '1.3'}, '4TTh': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '8.0'}, '5RLi4': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '7.0'}, 'CSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.6'}, 'CSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.8'}, 'CSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.3'}, '5RLi3': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '6.5'}, 'CSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.4'}, '1Tw2': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '1.3'}, '1Tw3': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '1.5'}, '2F': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.8'}, '1Tw1': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '1.1'}, '2ATh': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '4.0'}, '2A': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '3.3'}, '1Tw4': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '1.7'}, 'USpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.0'}, '3TwB': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '4.6'}, '2ATw2': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '3.5'}, '2LiB': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.1'}, '1ATw4': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '1.7'}, 'FCoSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.5'}, 'BoDs4': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '4.5'}, '2ATw4': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '4.1'}, '4LoTh': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '8.5'}, '4ATwB': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '7.0'}, 'StSqB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.5'}, 'CSSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.9'}, 'CSSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.3'}, 'CSSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.6'}, 'CSSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.0'}, '3Lz': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '6.0'}, '3S': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '4.2'}, 'FCSSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.0'}, '2FTh': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '3.0'}, 'FCSSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.9'}, 'PSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, 'FCSSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.6'}, '3T': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '4.1'}, 'FUSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.4'}, 'FUSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, 'FUSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, '3Lo': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.1'}, '2Lz': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '2.1'}, 'FUSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.9'}, '5BLi4': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '6.5'}, '3A': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '8.5'}, '5BLi1': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.0'}, '3F': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.3'}, '5BLi3': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '6.0'}, '5BLi2': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.5'}, 'FCCoSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.5'}, '1ATw2': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '1.3'}, 'CUSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.5'}, 'FCLSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, '2STh': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '2.5'}, 'FCCoSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.5'}, '4ATw2': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '8.0'}, '3TTh': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '4.5'}, 'LSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.2'}, '5ALi1': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.0'}, '3LoTh': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.0'}, 'FCCoSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.0'}, '2ATwB': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '3.0'}, '1ATw3': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '1.5'}, '4STh': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '8.0'}, 'LSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.4'}, 'LSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.9'}, 'LSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.5'}, '3Li1': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '2.5'}, '5SLi1': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '4.5'}, 'LSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.7'}, '1LoTh': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.4'}, '4LiB': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '2.0'}, 'CUSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, 'CUSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.4'}, 'FCLSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.4'}, 'CUSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, 'FCLSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.2'}, 'CUSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.9'}, 'FUSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.5'}, 'ChSq': {'goe_plus': '0.7', 'goe_minus': '0.5', 'base_value': '2.0'}, '1LiB': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.0'}, 'FCCoSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, '5BLiB': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '4.5'}, 'StSq2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.6'}, 'StSq3': {'goe_plus': '0.5', 'goe_minus': '0.7', 'base_value': '3.3'}, 'CSSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.6'}, 'StSq1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.8'}, 'StSq4': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '3.9'}, 'PSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.5'}, '3LzTh': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.5'}, 'PSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.5'}, 'PSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, 'FCSSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.6'}, '1ATw1': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '1.1'}, 'FCSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.2'}, '1S': {'goe_plus': '0.2', 'goe_minus': '0.1', 'base_value': '0.4'}, 'FCSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.9'}, '1T': {'goe_plus': '0.2', 'goe_minus': '0.1', 'base_value': '0.4'}, 'FCSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.8'}, 'FCSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.3'}, '4Lz': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '13.6'}, '4TwB': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '6.6'}, '1A': {'goe_plus': '0.2', 'goe_minus': '0.2', 'base_value': '1.1'}, 'CCoSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.5'}, '1F': {'goe_plus': '0.2', 'goe_minus': '0.1', 'base_value': '0.5'}, 'CLSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, 'BiDs2': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '3.0'}, 'CLSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.9'}, 'CLSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.4'}, '4Lo': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '12.0'}, 'CLSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.2'}, 'PCoSp4': {'goe_plus': '0.5', 'goe_minus': '0.6', 'base_value': '4.5'}, '3STh': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '4.5'}, 'FCLSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.9'}, '3Tw2': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.4'}, 'BoDs3': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '4.0'}, '3Tw3': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.8'}, '1FTh': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.4'}, 'BoDs2': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '3.5'}, 'CCSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, 'CCSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.3'}, 'CCSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.8'}, 'CCSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.2'}, 'PCoSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.0'}, '4A': {'goe_plus': '1.2', 'goe_minus': '1.2', 'base_value': '15.0'}, '5TLi3': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '5.5'}, '5TLi2': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '5.0'}, 'CoSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.5'}, 'FCLSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, 'CCSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, '2Li2': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.7'}, '2Li4': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '3.0'}, 'CoSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.0'}, 'CoSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, 'CoSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, 'CoSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.5'}, 'FoDsB': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '2.8'}, '2Tw3': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '3.5'}, 'PCoSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.5'}, 'FCSSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.3'}, '2Tw2': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '3.2'}, '1STh': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.1'}, '5TLi4': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '6.0'}, '1Lz': {'goe_plus': '0.2', 'goe_minus': '0.1', 'base_value': '0.6'}, '2Tw1': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '3.0'}, '1Li1': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.1'}, '1Li2': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.3'}, 'CLSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, '1Li4': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.7'}, '5ALi4': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '6.5'}, '1Lo': {'goe_plus': '0.2', 'goe_minus': '0.1', 'base_value': '0.5'}, '3Li4': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '4.0'}, '3Li2': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '3.0'}, '3Li3': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '3.5'}, '5ALi2': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.5'}, 'FCSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.6'}, '4Tw1': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '7.1'}, '4Tw3': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '8.1'}, '4Tw2': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '7.6'}, '4Tw4': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '8.6'}, '3Tw4': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '6.2'}, '2Li1': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.3'}, '3ATh': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '7.5'}, '1ATh': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '2.2'}, '3Tw1': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.0'}, 'FLSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, 'FSSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, '3ATw3': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '6.1'}, 'FCUSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.9'}, 'FCUSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.4'}, 'FCUSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, 'FCUSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, 'FiDsB': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '2.6'}, 'CCoSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, '2TwB': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '2.7'}, '3FTh': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.5'}, '3ATw4': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '6.6'}, 'FCCSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.2'}, 'FCCSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, '3ATw1': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.3'}, 'FCCSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.8'}, 'FCCSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.3'}, 'SSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.1'}, 'BoDsB': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '2.8'}, '1TTh': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.1'}, 'FoDs3': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '4.0'}, '5ALi3': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '6.0'}, '3ATw2': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.7'}, 'BiDs4': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '3.5'}, '2ATw1': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '3.3'}, '2ATw3': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '3.8'}, '4Li4': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '4.0'}, '4Li3': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '3.5'}, '4Li2': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '3.0'}, '4Li1': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '2.5'}, '2LzTh': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '3.0'}, 'BiDs1': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '2.8'}, 'FLSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.4'}, '5RLi1': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.5'}, '4T': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '10.3'}, 'FSSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.3'}, '4S': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '10.5'}, '5TLiB': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '4.0'}, '4FTh': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '9.0'}, '1LzTh': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.4'}, '4F': {'goe_plus': '1.0', 'goe_minus': '1.0', 'base_value': '12.3'}, 'SSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.5'}, '5RLi2': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '6.0'}, 'SSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.6'}, 'SSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.1'}, 'BoDs1': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '3.0'}, 'SSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.3'}, '2TTh': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '2.5'}, '2Lo': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '1.8'}, '2Tw4': {'goe_plus': '0.3', 'goe_minus': '0.3', 'base_value': '3.8'}, 'CCoSp2': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.5'}, 'CCoSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.0'}, '5SLi2': {'goe_plus': '0.5', 'goe_minus': '0.5', 'base_value': '5.0'}, 'CCoSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, 'PSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.0'}, '3ATwB': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '5.0'}, 'FCCSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.7'}, 'FLSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.2'}, 'FSSp4': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '3.0'}, 'FSSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, 'FLSp1': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.0'}, 'FSSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.6'}, 'FLSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '2.9'}, 'PCoSp3': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '4.0'}, 'BiDs3': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '3.2'}, 'FCUSpB': {'goe_plus': '0.5', 'goe_minus': '0.3', 'base_value': '1.5'}, 'FoDs4': {'goe_plus': '0.7', 'goe_minus': '0.7', 'base_value': '4.5'}}

    def __init__(self,competitor,category,segment,element_names_goes,pcs):
        # TODO: add second half info

        self.competitor = competitor
        self.category
        self.segment = segment

        # Dictionary of element names and goes - element_names_goes['4T'] = -2
        self.element_names_goes = element_names_goes

        # Dictionary of component names and scores - pcs['Skating Skills'] = 5.5
        self.pcs = pcs

        # ScoreCardElement objects - element scores
        self.element_scores = self.get_element_scores()

        # String - total pcs score
        self.pcs_total = self.get_pcs_total()

    # Method to attach base values to elements
    def get_element_scores(self):

        element_scores = []
        execution_order = 0
        for element_name, goe in self.element_names_goes:

            execution_order += 1
            elements = element_name.split('+')
            base_value = 0
            goe_factor = 0
            sequence = False

            for element in elements:
                under_rotated = False

                # if * in element name, it gets no points
                if '*' in element:
                    goe = 0
                    goe_factor = 0
                    base_value = 0

                # if << in element name
                if '<<' in element:
                    element = element.replace('<<','')
                    digit = int(element[0]) - 1
                    element = str(digit)+element[1:]

                # elif < in element name
                elif '<' in element:
                    element = element.replace('<','')
                    under_rotated = True

                # if SEQ in element name
                if 'SEQ' in element:
                    element = element.replace('SEQ','')
                    sequence = True
                    if len(element) == 0:
                        continue

                # skip if element not in the dictionary
                if element_name not in ELEMENT_BV_GOEPLUS_GOEMINUS:
                    print 'element name not in dictionary: ', element_name
                    continue

                # get element base value, accounting for under rotations
                element_base_value = ELEMENT_BV_GOEPLUS_GOEMINUS[element_name]['base_value']
                if under_rotated:
                    element_base_value = round(element_base_value*0.7,1)

                base_value += element_base_value

                # find goe factor: number by which to multiply judge goe to get goe point value
                if goe > 0:
                    goe_plus = ELEMENT_BV_GOEPLUS_GOEMINUS[element_name]['goe_plus']
                    if goe_plus > goe_factor:
                        goe_factor = goe_plus
                elif goe < 0:
                    goe_minus = ELEMENT_BV_GOEPLUS_GOEMINUS[element_name]['goe_minus']
                    if goe_minus > goe_factor:
                        goe_factor = goe_minus

            goe_score = round(goe_factor*goe,2)
            total_element_score = str(Decimal(base_value + goe_score))
            element_scores.append(ScoreCardElement(execution_order,element_name,goe,goe_score,total_element_score))

        return element_scores

    def get_pcs_total(self):
        pcs_total = 0
        for name, pc in pcs:
            pcs_total += round(self.SEGMENT_MULTIPLIER[self.category][self.segment][name]*pc,2)
        return pcs_total

class ScoreCardElement:

    def __init__(self,execution_order,element_name,goe,goe_score,total_element_score):
        self.execution_order = execution_order
        self.element_name = element_name
        self.goe = goe
        self.goe_score = goe_score
        self.total_element_score = total_element_score
