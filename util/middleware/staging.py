"""
This Middleware checks if the django environment is set to staging.
If the environment is a staging environment, password protect the page.
"""
import os
from django.conf import settings
from django.shortcuts import render

class StagingMiddleware(object):
    STAGING_PASSWORD = 'staging'
    ALLOWED_URLS = ['cache_blog/']

    def process_request(self, request):
        if settings.ENV != 'staging':
            return None
        if StagingMiddleware.STAGING_PASSWORD in request.COOKIES:
            return None
        if self.check_password(request):
            return None
        for url in StagingMiddleware.ALLOWED_URLS:
            if url in request.path:
                return None
        return render(request, 'staging.dj')

    def process_response(self, request, response):
        if self.check_password(request):
            response.set_cookie(StagingMiddleware.STAGING_PASSWORD)
        return response

    def check_password(self, request):
        if 'pass' in request.GET:
            if request.GET['pass'] == StagingMiddleware.STAGING_PASSWORD:
                return True
        return False
