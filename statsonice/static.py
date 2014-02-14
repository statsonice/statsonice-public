from django.core.mail import send_mail
from django.shortcuts import render_to_response, render
from django.conf import settings

from statsonice.models import Skater, SkaterTeam, Competitor, SkaterName, Competition, SkaterResult, Program, Settings

def home(request):
    recent_competitions = Competition.objects.order_by('-start_date')[:8]
    competition_sum = Competition.objects.count()
    skater_sum = Skater.objects.count()
    team_sum = SkaterTeam.objects.count()

    # get random skater profile
    srs_num = 0
    while srs_num < 5:
        sr = SkaterResult.objects.filter(total_score__gt=150).order_by('?')[0]
        competitor = sr.competitor
        srs = SkaterResult.objects.filter(competitor=competitor,withdrawal=False,qualifying__name='')
        srs_num = srs.count()

    # best total score skater result
    srs = srs.order_by('-competition__start_date')[:5]

    return render(request, 'index.dj', {
        'recent_competitions': recent_competitions,
        'competition_sum': competition_sum,
        'skater_sum': skater_sum,
        'team_sum': team_sum,
        'competitor': competitor,
        'srs': srs,
        'blog_post_url': Settings.get_value('blog_post_url'),
        'blog_post': Settings.get_value('blog_post'),
        'blog_post_date': Settings.get_value('blog_post_date').split(" ")[0]
    })

def about(request):
    return render(request, 'about.dj')

def contact(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']
        except:
            return render(request, 'contact.dj')
        from_address = 'bot@statsonice.com'
        to_address = 'team@statsonice.com'
        subject = 'New Contact: '+subject
        message = "From: "+name+" ("+email+")  \n"+message
        send_mail(subject, message, from_address, [to_address])
        return render(request, 'contact.dj', {'submitted':True})
    return render(request, 'contact.dj')

def privacy_policy(request):
    return render(request, 'privacy_policy.dj')

def terms_of_use(request):
    return render(request, 'terms_of_use.dj')

def faq(request):
    return render(request, 'faq.dj')

def database_completion(request):
    return render(request, 'database_completion.dj')

# Render a robots.txt file
def robots(request):
    text = ''
    if settings.ENV != 'production':
        text = "User-agent: *\n"
        text += "Disallow: /\n"
    return render_to_response('robots.dj', {
        'text': text,
    }, content_type='text/plain')
