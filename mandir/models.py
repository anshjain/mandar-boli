# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from account.models import Account


class BoliChoice(models.Model):
    """
    Boli choices so we can add and remove
    """
    name = models.CharField(max_length=50, verbose_name=_("name"))

    class Meta:
        verbose_name = _("Boli Choice")
        verbose_name_plural = _("Boli Choices")

    def __unicode__(self):
        return self.name


class Mandir(models.Model):
    """
    Mandir records
    """
    name = models.CharField(max_length=255, verbose_name=_("mandir name"))
    contract_number = models.CharField(max_length=10, verbose_name=_("contact number"), blank=True, null= True, unique= True)
    email = models.EmailField(max_length=70, blank=True, null= True, unique= True)
    address = models.CharField(max_length=255, verbose_name=_("mandir location"))
    city = models.CharField(max_length=20, verbose_name=_("city"), default='Pune')
    state = models.CharField(max_length=20, verbose_name=_("state"), default='maharashtra')
    pin_code = models.CharField(max_length=6, verbose_name=_("pin code"), default='411021')
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=18.557024, verbose_name=_("latitude"))
    long = models.DecimalField(max_digits=9, decimal_places=6, default=73.75092, verbose_name=_("longitude"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))

    def get_images(self):
        """
        return list of images associated with mandir object
        """
        return self.mandir_image.all()

    class Meta:
        verbose_name = _("Mandir")
        verbose_name_plural = _("Mandirs")

    def __unicode__(self):
        return self.name


class MandirImage(models.Model):
    """
    Mandir Images
    """
    mandir = models.ForeignKey(Mandir, verbose_name=_('mandir'), related_name='mandir_image')
    image = models.ImageField(verbose_name=_('image'), upload_to='pics/')
    title = models.TextField(verbose_name=_("title"), blank=True, null=True)
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)

    class Meta:
        verbose_name = _("Mandir Image")
        verbose_name_plural = _("Mandir Images")

    def __unicode__(self):
        return self.mandir.name


class Record(models.Model):
    """
    Boil records entry model.
    """
    mandir = models.ForeignKey(Mandir, verbose_name=_('mandir'), related_name='mandirs')
    account = models.ForeignKey(Account, verbose_name=_('account'), related_name='accounts')
    title = models.ForeignKey(BoliChoice, verbose_name=_('title'), related_name='bolichoices', default='1')
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
        return self.title

    def is_paid(self):
        """
        Will return paid or not paid
        """
        return _('Not Paid') if not self.paid else _('Paid')
