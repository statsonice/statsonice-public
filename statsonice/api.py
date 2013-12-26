import json

from django.http import HttpResponse
from django.db.models import Q

import statsonice.backend.search as search_backend
from statsonice.models import Skater

# API to search for skater names given a substring of the skater's name
#
def skater_name_search(request):
    if request.method != 'POST':
        return HttpResponse('')
    query = request.POST.get('skatername_query')
    if query == None:
        query = ''
    search = search_backend.GeneralSearch(Skater.objects.all())
    skaters = search.general_search({'skatername': query}, search_backend.SKATER_FIELD_TYPES)
    skater_names = [skater.url_name() for skater in skaters[:10]]
    return HttpResponse(json.dumps(skater_names))

# API to search for skater teams given a substring of one of the skater's names
#
def skater_team_search(request):
    if request.method != 'POST':
        return HttpResponse('')
    query = request.POST.get('skatername_query')
    if query == None:
        query = ''
    # Find skaters matching query
    search = search_backend.GeneralSearch(Skater.objects.all())
    skaters = search.general_search({'skatername': query}, search_backend.SKATER_FIELD_TYPES)
    partner_ids = skaters.values_list('male_skater__female_skater', 'female_skater__male_skater')
    partner_ids = partner_ids.filter(Q(male_skater__isnull = False) | Q(female_skater__isnull = False))
    partner_names = []
    for female_partner_id, male_partner_id in partner_ids[:10]:
        if female_partner_id == None:
            partner_id = male_partner_id
        else:
            partner_id = female_partner_id
        partner_name = Skater.objects.get(pk=partner_id).url_name()
        partner_names.append(partner_name)
    return HttpResponse(json.dumps(partner_names))
