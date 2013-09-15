"""
This Middleware adds an X-Django-Request-Time request response
header to all pages so you can check how long any page takes
to load.  It also sends an email if it takes longer than 10 seconds to load
"""
from time import time

from django.core.mail import send_mail

class TimerMiddleware:
    def process_request(self, request):
        request._tm_start_time = time()

    def process_response(self, request, response):
        if not hasattr(request, "_tm_start_time"):
            return response

        total = time() - request._tm_start_time

        if total > 10:
            from_address = 'bot@statsonice.com'
            to_address = 'team@statsonice.com'
            subject = 'Long Running Script'
            message = str(total)+" seconds:\n\n"+request.path+"\n\n"+request.body
            send_mail(subject, message, from_address, [to_address])

        response['X-Django-Request-Time'] = '%fs' % total
        return response
