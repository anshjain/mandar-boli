# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import Account


class BoliChoice(models.Model):
    """
    Boli choices so we can add and remove
    """
    name = models.CharField(max_length=50, verbose_name=_("name"))
    request_choice = models.BooleanField(default=False, verbose_name=_("Request Choices"))

    class Meta:
        verbose_name = _("Boli Choice")
        verbose_name_plural = _("Boli Choices")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Mandir(models.Model):
    """
    Mandir records
    """
    name = models.CharField(max_length=255, verbose_name=_("mandir name"))
    contract_number = models.CharField(max_length=10, verbose_name=_("contact number"), blank=True, null=True, unique=True)
    email = models.EmailField(max_length=70, blank=True, null=True, unique=True)
    description = models.CharField(max_length=255, verbose_name=_("Mandir Description"), blank=True, null=True, unique=True)
    committee_name = models.CharField(max_length=255, blank=True, null=True, unique=True, verbose_name=_("Committee name"))
    city = models.CharField(max_length=20, verbose_name=_("city"), default='Pune')
    state = models.CharField(max_length=20, verbose_name=_("state"), default='maharashtra')
    pin_code = models.CharField(max_length=6, verbose_name=_("pin code"), default='411021')
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=18.557024, verbose_name=_("latitude"))
    long = models.DecimalField(max_digits=9, decimal_places=6, default=73.75092, verbose_name=_("longitude"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    status = models.BooleanField(default=True)

    #whats app details
    whatsapp_number = models.CharField(max_length=10, verbose_name=_("Whatsapp number"), blank=True, null=True)
    whatsapp_message = models.TextField(max_length=1000, verbose_name=_("Whatsapp Message"), blank=True, null=True)

    # bank details
    account_name = models.CharField(max_length=255, verbose_name=_("Account Name"), blank=True, null=True, unique=True)
    bank_name = models.CharField(max_length=255, verbose_name=_("Bank Name"), blank=True, null=True, unique=True)
    account_number = models.CharField(max_length=20, verbose_name=_("Account Number"), blank=True, null=True, unique=True)
    ifsc_code = models.CharField(max_length=11, verbose_name=_("IFSC Code"), blank=True, null=True, unique=True)
    branch = models.CharField(max_length=255, verbose_name=_("Branch"), blank=True, null=True, unique=True)

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

    def __str__(self):
        return self.name


class MandirImage(models.Model):
    """
    Mandir Images
    """
    mandir = models.ForeignKey(Mandir, verbose_name=_('mandir'), related_name='mandir_image', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_('image'), upload_to='images/')
    title = models.TextField(verbose_name=_("title"), blank=True, null=True)
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    event_url = models.URLField(null=True, blank=True, default='')

    class Meta:
        verbose_name = _("Mandir Image")
        verbose_name_plural = _("Mandir Images")

    def __unicode__(self):
        return self.mandir.name

    def __str__(self):
        return self.mandir.name


class Record(models.Model):
    """
    Boil records entry model.
    """
    mandir = models.ForeignKey(Mandir, verbose_name=_('mandir'), related_name='mandirs', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, verbose_name=_('account'), related_name='accounts', on_delete=models.CASCADE)
    title = models.ForeignKey(BoliChoice, verbose_name=_('title'), related_name='bolichoices', default='1', on_delete=models.CASCADE)
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    amount = models.IntegerField(verbose_name=_("amount"))
    remaining_amt = models.IntegerField(verbose_name=_("Remaining amount"), default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    boli_date = models.DateTimeField(verbose_name=_("boli date"), blank=True, null=True)
    payment_date = models.DateTimeField(verbose_name=_("payment date"), blank=True, null=True)
    transaction_id = models.CharField(max_length=255, verbose_name=_("transaction id"), blank=True, null=True)
    paid = models.BooleanField(default=False)
    request_by_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Record")
        verbose_name_plural = _("Records")

    def __unicode__(self):
        return self.title.name

    def get_default_description(self):
        """"
        Display description for corresponding to default mobile number.
        """
        return self.description.split('\n')[0]

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


class VratDetail(models.Model):
    """
    Vrat details
    """
    name = models.CharField(max_length=255, verbose_name=_("vrat name"))
    enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    vrat_date = models.DateTimeField(verbose_name=_("vrat date"), blank=True, null=True)

    class Meta:
        verbose_name = _("Vrat Detail")
        verbose_name_plural = _("Vrat Details")

    def __unicode__(self):
        return "{} {}".format(self.name, self.vrat_date.strftime("%m/%d/%Y"))

    def __str__(self):
        return "{} {}".format(self.name, self.vrat_date.strftime("%m/%d/%Y"))
