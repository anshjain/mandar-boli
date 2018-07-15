# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from events.models import Events, EventMember


class EventAdmin(admin.ModelAdmin):
    list_display = ('get_mandir_name', 'name', 'description', 'start_date', 'end_date')

    def get_mandir_name(self, obj):
        return obj.mandir.name
    get_mandir_name.short_description = 'Mandir Name'


class EventMemberAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'phone_number', 'number_of_person')


admin.site.register(Events, EventAdmin)
admin.site.register(EventMember, EventMemberAdmin)
