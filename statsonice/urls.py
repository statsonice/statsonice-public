from django.conf.urls import patterns, url

def skater_url(skater_name):
    return r'(?P<'+skater_name+r'_first_name>.+)/(?P<'+skater_name+r'_last_name>.+)'
def competition_regex():
    return r'(?P<competition_name>.+)/(?P<competition_year>[0-9]+)'

urlpatterns = ('',
    # Static Pages
    url(r'^$',
        'statsonice.static.home', name='home'),
    url(r'^about/$',
        'statsonice.static.about', name='about'),
    url(r'^contact/$',
        'statsonice.static.contact', name='contact'),
    url(r'^privacy_policy/$',
        'statsonice.static.privacy_policy', name='privacy_policy'),
    url(r'^terms_of_use/$',
        'statsonice.static.terms_of_use', name='terms_of_use'),
    url(r'^faq/$',
        'statsonice.static.faq', name='faq'),
    url(r'^database_completion/$',
        'statsonice.static.database_completion', name='database_completion'),

    # Search
    url(r'^search_skaters/$',
        'statsonice.search.skaters', name='search_skaters'),
    url(r'^search_competitions/$',
        'statsonice.search.competitions', name='search_competitions'),
    url(r'^search_head_to_head/$',
        'statsonice.search.head_to_head', name='search_head_to_head'),

    # Skater Profiles
    url(r'^skater/$',
        'statsonice.skater.browse', name='skater_browse'),
    url(r'^skater/'+skater_url('skater')+r'/$',
        'statsonice.skater.profile', name='skater_profile'),
    url(r'^skaterteam/'+skater_url('first_skater')+r'/'+skater_url('second_skater')+r'/$',
        'statsonice.skater.team_profile', name='team_profile'),
    url(r'^skaterpair/'+skater_url('first_skater')+r'/'+skater_url('second_skater')+r'/$',
        'statsonice.utility.pair_profile', name='pair_profile'),

    # Competition/Program Result Pages
    url(r'^competition/$',
        'statsonice.competition.browse', name='competition_browse'),
    url(r'^competition/'+competition_regex()+r'/$',
        'statsonice.competition.profile', name='competition_profile'),
    url(r'^competition/'+competition_regex()+r'/(?P<category>[A-Z]{3,6})/(?P<qualifying>.*)/(?P<level>[A-Z]{2,3})/(?P<segment>[A-Z]{2})/$',
        'statsonice.competition.segment_summary', name='segment_summary'),
    url(r'^competition/'+competition_regex()+r'/'+skater_url('first_skater')+r'/'+skater_url('second_skater')+r'/$',
        'statsonice.competition.skater_result_profile_team', name='skater_result_profile_team'),
    url(r'^competition/'+competition_regex()+r'/'+skater_url('skater')+r'/$',
        'statsonice.competition.skater_result_profile_single', name='skater_result_profile_single'),


    # Stats
    url(r'^stats/$',
        'statsonice.stats.stats', name='stats'),
    url(r'^stats/hth/singles/'+skater_url('skater1')+r'/'+skater_url('skater2')+r'/$',
        'statsonice.stats.stats_head_to_head_singles', name='head_to_head_singles'),
    url(r'^stats/hth/teams/'+skater_url('skater1')+r'/'+skater_url('skater2')+r'/'+skater_url('skater3')+r'/'+skater_url('skater4')+r'/$',
        'statsonice.stats.stats_head_to_head_teams', name='head_to_head_teams'),
    url(r'^stats/competition_preview/$',
        'statsonice.stats.stats_competition_preview', name='competition_preview'),
    url(r'^stats/competition_preview/'+competition_regex()+r'/$',
        'statsonice.stats.stats_competition_preview_detailed', name='competition_preview_detailed'),
    url(r'^stats/element_stats/$',
        'statsonice.stats.stats_element_stats', name='element_stats'),
    url(r'^stats/top_scores/$',
        'statsonice.stats.stats_top_scores', name='top_scores'),
    url(r'^stats/articles/$',
        'statsonice.stats.articles', name='articles'),
    url(r'^stats/articles/(?P<article_name>.+)/$',
        'statsonice.stats.articles', name='articles'),
    url(r'^stats/score_cards/$',
        'statsonice.stats.score_cards', name='score_cards'),
    url(r'^stats/custom/$',
        'statsonice.stats.custom_stats', name='custom_stats'),

    # Website User Pages
    url(r'^user/register/$',
        'statsonice.user.register', name='register'),
    url(r'^user/login/',
        'statsonice.user.login', name='login'),
    url(r'^user/logout/$',
        'statsonice.user.logout', name='logout'),
    url(r'^user/account/$',
        'statsonice.user.account', name='account'),
    url(r'^user/subscribe/$',
        'statsonice.user.subscribe', name='subscribe'),
    url(r'^user/change_account_settings/$',
        'statsonice.user.change_account_settings', name='change_account_settings'),

    # Utility pages
    url(r'^cache_blog/$',
        'statsonice.utility.cache_blog', name='cache_blog'),
    url(r'^robots\.txt$',
        'statsonice.static.robots', name='robots'),
)

urlpatterns = patterns(*urlpatterns)
