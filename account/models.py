# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Account(models.Model):
    phone_number = models.CharField(max_length=10, verbose_name=_("phone number"))
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __unicode__(self):
        return self.phone_number