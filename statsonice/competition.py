from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import Http404

from statsonice.models import Competition, Competitor, Skater, SkaterTeam, Program, Qualifying
from statsonice.backend.programresults import SkaterResults, ProgramResults
from statsonice.backend.competitionresults import CompResults, SegmentResults

def browse(request):
    now = datetime.now().date()
    competitions = Competition.objects.filter(start_date__lt = now).order_by('-start_date')
    years = competitions.values_list('start_date', flat=True)
    years = list(set([start_date.year for start_date in years]))
    years.sort()
    years.reverse()
    competition_years = []
    for year in years:
        competition_years.append((year, competitions.filter(start_date__year = year)))
    return render(request, 'competition_browse.dj', {
        'competition_years': competition_years,
        'total_competitions': competitions.count()
    })


def profile(request, competition_name, competition_year):
    start = datetime.now()
    competition_name = competition_name.replace('-',' ')
    competition = get_object_or_404(Competition, name=competition_name, start_date__year = competition_year)
    if competition.skaterresult_set.values_list('program').count() == 0:
        return redirect(competition.preview_url())
    if competition.end_date > datetime.now().date():
        return redirect(competition.preview_url())

    comp_results = CompResults(competition)
    results = comp_results.get_results_by_category_and_level()
    combined_results = {}
    for category, results_in_category in results.items():
        category = category.lower()
        combined_results[category] = comp_results.get_combined_results(results_in_category)

    category_results = {}
    for category, cat_results in combined_results.items():
        category_results[category] = False
        for lev_qual_srs in cat_results:
            if lev_qual_srs:
                category_results[category] = True
                break

    print 'time: ', datetime.now() - start

    return render(request, 'competition.dj', {
        'comp_results': comp_results,
        'competition': competition,
        'category_results': category_results,
        'results': combined_results,
    })

def skater_result_profile_single(request, competition_name, competition_year, \
        skater_first_name, skater_last_name):
    try:
        skater = Skater.find_skater_by_url_name(skater_first_name, skater_last_name)
        competitor = Competitor.find_competitor(skater)
    except:
        raise Http404
    competition_name = competition_name.replace('-',' ')
    competition = get_object_or_404(Competition, name=competition_name, start_date__year=int(competition_year))
    return skater_result_profile(request, competition, competitor)

def skater_result_profile_team(request, competition_name, competition_year, \
        first_skater_first_name, first_skater_last_name, \
        second_skater_first_name, second_skater_last_name):
    try:
        first_skater = Skater.find_skater_by_url_name(first_skater_first_name, first_skater_last_name)
        second_skater = Skater.find_skater_by_url_name(second_skater_first_name, second_skater_last_name)
        skater_team = SkaterTeam.objects.get(female_skater=first_skater, male_skater=second_skater)
        competitor = Competitor.find_competitor(skater_team)
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
        'competitor': competitor
    })

def segment_summary(request, competition_name, competition_year, category, qualifying, level, segment):
    competition_name = competition_name.replace('-',' ')
    competition = get_object_or_404(Competition, name=competition_name, start_date__year = competition_year)
    if qualifying == 'final':
        qualifying = ''
    programs = Program.objects.filter(skater_result__competition = competition,
                                      skater_result__category__category = category,
                                      skater_result__level__level = level,
                                      segment__segment = segment,
                                      skater_result__qualifying__name = qualifying)

    segment_results = SegmentResults.get_results(programs)
    program_results = [ProgramResults(result.program) for result in segment_results]
    #[program.calculate_variables() for program in program_results]

    return render(request, 'segment.dj', {
        'competition': competition,
        'category': category,
        'qualifying':qualifying,
        'level': level,
        'segment': segment,
        'segment_results': segment_results,
        'programs': program_results
    })
