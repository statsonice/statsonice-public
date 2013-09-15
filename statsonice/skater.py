from django.core.cache import cache
from django.http import Http404
from django.shortcuts import render, redirect
from time import time

from statsonice.models import Skater, SkaterTeam, SkaterName, Competitor, Program
from statsonice.backend.profileresults import ProfileResults
from statsonice import search
from includes import unitconversion


# View to browse through all skaters
#
def browse(request):
    cache_key = 'skater_browse'
    response_dict = cache.get(cache_key)
    if not response_dict:
        skaters = {}
        for skater in Skater.objects.order_by('skatername__last_name'):
            url = skater.url()
            view_name = skater.view_name()
            skaters[skater.id] = [url, view_name, []]
        skater_teams = SkaterTeam.objects.all()
        for skater_team in skater_teams:
            url = skater_team.url()
            view_name = skater_team.view_name()
            skaters[skater_team.female_skater_id][2].append([url, view_name])
            skaters[skater_team.male_skater_id][2].append([url, view_name])
        skaters = skaters.values()
        skaters.sort(key=lambda i: i[1])
        response_dict = {'skaters':skaters}
        cache.set(cache_key, response_dict)
    return render(request, 'skater_browse.dj', response_dict)

# View to display information about a single skater
#
def profile(request, skater_first_name, skater_last_name):
    # Get skater
    start = time()
    try:
        skater = Skater.find_skater_by_url_name(skater_first_name, skater_last_name)
    except:
        raise Http404
    skater_name = skater.get_default_skater_name()

    # Redirect to canonical name (and url) if not default skater name
    if skater.url_name() != (skater_first_name, skater_last_name):
        return redirect(skater.url())

    # Compute skater information
    skater.height_feet, skater.height_inches = unitconversion.metric_to_imperial(skater.height)
    skater.other_names = list(skater.skatername_set.all())
    skater.other_names.remove(skater_name)

    # get results matrices
    profile_results = ProfileResults(skater)
    personal_records, best_total = profile_results.get_best_isu_programs()
    isu_results_matrix, isu_years = profile_results.get_isu_results_matrix()

    # Get head to head autocomplete
    # TODO: this part is too slow, takes on the order of 15s
    '''
    skaters_dict = search.get_options('skaters_dict')
    for view_name, url_name in skaters_dict.items():
        skaters_dict[view_name] = url_name[0]+'/'+url_name[1]
    '''

    return render(request, 'skater.dj', {
        'skater_name': skater_name,
        'skater': skater,
        'isu_results_matrix': isu_results_matrix,
        'isu_years': isu_years,
        'personal_records': personal_records,
        'best_total': best_total,
        #'skaters_dict': skaters_dict,
    })

# View to display information about a skater team
#
def team_profile(request, first_skater_first_name, first_skater_last_name, second_skater_first_name, second_skater_last_name):
    try:
        first_skater = Skater.find_skater_by_url_name(first_skater_first_name, first_skater_last_name)
        second_skater = Skater.find_skater_by_url_name(second_skater_first_name, second_skater_last_name)
        skater_team = SkaterTeam.objects.get(female_skater=first_skater, male_skater=second_skater)
        competitor = Competitor.find_competitor(skater_team)
    except:
        raise Http404

    # skater heights
    first_skater.height_feet, first_skater.height_inches = unitconversion.metric_to_imperial(first_skater.height)
    second_skater.height_feet, second_skater.height_inches = unitconversion.metric_to_imperial(second_skater.height)

    # height gap
    if first_skater.height and second_skater.height:
        height_gap = second_skater.height - first_skater.height
        height_gap = list(unitconversion.metric_to_imperial(height_gap)) + [height_gap]
    else:
        height_gap = False

    # determine whether teams or dance
    program = Program.objects.filter(skater_result__competitor = competitor)
    if program.count() == 0:
        program = 0
        category = 0
    else:
        program = program[0]
        category = program.skater_result.category.category

    # get results matrices
    profile_results = ProfileResults(skater_team)
    personal_records, best_total = profile_results.get_best_isu_programs()
    isu_results_matrix, isu_years = profile_results.get_isu_results_matrix()

    # Get head to head autocomplete
    # TODO: this part is too slow, takes on the order of 15s
    '''
    teams_dict = search.get_options('teams_dict')
    for view_name, url_name in teams_dict.items():
        teams_dict[view_name] = url_name[0][0]+'/'+url_name[0][1]+'/'+url_name[1][0]+'/'+url_name[1][1]
    '''

    return render(request, 'skater_team.dj', {
            'first_skater': first_skater,
            'second_skater': second_skater,
            'height_gap': height_gap,
            'category': category,
            'skater_team': skater_team,
            'program': program,
            'isu_results_matrix': isu_results_matrix,
            'isu_years': isu_years,
            'personal_records': personal_records,
            'best_total': best_total,
            #'teams_dict': teams_dict,
        })
