# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from account.models import Account, UserProfile


class AccountAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'description')
    search_fields = ('description',)
    list_per_page = 15


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_mandir_name')

    def get_mandir_name(self, obj):
        return obj.mandir.name
    get_mandir_name.short_description = 'Mandir Name'


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
