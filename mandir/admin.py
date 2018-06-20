# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mandir.models import Mandir, Record


class MandirAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


class RecordAdmin(admin.ModelAdmin):
    list_display = ('mandir', 'account', 'title', 'amount', 'boli_date', 'payment_date', 'transaction_id', 'paid')
    readonly_fields = ('account', 'mandir')


admin.site.register(Mandir, MandirAdmin)
admin.site.register(Record, RecordAdmin)
