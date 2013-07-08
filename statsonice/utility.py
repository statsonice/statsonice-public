import urllib2

from django.http import HttpResponse

from statsonice.models import Settings

def save_settings(key, value):
    s = Settings()
    s.key = key
    s.value = value
    s.save()

def cache_blog(request):
    try:
        f = urllib2.urlopen('http://blog.statsonice.com/most-recent-post.php')
        blog_post = f.read().split("\n")
        save_settings('blog_post_url', blog_post[0])
        save_settings('blog_post', blog_post[1])
        save_settings('blog_post_date', blog_post[2])
        return HttpResponse('Loaded')
    except:
        return HttpResponse('Not Found')

