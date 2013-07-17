"""
Prints exceptions to stdout; useful for seeing errors
when running a test server
"""
class ExceptionLoggingMiddleware(object):
    def process_exception(self, request, exception):
        if request.META["SERVER_NAME"] != 'testserver':
            import traceback
            print traceback.format_exc()
