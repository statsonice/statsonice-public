"""
These decorators help with caching
"""
from django.core.cache import cache
from django.shortcuts import render

# Decorator that can be used to cache dictionaries to be rendered
#
class cached_response_dict(object):
    def __init__(self, template):
        """
        Template to be rendered with the dictionary
        """
        self.template = template

    def __call__(self, view_function):
        """
        Check for already created response dictionary, then render it with the template
        """
        def wrapped_view_function(*args):
            cache_key = self.template+view_function.__name__+'-'.join(args[1:])
            response_dict = cache.get(cache_key)
            if not response_dict:
                response_dict = view_function(*args)
                cache.set(cache_key, response_dict)
            return render(args[0], self.template, response_dict)
        return wrapped_view_function


# Decorator that can be used to cache the output of a function and is uniqued
# based on the instance id
#
def cached_function(f):
    def wrapped(self, *args):
        cache_key = self.__class__.__name__ + '.' + f.__name__ + '.' + str(self.id)
        value = cache.get(cache_key)
        if value:
            return value
        value = f(self, *args)
        cache.set(cache_key, value)
        return value
    return wrapped

