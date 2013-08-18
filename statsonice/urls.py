from django.conf.urls import patterns, include, url

from django.conf import settings

urlpatterns = ('',
    # Static Pages
    url(r'^$', 'statsonice.static.home', name='home'),
    url(r'^about/$', 'statsonice.static.about', name='about'),
    url(r'^contact/$', 'statsonice.static.contact', name='contact'),
    url(r'^privacy_policy/$', 'statsonice.static.privacy_policy', name='privacy_policy'),
    url(r'^terms_of_use/$', 'statsonice.static.terms_of_use', name='terms_of_use'),
    url(r'^faq/$', 'statsonice.static.faq', name='faq'),

    # Search
    url(r'^search_skaters/$', 'statsonice.search.skaters', name='search_skaters'),
    url(r'^search_competitions/$', 'statsonice.search.competitions', name='search_competitions'),
    url(r'^search_head_to_head/$', 'statsonice.search.head_to_head', name='search_head_to_head'),

    # Skater Profiles
    url(r'^skater/$', 'statsonice.skater.browse', name='skater_browse'),
    url(r'^skater/(?P<skater_first_name>.+)/(?P<skater_last_name>.+)/$', 'statsonice.skater.profile', name='skater_profile'),
    url(r'^skaterteam/(?P<first_skater_first_name>.+)/(?P<first_skater_last_name>.+)/(?P<second_skater_first_name>.+)/(?P<second_skater_last_name>.+)/$', 'statsonice.skater.team_profile', name='team_profile'),

    # Competition/Program Result Pages
    url(r'^competition/$', 'statsonice.competition.browse', name='competition_browse'),
    url(r'^competition/(?P<competition_name>.+)/(?P<competition_year>[0-9]+)/$', 'statsonice.competition.profile', name='competition_profile'),
    url(r'^competition/(?P<competition_name>.+)/(?P<competition_year>[0-9]+)/(?P<category>[A-Z]{3,6})/(?P<qualifying>[A-Za-z]*)/(?P<level>[A-Z]{2,3})/(?P<segment>[A-Z]{2})/$', 'statsonice.competition.segment_summary', name='segment_summary'),
    url(r'^competition/(?P<competition_name>.+)/(?P<competition_year>[0-9]+)/(?P<first_skater_first_name>.+)/(?P<first_skater_last_name>.+)/(?P<second_skater_first_name>.+)/(?P<second_skater_last_name>.+)/$', 'statsonice.competition.skater_result_profile_team', name='skater_result_profile_team'),
    url(r'^competition/(?P<competition_name>.+)/(?P<competition_year>[0-9]+)/(?P<skater_first_name>.+)/(?P<skater_last_name>.+)/$', 'statsonice.competition.skater_result_profile_single', name='skater_result_profile_single'),

    # Stats
    url(r'^stats/$', 'statsonice.stats.stats', name='stats'),
    url(r'^stats/hth/singles/(?P<skater1_first_name>.+)/(?P<skater1_last_name>.+)/(?P<skater2_first_name>.+)/(?P<skater2_last_name>.+)/$', 'statsonice.stats.stats_head_to_head_singles', name='head_to_head_singles'),
    url(r'^stats/hth/teams/(?P<skater1_first_name>.+)/(?P<skater1_last_name>.+)/(?P<skater2_first_name>.+)/(?P<skater2_last_name>.+)/(?P<skater3_first_name>.+)/(?P<skater3_last_name>.+)/(?P<skater4_first_name>.+)/(?P<skater4_last_name>.+)/$', 'statsonice.stats.stats_head_to_head_teams', name='head_to_head_teams'),
    url(r'^stats/competition_preview/$', 'statsonice.stats.stats_competition_preview', name='competition_preview'),
    url(r'^stats/competition_preview/(?P<competition_name>.+)/(?P<competition_year>[0-9]+)/$', 'statsonice.stats.stats_competition_preview_detailed', name='competition_preview_detailed'),
    url(r'^stats/element_stats/$', 'statsonice.stats.stats_element_stats', name='element_stats'),

    # Website User Pages
    url(r'^user/register/$', 'statsonice.user.register', name='register'),
    url(r'^user/login/', 'statsonice.user.login', name='login'),
    url(r'^user/logout/$', 'statsonice.user.logout', name='logout'),
    url(r'^user/account/$', 'statsonice.user.account', name='account'),
    url(r'^user/subscribe/$', 'statsonice.user.subscribe', name='subscribe'),
    #url(r'^user/change_account_settings/$', 'statsonice.user.change_account_settings', name='change_account_settings'),
    #url(r'^user/payment_processing/$', 'statsonice.user.payment_processing', name='payment_processing'),
    #url(r'^user/upgrade_account/$', 'statsonice.user.upgrade_account', name='upgrade_account'),

    # Utility pages
    url(r'^cache_blog/$', 'statsonice.utility.cache_blog', name='cache_blog'),
    url(r'^robots\.txt$', 'statsonice.static.robots', name='robots'),
)

# Load Admin Site
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    from django.db.models import get_models, get_app
    from django.contrib.admin.sites import AlreadyRegistered
    for model in get_models(get_app('statsonice')):
        try:
            admin.site.register(model)
        except AlreadyRegistered:
            pass
    admin.autodiscover()
    urlpatterns += (
        (r'^admin/', include(admin.site.urls)),
    )


urlpatterns = patterns(*urlpatterns)
