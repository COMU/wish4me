#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin

from wish4meUI.wish.models import Wish
from wish4meUI.wish.models import WishCategory
from wish4meUI.wish.models import Wishlist
from wish4meUI.wish.models import WishPhoto


class WishPhotoPhotoInline(admin.TabularInline):
    model = WishPhoto


class WishAdmin(admin.ModelAdmin):
    inlines = [
        WishPhotoPhotoInline
    ]


admin.site.register(Wish, WishAdmin)
admin.site.register(WishCategory)
admin.site.register(Wishlist)
