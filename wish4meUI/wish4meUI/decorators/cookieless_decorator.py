# -*- coding: utf-8 -*-

from functools import wraps
from django.conf import settings
from django.utils.importlib import import_module

def session_from_http_params(view_func):
    @wraps(view_func)
    def decorated(request, *args, **kwargs):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = request.GET.get(settings.SESSION_COOKIE_NAME, None)
        if session_key is None:
            session_key = request.POST.get(settings.SESSION_COOKIE_NAME, None)
        request.session = engine.SessionStore(session_key)
        return view_func(request, *args, **kwargs)
    return decorated