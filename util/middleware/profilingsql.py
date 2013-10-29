"""
Add `?profsql` to the end of any URL and get it profiled for speed analysis
"""
from django.conf import settings
from django.db import connection

class ProfileSQLMiddleware(object):
    """
    http://yoursite.com/yourview/?profsql

    Add the "profsql" key to query string by appending ?profsql (or &profsql=)
    and you'll see the profiling results in your browser.
    It's set up to only be available in django's debug mode, is available for superuser otherwise,
    but you really shouldn't add this middleware to any production configuration.

    """
    def process_response(self, request, response):
        if not (settings.DEBUG or request.user.is_superuser) or 'profsql' not in request.GET:
            return response
        total_time = 0.0
        output = ""
        for query in connection.queries:
            nice_sql = query['sql'].replace('"', '').replace(',',', ')
            sql = "[%s]   %s" % (query['time'], nice_sql)
            output += sql+"\n"
            total_time = total_time + float(query['time'])
        output += "\n"
        output += "Total SQL Time "+str(total_time)
        response.content = "<pre>" + output + "</pre>"
        return response
