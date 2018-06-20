# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from account.models import Account


BOLI_CHOICES = (
    ('1', _("Shanti Dhara")),
    ('2', _("Abhishek")),
    ('3', _("Chatra")),
)


class Mandir(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("mandir name"))
    address = models.CharField(max_length=255, verbose_name=_("mandir location"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))

    class Meta:
        verbose_name = _("Mandir")
        verbose_name_plural = _("Mandirs")

    def __unicode__(self):
        return self.name


class Record(models.Model):
    """
    Boil records entry model.
    """
    mandir = models.ForeignKey(Mandir, verbose_name=_('mandir'), related_name='mandirs')
    account = models.ForeignKey(Account, verbose_name=_('account'), related_name='accounts')
    title = models.CharField(max_length=2, choices=BOLI_CHOICES, default='1')
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    amount = models.IntegerField(verbose_name=_("amount"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    boli_date = models.DateTimeField(verbose_name=_("boli date"), blank=True, null=True)
    payment_date = models.DateTimeField(verbose_name=_("payment date"), blank=True, null=True)
    transaction_id = models.CharField(max_length=255, verbose_name=_("transaction id"), blank=True, null=True)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Record")
        verbose_name_plural = _("Records")

    def __unicode__(self):
        return self.title

    def get_title(self):
        """
        Return human readable data
        """
        boils = dict(BOLI_CHOICES)
        return boils.get(self.title)

    def is_paid(self):
        """
        Will return paid or not paid
        """
        return _('Not Paid') if not self.paid else _('Paid')
