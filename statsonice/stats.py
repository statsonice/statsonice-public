from django.shortcuts import render, get_object_or_404, redirect
from django.utils import simplejson
from django.views.decorators.csrf import ensure_csrf_cookie

from datetime import datetime, timedelta

from statsonice.backend.headtohead import HeadToHead
from statsonice.backend.competitionpreview import CompPreviewStats
from statsonice.backend.elementstats import *
from statsonice.backend.top_scores import *
from statsonice.backend.scorecards import *
from statsonice.backend.stats import *
from statsonice.models import Skater, SkaterTeam, Competitor, Competition


def stats(request):
    return render(request, 'stats.dj')

def stats_head_to_head_singles(request, skater1_first_name, skater1_last_name, skater2_first_name, skater2_last_name):
    skater1 = Skater.find_skater_by_url_name(skater1_first_name, skater1_last_name)
    skater2 = Skater.find_skater_by_url_name(skater2_first_name, skater2_last_name)
    competitor1 = Competitor.find_competitor(skater1)
    competitor2 = Competitor.find_competitor(skater2)

    if skater1.gender != skater2.gender:
        return render(request, "head_to_head_error.dj", {
            'competitor1': competitor1,
            'competitor2': competitor2
        })

    hth = HeadToHead(competitor1,competitor2)
    s1_count, s2_count, hth_results = hth.get_head_to_head_results()
    s1_scores, s2_scores, num = hth.get_hth_graph_stats()

    s1_scores, s2_scores, num = s1_scores, s2_scores, simplejson.dumps(num)
    diff_scores = [round(s1 - s2,2) for s1, s2 in zip(s1_scores,s2_scores)]
    diff_scores = simplejson.dumps(diff_scores)

    hth_table_stats = hth.get_hth_table_stats()

    return render(request, 'head_to_head.dj', {
        'hth': hth,
        's1_count': s1_count,
        's2_count': s2_count,
        'hth_results': hth_results,
        's1_scores': s1_scores,
        's2_scores': s2_scores,
        'diff_scores': diff_scores,
        'num': num,
        'hth_table_stats': hth_table_stats
    })

def stats_head_to_head_teams(request, skater1_first_name, skater1_last_name, skater2_first_name, skater2_last_name, skater3_first_name, skater3_last_name, skater4_first_name, skater4_last_name):
    skater1 = Skater.find_skater_by_url_name(skater1_first_name, skater1_last_name)
    skater2 = Skater.find_skater_by_url_name(skater2_first_name, skater2_last_name)
    team1 = SkaterTeam.objects.get(female_skater=skater1, male_skater=skater2)
    competitor1 = Competitor.find_competitor(team1)
    skater3 = Skater.find_skater_by_url_name(skater3_first_name, skater3_last_name)
    skater4 = Skater.find_skater_by_url_name(skater4_first_name, skater4_last_name)
    team2 = SkaterTeam.objects.get(female_skater=skater3, male_skater=skater4)
    competitor2 = Competitor.find_competitor(team2)

    if competitor1.skater_team.is_dance() is not competitor2.skater_team.is_dance():
        return render(request, "head_to_head_error.dj", {
            'competitor1': competitor1,
            'competitor2': competitor2
        })

    hth = HeadToHead(competitor1,competitor2)
    s1_count, s2_count, hth_results = hth.get_head_to_head_results()
    s1_scores, s2_scores, num = hth.get_hth_graph_stats()

    s1_scores, s2_scores, num = s1_scores, s2_scores, simplejson.dumps(num)
    diff_scores = [round(s1 - s2,2) for s1, s2 in zip(s1_scores,s2_scores)]
    diff_scores = simplejson.dumps(diff_scores)

    hth_table_stats = hth.get_hth_table_stats()

    return render(request, 'head_to_head.dj', {
        'hth': hth,
        's1_count': s1_count,
        's2_count': s2_count,
        'hth_results': hth_results,
        's1_scores': s1_scores,
        's2_scores': s2_scores,
        'diff_scores': diff_scores,
        'num': num,
        'hth_table_stats': hth_table_stats
    })

def stats_competition_preview(request):
    now = datetime.now()
    now = now.date()
    then = now + timedelta(days=180)
    competitions = Competition.objects.filter(start_date__range=(now,then))

    return render(request, 'competition_preview.dj', {
        'competitions': competitions
    })

