# class to compute compare data
from statsonice.models import SkaterResult, ResultIJS

class CompetitorCompare:

    def __init__(self,competitor):
        self.competitor = competitor
        self.scores = self.get_scores()

    def get_scores(self):
        scores = {}
        sp_scores = ResultIJS.objects.filter(program__segment__segment = 'SP',program__skater_result__competitor = self.competitor).order_by('-program__skater_result__competition__start_date')[:3]
        fs_scores = ResultIJS.objects.filter(program__segment__segment = 'FS',program__skater_result__competitor = self.competitor).order_by('-program__skater_result__competition__start_date')[:3]
        tot_scores = SkaterResult.objects.filter(competitor = self.competitor).order_by('-competition__start_date')[:3]
        scores['sp_scores'] = sp_scores
        scores['fs_scores'] = fs_scores
        scores['tot_scores'] = tot_scores
        return scores

class Compare:

    def __init__(self,skaters):
        self.skaters = skaters
        self.competitors = [skater.competitor() for skater in self.skaters]
        self.competitor_compares = [CompetitorCompare(competitor) for competitor in self.competitors]
        self.matrix = self.get_matrix()

    def get_hth(self,competitor1,competitor2):
        srs1 = SkaterResult.objects.filter(competitor=competitor1,withdrawal=False).order_by('competition__id')
        srs2 = SkaterResult.objects.filter(competitor=competitor2,withdrawal=False).select_related('competition__id')
        comps1 = [sr.competition for sr in srs1]
        comps = [sr.competition for sr in srs2 if sr.competition in comps1]
        res1 = srs1.filter(competition__in=comps)
        res2 = srs2.filter(competition__in=comps)

        i = 0
        s1_count, s2_count = 0, 0
        while i < len(res1):
            if res1[i].level != res2[i].level:
                i += 1
                continue
            if res1[i].total_score > res2[i].total_score:
                s1_count += 1
            else:
                s2_count += 1
            i += 1

        return (s1_count, s2_count)


    def get_matrix(self):
        matrix = {}
        for competitor1 in self.competitors:
            matrix[competitor1] = {}
            for competitor2 in self.competitors:
                matrix[competitor1][competitor2] = None

        for competitor1 in self.competitors:
            for competitor2 in self.competitors:
                if competitor1 == competitor2:
                    continue
                elif matrix[competitor2][competitor1] != None:
                    matrix[competitor1][competitor2] = matrix[competitor2][competitor1][::-1]
                else:
                    matrix[competitor1][competitor2] = self.get_hth(competitor1,competitor2)

        return matrix
