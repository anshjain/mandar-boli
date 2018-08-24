# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mandir.models import Mandir


class Events(models.Model):
    """
    Manage event information.
    """
    name = models.CharField(max_length=255, verbose_name=_("Event Name"))
    description = models.TextField(max_length=1500, verbose_name=_("Event Description"))
    mandir = models.ForeignKey(Mandir, verbose_name=_('mandir'), related_name='mandir_event')
    start_date = models.DateTimeField(verbose_name=_("start date"))
    end_date = models.DateTimeField(verbose_name=_("end date"), blank=True, null=True, unique=True)
    status = models.BooleanField(default=True)
    member_required = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class EventMember(models.Model):
    """
    Event member list
    """
    event = models.ForeignKey(Events, verbose_name=_('event'))
    create = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    phone_number = models.CharField(max_length=10, verbose_name=_("phone number"))
    name = models.CharField(max_length=255, verbose_name=_("Event Name"))
    number_of_person = models.CharField(max_length=2, verbose_name=_("number of person"),
                                        blank=True, null=True, unique=True)

    class Meta:
        verbose_name = _("Event Member")
        verbose_name_plural = _("Event Members")

    def __unicode__(self):
        return "{}-{}".format(self.event.name, self.name)

    def __str__(self):
        return "{}-{}".format(self.event.name, self.name)