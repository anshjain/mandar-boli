# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mandir.models import Mandir, Record, MandirImage, BoliChoice


class MandirAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contract_number', 'email')


class RecordAdmin(admin.ModelAdmin):
    list_display = ('get_mandir_name', 'get_account_no', 'get_title', 'amount', 'boli_date',
                    'payment_date', 'transaction_id', 'paid')
    readonly_fields = ('account', 'mandir')

    def get_mandir_name(self, obj):
        return obj.mandir.name
    get_mandir_name.short_description = 'Mandir Name'

    def get_account_no(self, obj):
        return obj.account.phone_number
    get_account_no.short_description = 'Phone Number'

    def get_title(self, obj):
        return obj.title.name
    get_title.short_description = 'Title'

    #Filtering on side - for some reason, this works
    list_filter = ['title', 'paid', 'account__phone_number']


class MandirImageAdmin(admin.ModelAdmin):
    list_display = ('get_mandir_name',)

    def get_mandir_name(self, obj):
        return obj.mandir.name
    get_mandir_name.short_description = 'Mandir Name'


class BoliChoiceAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Mandir, MandirAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(MandirImage, MandirImageAdmin)
admin.site.register(BoliChoice, BoliChoiceAdmin)
