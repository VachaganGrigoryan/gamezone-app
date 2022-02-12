from server.settings.base import *

ALLOWED_HOSTS = []

DEBUG = True


INSTALLED_APPS += THIRD_PARTY_APPS + PROJECT_APPS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': 5432,
    }
}




# LOCAL_APPS = [
#     'debug_toolbar',
# ]
# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.history.HistoryPanel',
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
#     'debug_toolbar.panels.profiling.ProfilingPanel',
# ]
#
# INTERNAL_IPS = ["127.0.0.1:8000"]
#
# import mimetypes
# mimetypes.add_type("application/javascript", ".js", True)
#
# # This example is unlikely to be appropriate for your project.
# DEBUG_TOOLBAR_CONFIG = {
#     'INSERT_BEFORE': '</body>',
#     # 'SHOW_TEMPLATE_CONTEXT': True,
#
#     'INTERCEPT_REDIRECTS': False,
#     'JQUERY_URL': 'https://cdn.bootcss.com/jquery/3.4.1/jquery.min.js',
#     'SHOW_TOOLBAR_CALLBACK': lambda request: True,
#     # # Toolbar options
#     # 'RESULTS_CACHE_SIZE': 100,
#     # # 'DISABLE_PANELS': False,
#     # 'RENDER_PANELS': False,
#     'SHOW_COLLAPSED': False,
#     # # Panel options
#     # 'SQL_WARNING_THRESHOLD': 100,   # milliseconds
# }
