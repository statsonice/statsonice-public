import urllib2

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect

from statsonice.models import Settings
from statsonice import user

def save_settings(key, value):
    s = Settings()
    s.key = key
    s.value = value
    s.save()

def cache_blog(request):
    try:
        f = urllib2.urlopen('http://blog.statsonice.com/statsonice/most-recent-post.php')
        blog_post = f.read().split("\n")
        save_settings('blog_post_url', blog_post[0])
        save_settings('blog_post', blog_post[1])
        save_settings('blog_post_date', blog_post[2])
        output = 'Loaded<br />'
        output += '<br />'.join(blog_post)
        return HttpResponse(output)
    except:
        return HttpResponse('Not Found')

def pair_profile(*args, **kwargs):
    return redirect(reverse('team_profile', kwargs=kwargs), permanent=True)

def require_subscribe(f):
    def wrapped(*args, **kwargs):
        # TODO - have code to check for subscription
        subscribed = True

        if subscribed:
            return f(*args, **kwargs)
        else:
            return user.subscribe(*args, **kwargs)
        return value
    return wrapped
