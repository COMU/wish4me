import os, sys
sys.path.append('/home/oguz/git/wish4me')
os.environ['DJANGO_SETTINGS_MODULE'] = 'wish4meUI.settings'

import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    return _application(environ, start_response)
