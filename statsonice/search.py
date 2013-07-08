import datetime
import os.path
from django.shortcuts import render_to_response, redirect, render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from util.settings import STATIC_ROOT, STATIC_URL
from statsonice.models import *
import statsonice.backend.search as search_backend


# Render an error message instead of the normal search result
#
def search_error(error_message):
    return render_to_response('include/search_result.dj', {
        'error_message': error_message,
    })

# Search skaters
#
@ensure_csrf_cookie
def skaters(request):
    if request.method == 'POST':
        search_params = request.POST.copy()
        # Actually do a search
        all_skaters = Skater.objects.all()
        search = search_backend.GeneralSearch(all_skaters)
        results = search.general_search(search_params, search_backend.SKATER_FIELD_TYPES)
        if type(results) == str or type(results) == unicode:
            return search_error(results)
        # Render response
        response = render_to_response('include/search_result.dj', {
            'results' : results,
        })
        return response
    return render(request, 'search_skaters.dj', {
        'countries': get_options('countries'),
        'genders': get_options('genders'),
        'coaches': get_options('coaches'),
        'months': get_options('months'),
    })


@ensure_csrf_cookie
def competitions(request):
    if request.method == 'POST':
        search_params = request.POST.copy()
        # Actually do a search
        all_competitions = Competition.objects.all()
        search = search_backend.GeneralSearch(all_competitions)
        results = search.general_search(search_params, search_backend.COMPETITION_FIELD_TYPES)
        if type(results) == str or type(results) == unicode:
            return search_error(results)
        response = render_to_response('include/search_result.dj', {
            'results' : results,
        })
        return response
    return render(request, 'search_competitions.dj', {
        'countries': get_options('countries'),
        'months': get_options('months'),
    })

@ensure_csrf_cookie
def programs(request):
    if request.method == 'POST':
        search_params = request.POST.copy()
        # Actually do a search
        all_programs = Program.objects.all()
        search = search_backend.GeneralSearch(all_programs)
        results = search.general_search(search_params, search_backend.PROGRAM_FIELD_TYPES)
        if type(results) == str or type(results) == unicode:
            return search_error(results)
        return render_to_response('include/search_result.dj', {
            'results' : results,
        })
    return render(request, 'search_programs.dj', {
        'skaters': get_options('skaters'),
        'competitions': get_options('competitions'),
        'categories': get_options('categories'),
        'segment': get_options('segment'),
        'level': get_options('level'),
    })

def get_options(option):
    if option == 'countries':
        return [country.get_country_name() for country in Country.objects.all()]
    if option == 'coaches':
        return [coach.first_name+' '+coach.last_name for coach in Coach.objects.all()]
    if option == 'months':
        return search_backend.MONTHS
    if option == 'genders':
        return ['', 'Female', 'Male']
    if option == 'competitions':
        return [competition.name for competition in Competition.objects.all()]
    if option == 'skaters':
        return [skater.view_name() for skater in Skater.objects.all()]
    if option == 'categories':
        return ['']+[category.category for category in Category.objects.all()]
    if option == 'segment':
        return [segment.segment for segment in Segment.objects.all()]
    if option == 'level':
        return [level.level for level in Level.objects.all()]