def stats_competition_preview_detailed(request, competition_name, competition_year):
    start = time()
    competition_name = competition_name.replace('-',' ')
    competition = get_object_or_404(Competition, name=competition_name, start_date__year = competition_year)
    if competition.end_date < datetime.now().date():
        return redirect(competition.url())

    print 'A', time() - start
    comp_preview = CompPreviewStats(competition)
    print 'B', time() - start
    comp_preview.get_projected_placements()
    print 'C', time() - start
    comp_preview.get_hth_records()
    print 'D', time() - start
    # comp_preview.calculate_medal_probability()

    return render(request, 'competition_preview_detailed.dj', {
        'competition': competition,
        'men_competitors': comp_preview.men,
        'ladies_competitors': comp_preview.ladies,
        'pairs_competitors': comp_preview.pairs,
        'dance_competitors': comp_preview.dance,
    })

@ensure_csrf_cookie
def stats_element_stats(request):
    # TODO: add dynamic if POST code to allow query from page
    # TODO: make element stats classes MUCH less expensive
        # - look to db_cleaning_script for some ideas/a start
    # what follows is only example code
    if request.method == 'POST':
        open_detailed = False
        elem_skater = request.POST.get('elementName')
        if ',' in elem_skater:
            temp = elem_skater.split(',')
            element_name = temp[0].strip()
            skater_name = temp[1].strip()
        else:
            element_name = elem_skater
            skater_name = ''
        category = request.POST.get('group1')
        category_name = category.strip().upper()
        element_cat_stats = ElementStats(element_name,skater_name,category)
        if element_name == '':
            element_name = 'None'
            category_name = 'None'
            skater_name = ''
            goes = [0]
            years = [0]
            time_series = [0]
            element_scores = None
        else:
            goes = element_cat_stats.goe_stats
            years = element_cat_stats.years
            time_series = element_cat_stats.attempts_time_series
            element_scores = element_cat_stats.element_scores
            if len(element_scores) > 300:
                element_scores = element_scores[len(element_scores)-300:]

            goes = simplejson.dumps(goes)
            years = simplejson.dumps(years)
            time_series = simplejson.dumps(time_series)
    else:
        element_name = '4S+2T'
        category_name = 'MEN'
        skater_name = 'Max Aaron'
        element_cat_stats = ElementStats(element_name,skater_name,category_name)
        goes = element_cat_stats.goe_stats
        years = element_cat_stats.years
        time_series = element_cat_stats.attempts_time_series
        element_scores = element_cat_stats.element_scores
        if len(element_scores) > 300:
            element_scores = element_scores[len(element_scores)-300:]

        goes = simplejson.dumps(goes)
        years = simplejson.dumps(years)
        time_series = simplejson.dumps(time_series)
        open_detailed = True

    print 'goes: ', goes
    return render(request, 'element_stats.dj', {
            'element_name': element_name,
            'category_name': category_name,
            'skater_name': skater_name,
            'goes': goes,
            'years': years,
            'time_series': time_series,
            'element_scores': element_scores,
            'open_detailed': open_detailed
        })

@ensure_csrf_cookie
def stats_top_scores(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        segment = request.POST.get('segment')
        start_year = int(request.POST.get('season'))
    else:
        category = 'MEN'
        segment = 'TOTAL'
        start_year = 0
    top_scores = TopScores(segment,category,start_year)
    return render(request, 'top_scores.dj', {
            'top_scores': top_scores,
            'segment': segment,
            'category': category,
            'start_year': start_year
        })

def articles(request, article_name=None):
    return render(request, 'articles.dj', {
            'article_name': article_name
        })

def score_cards(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        segment = request.POST.get('segment')
    skater_name = 'Curran Oi'
    competitor = Competitor.objects.get(skater__skatername__first_name="Curran")
    segment = 'FS'
    category = 'MEN'
    score_card = ScoreCard(competitor,category,segment)
    element_names = score_card.element_names
    pcs = score_card.pcs
    return render(request, 'score_cards.dj', {
            'element_names': element_names,
            'skater_name': skater_name,
            'pcs': pcs,
            'segment': segment,
            'category': category
        })

def custom_stats(request):
    return render(request, 'custom_stats.dj')


