#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from wish4meUI.wish.models import Wish, WishCategory

admin.site.register(Wish)
admin.site.register(WishCategory)
