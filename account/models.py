# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Account(models.Model):
    phone_number = models.CharField(max_length=10, verbose_name=_("phone number"))
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    pan_card = models.CharField(max_length=10, verbose_name=_("PAN Card"), blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __unicode__(self):
        return self.phone_number

    def __str__(self):
        return self.phone_number


class UserProfile(models.Model):
    """
    User profile which will associate with temple (Mandir)
    """
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    mandir = models.ForeignKey('mandir.Mandir', verbose_name=_('mandir'), related_name='user_mandir', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username
