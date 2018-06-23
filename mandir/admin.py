# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mandir.models import Mandir, Record, MandirImage, BoliChoice


class MandirAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contract_number', 'email')


class RecordAdmin(admin.ModelAdmin):
    list_display = ('mandir', 'account', 'title', 'amount', 'boli_date', 'payment_date', 'transaction_id', 'paid')
    readonly_fields = ('account', 'mandir')


class MandirImageAdmin(admin.ModelAdmin):
    list_display = ('mandir',)


class BoliChoiceAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Mandir, MandirAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(MandirImage, MandirImageAdmin)
admin.site.register(BoliChoice, BoliChoiceAdmin)
