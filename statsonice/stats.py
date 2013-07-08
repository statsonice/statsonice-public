from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson

from datetime import datetime, timedelta

from statsonice.backend.headtohead import HeadToHead
from statsonice.backend.competitionpreview import CompPreviewStats
from statsonice.backend.stats import *
from statsonice.models import Skater, SkaterPair, Competitor, Competition


def stats(request):
    return render(request, 'stats.dj')

def stats_dance(request):
    return render(request, 'stats_dance.dj')

def stats_ladies(request):
    return render(request, 'stats_ladies.dj')

def stats_men(request):
    return render(request, 'stats_men.dj')

def stats_pairs(request):
    return render(request, 'stats_pairs.dj')

def stats_head_to_head_singles(request, skater1_first_name, skater1_last_name, skater2_first_name, skater2_last_name):

    skater1 = Skater.find_skater_by_url_name(skater1_first_name, skater1_last_name)
    skater2 = Skater.find_skater_by_url_name(skater2_first_name, skater2_last_name)
    competitor1 = Competitor.find_competitor(skater1)
    competitor2 = Competitor.find_competitor(skater2)

    hth = HeadToHead(competitor1,competitor2)
    s1_count, s2_count, hth_results = hth.get_head_to_head_results()
    s1_scores, s2_scores, num = hth.get_hth_graph_stats()
    
    s1_scores, s2_scores, num = simplejson.dumps(s1_scores), simplejson.dumps(s2_scores), simplejson.dumps(num)

    hth_table_stats = hth.get_hth_table_stats()
    
    return render(request, 'head_to_head.dj', {
        'hth': hth,
        's1_count': s1_count,
        's2_count': s2_count,
        'hth_results': hth_results,
        's1_scores': s1_scores,
        's2_scores': s2_scores,
        'num': num,
        'hth_table_stats': hth_table_stats
    })

def stats_head_to_head_teams(request, skater1_first_name, skater1_last_name, skater2_first_name, skater2_last_name, skater3_first_name, skater3_last_name, skater4_first_name, skater4_last_name):

    team1 = SkaterPair.find_skater_pair_by_url_name(skater1_first_name, skater1_last_name, skater2_first_name, skater2_last_name)
    team2 = SkaterPair.find_skater_pair_by_url_name(skater3_first_name, skater3_last_name, skater4_first_name, skater4_last_name)
    competitor1 = Competitor.find_competitor(team1)
    competitor2 = Competitor.find_competitor(team2)

    hth = HeadToHead(competitor1,competitor2)
    s1_count, s2_count, hth_results = hth.get_head_to_head_results()
    s1_scores, s2_scores, num = hth.get_hth_graph_stats()
    
    s1_scores, s2_scores, num = simplejson.dumps(s1_scores), simplejson.dumps(s2_scores), simplejson.dumps(num)

    hth_table_stats = hth.get_hth_table_stats()
    
    return render(request, 'head_to_head.dj', {
        'hth': hth,
        's1_count': s1_count,
        's2_count': s2_count,
        'hth_results': hth_results,
        's1_scores': s1_scores,
        's2_scores': s2_scores,
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
    competition_name = competition_name.replace('-',' ')
    competition = get_object_or_404(Competition, name=competition_name, start_date__year = competition_year)

    comp_preview = CompPreviewStats(competition)
    comp_preview.get_projected_placements()
    comp_preview.get_hth_records()
    comp_preview.calculate_medal_probability()

    return render(request, 'competition_preview_detailed.dj', {
        'competition': competition,
        'men_competitors': comp_preview.men,
        'ladies_competitors': comp_preview.ladies,
        'pairs_competitors': comp_preview.pairs,
        'dance_competitors': comp_preview.dance,
    })


