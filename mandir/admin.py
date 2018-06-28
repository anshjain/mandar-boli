# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from django.contrib import admin

from mandir.models import Mandir, Record, MandirImage, BoliChoice


class MandirAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contract_number', 'email')

    def get_queryset(self, request):
        """Limit records to those that belong to the user temple."""

        qs = super(MandirAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(id=request.user.userprofile.mandir.id)


class RecordResource(resources.ModelResource):

    mandir = Field()
    account = Field()
    title = Field()
    paid = Field()

    def dehydrate_mandir(self, record):
        return record.mandir.name

    def dehydrate_account(self, record):
        return record.account.phone_number

    def dehydrate_title(self, record):
        return record.title.name

    def dehydrate_paid(self, record):
        return 'Paid' if record.paid else 'Not Paid'

    class Meta:
        model = Record
        export_order = ('mandir', 'account', 'title', 'amount', 'boli_date', 'paid', 'description')
        exclude = ('created', 'transaction_id', 'payment_date', 'id')


class RecordAdmin(ImportExportModelAdmin):
    list_display = ('get_mandir_name', 'get_account_no', 'get_title', 'amount', 'boli_date',
                    'payment_date', 'transaction_id', 'paid')
    readonly_fields = ('account', 'mandir')
    resource_class = RecordResource

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
    list_filter = ['title', 'paid']

    def get_queryset(self, request):
        """Limit records to those that belong to the user temple."""

        qs = super(RecordAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(mandir=request.user.userprofile.mandir)


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
        return qs.filter(mandir=request.user.userprofile.mandir)


class BoliChoiceAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Mandir, MandirAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(MandirImage, MandirImageAdmin)
admin.site.register(BoliChoice, BoliChoiceAdmin)
