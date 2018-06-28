# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mandir.models import Mandir, Record, MandirImage, BoliChoice


class MandirAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contract_number', 'email')
    readonly_fields = ('user',)

    def get_queryset(self, request):
        """Limit records to those that belong to the user temple."""

        qs = super(MandirAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(user=request.user)


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

    def get_queryset(self, request):
        """Limit records to those that belong to the user temple."""

        qs = super(RecordAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(mandir=request.user.mandir)


class MandirImageAdmin(admin.ModelAdmin):
    list_display = ('get_mandir_name',)

    def get_mandir_name(self, obj):
        return obj.mandir.name
    get_mandir_name.short_description = 'Mandir Name'

    def get_queryset(self, request):
        """Limit records to those that belong to the user temple."""

        qs = super(MandirImageAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(mandir=request.user.mandir)


class BoliChoiceAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Mandir, MandirAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(MandirImage, MandirImageAdmin)
admin.site.register(BoliChoice, BoliChoiceAdmin)
