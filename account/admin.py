# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from account.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'description')
    # readonly_fields = ('user', 'phone_number', 'description')

admin.site.register(Account, AccountAdmin)
