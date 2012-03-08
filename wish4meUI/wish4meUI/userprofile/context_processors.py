#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from django.conf import settings

def default_profile_image(context):
    return {'DEFAULT_PROFILE_PICTURE': settings.DEFAULT_PROFILE_PICTURE}
