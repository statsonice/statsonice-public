from util.settings import *

# **WARNING** THIS SECRET KEY SHOULD NOT BE USED PUBLICLY
SECRET_KEY = 'f98rg$$l@=ibae7q79d0i#^ebh(w1@gl1#c*t_s^n#0#^4@5hb'

# make tests faster
SOUTH_TESTS_MIGRATE = False

DEBUG = True

# Print emails to stdout instead of actually sending emails
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Turn off caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

MIDDLEWARE_CLASSES += (
    'util.middleware.timer.TimerMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'util.middleware.profiling.ProfileMiddleware',
)

INSTALLED_APPS += (
    'django.contrib.admin',
    #'debug_toolbar',
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    'debug_toolbar.panels.profiling.ProfilingDebugPanel',
)

# Set the allowed hosts setting to allow any host
from fnmatch import fnmatch
class glob_list(list):
    def __contains__(self, key):
        for elt in self:
            if fnmatch(key, elt): return True
        return False

INTERNAL_IPS = glob_list([
    '127.0.0.1',
    '10.*.*.*'
    ])
