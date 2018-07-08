# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from mandir.models import BoliChoice


PAYMENT_MODES = (
    ('Online', 'Online'),
    ('Check', 'Check'),
    ('Cash', 'Cash'),
)

class SearchForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'autocomplete': 'off'}))


class EntryForm(forms.Form):
    title = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'w3-input w3-border',
                                                              'style': 'height: 40px;'}),
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
                                                               'class': 'w3-input w3-border', 'rows': '4'}))
    amount = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Amount', 'autocomplete': 'off',
                                                             'class': 'w3-input w3-border',
                                                             'style': 'margin: 18px 6px 0px 6px'}))


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
    payment_mode = forms.ChoiceField(required=True, choices=PAYMENT_MODES, widget=forms.Select(
        attrs={'class': 'w3-input w3-border', 'style': "height: 40px;", "onchange": "payment_md();"}
    ))

    id_details = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Transaction Id / Check Number', 'autocomplete': 'off', 'class': 'w3-input w3-border'}
    ))

    send_to = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Enter email address', 'autocomplete': 'off', 'class': 'w3-input w3-border'}
    ))
