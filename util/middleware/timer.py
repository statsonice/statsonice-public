"""
This Middleware adds an X-Django-Request-Time request response
header to all pages so you can check how long any page takes
to load
"""
from time import time

class TimerMiddleware:
    def process_request(self, request):
        request._tm_start_time = time()

    def process_response(self, request, response):
        if not hasattr(request, "_tm_start_time"):
            return response

        total = time() - request._tm_start_time

        response['X-Django-Request-Time'] = '%fs' % total
        return response
