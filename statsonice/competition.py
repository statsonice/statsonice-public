from datetime import datetime
import urllib

from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import Http404

from statsonice.models import Competition, Competitor, Skater, SkaterPair
from statsonice.backend.programresults import SkaterResults
from statsonice.backend.competitionresults import CompResults

def browse(request):
    now = datetime.now().date()
    competitions = Competition.objects.filter(end_date__lt = now)
    return render(request, 'competition_browse.dj', {
        'competitions': competitions
    })


def profile(request, competition_name, competition_year):
    competition_name = competition_name.replace('-',' ')
    competition = get_object_or_404(Competition, name=competition_name, start_date__year = competition_year)
    if competition.end_date > datetime.now().date():
        data = {'competition_name':competition_name, 'competition_year':competition_year}
        return redirect(reverse('competition_preview_detailed', kwargs=data))

    comp_results = CompResults(competition)
    results = comp_results.get_results_by_category_and_level()
    combined_results = {}
    for category, results_in_category in results.items():
        category = category.lower()
        combined_results[category] = comp_results.get_combined_results(results_in_category)
    return render(request, 'competition.dj', {
        'comp_results': comp_results,
        'competition': competition,
        'results': combined_results,
    })

def skater_result_profile_single(request, competition_name, competition_year, \
        skater_first_name, skater_last_name):
    skater = Skater.find_skater_by_url_name(skater_first_name, skater_last_name)
    try:
        competitor = Competitor.find_competitor(skater)
    except:
        raise Http404
    competition_name = competition_name.replace('-',' ')
    competition = get_object_or_404(Competition, name=competition_name, start_date__year=int(competition_year))
    return skater_result_profile(request, competition, competitor)

def skater_result_profile_pair(request, competition_name, competition_year, \
        first_skater_first_name, first_skater_last_name, \
        second_skater_first_name, second_skater_last_name):
    try:
        first_skater_first_name = urllib.unquote(first_skater_first_name)
        first_skater_last_name = urllib.unquote(first_skater_last_name)
        second_skater_first_name = urllib.unquote(second_skater_first_name)
        second_skater_last_name = urllib.unquote(second_skater_last_name)
        skater_pair = SkaterPair.find_skater_pair_by_url_name(first_skater_first_name, first_skater_last_name, second_skater_first_name, second_skater_last_name)
        competitor = Competitor.find_competitor(skater_pair)
    except:
        raise Http404
    competition_name = competition_name.replace('-',' ')
    competition = get_object_or_404(Competition, name=competition_name, start_date__year=int(competition_year))
    return skater_result_profile(request, competition, competitor)

def skater_result_profile(request, competition, competitor):
    skater_results = SkaterResults(competition, competitor)
    skater_results.load_program_results()
    return render(request, 'skater_result.dj', {
        'skater_results': skater_results,
    })

def segment_summary(request, competition_name, competition_year, category, level, segment):
    competition_name = competition_name.replace('-',' ')
    competition = get_object_or_404(Competition, name=competition_name, start_date__year = competition_year)

    comp_results = CompResults(competition)
    segment_results = comp_results.get_segment_results(category, level, segment)

    return render(request, 'segment.dj', {
        'competition': competition,
        'competition_name': competition_name,
        'competition_year': competition_year,
        'category': category,
        'level': level,
        'segment': segment,
        'segment_results': segment_results
    })
