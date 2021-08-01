# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from datetime import datetime
from mandir.models import BoliChoice


PAYMENT_MODES = (
    ('Cash', 'Cash'),
    ('Online', 'Online'),
    ('Cheque', 'Cheque'),
)


class SearchForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'SEARCH', 'autocomplete': 'off'}))


class EntryForm(forms.Form):
    title = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'w3-input w3-border',
                                                              'style': 'height: 45px; margin-left:6px; width:98%'}),
                                   queryset=BoliChoice.objects.all(), required=True)
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', max_length=10,
                                    widget=forms.NumberInput(
                                        attrs={'placeholder': 'Phone Number',
                                               'autocomplete': 'off', 'class': 'w3-input w3-border',
                                               'onkeyup': "javascript:get_description();"}),
                                    error_messages={
                                        'required': "Phone number must be entered in the format: '9999999999'"
                                    })

    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', 'autocomplete': 'off',
                                                               'class': 'w3-input w3-border', 'rows': '3'}))
    amount = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Amount', 'autocomplete': 'off',
                                                             'class': 'w3-input w3-border',
                                                             'style': 'margin: 27px 8px 0px 7px; width:98%'}))
    boli_date = forms.DateField(initial=datetime.today().date(),
                                widget=forms.DateInput(attrs={'autocomplete': 'off',
                                                              'class': 'w3-input w3-border datepicker'})
    )


class BoliRequestForm(forms.Form):
    title = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'w3-input w3-border',
                                                              'style': 'height: 45px; margin-left:6px; width:98%'}),
                                   queryset=BoliChoice.objects.all(), required=True)
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', max_length=10,
                                    widget=forms.NumberInput(
                                        attrs={'placeholder': 'Phone Number',
                                               'autocomplete': 'off', 'class': 'w3-input w3-border',
                                               'onkeyup': "javascript:get_description();"}),
                                    error_messages={
                                        'required': "Phone number must be entered in the format: '9999999999'"
                                    })

    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', 'autocomplete': 'off',
                                                               'class': 'w3-input w3-border', 'rows': '3'}))
    amount = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Amount', 'autocomplete': 'off',
                                                             'class': 'w3-input w3-border',
                                                             'style': 'margin: 27px 8px 0px 7px; width:98%'}))
    boli_date = forms.DateField(initial=datetime.today().date(),
                                widget=forms.DateInput(attrs={'autocomplete': 'off',
                                                              'class': 'w3-input w3-border datepicker'})
    )


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Name', 'autocomplete': 'off', 'class': 'w3-input w3-border'}
    ))

    contact_email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'autocomplete': 'off', 'class': 'w3-input w3-border'}
    ))

    message = forms.CharField(
        required=True, max_length="300",
        widget=forms.Textarea(attrs={
            'placeholder': 'Message', 'autocomplete': 'off',
            'class': 'w3-input w3-border', 'rows': '2'
        })
    )


class PaymentForm(forms.Form):

    payment_mode = forms.ChoiceField(choices=PAYMENT_MODES, widget=forms.Select(
        attrs={'class': 'w3-input w3-border', 'style': "height: 40px;", "onchange": "payment_md();"}
    ))

    partial_payment = forms.CharField(required=False, widget=forms.NumberInput(
        attrs={'placeholder': 'Paid Amount', 'autocomplete': 'off', 'class': 'w3-input w3-border',
               'style': 'display:none', "onkeyup": "payment_cal();"}
    ))

    id_details = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Transaction Id / Cheque Number', 'autocomplete': 'off', 'class': 'w3-input w3-border',
               'style': 'display:none'}
    ))

    send_to = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your email address', 'autocomplete': 'off', 'class': 'w3-input w3-border'}
    ))

    remark = forms.CharField(
        required=False, max_length="200",
        widget=forms.Textarea(attrs={
            'placeholder': 'Remark', 'autocomplete': 'off',
            'class': 'w3-input w3-border', 'rows': '1'
        })
    )

    pan_card = forms.CharField(
        required=False, max_length="10",
        widget=forms.Textarea(attrs={
            'placeholder': 'PAN card', 'autocomplete': 'off',
            'class': 'w3-input w3-border', 'rows': '1'
        })
    )