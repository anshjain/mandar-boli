# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from mandir.models import BoliChoice, Mandir


class SearchForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'autocomplete': 'off'}))
    mandir = forms.ModelChoiceField(widget=forms.Select(
        attrs={
            'class': 'w3-input w3-border',
            'style': 'width: 20%; float: right; margin: 3px; height: 38px;'
        }), queryset=Mandir.objects.all(), required=True)


class EntryForm(forms.Form):
    title = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'w3-input w3-border',
                                                              'style': 'height: 40px;'}),
                                   queryset=BoliChoice.objects.all(),
                                   required=True)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number',
                                                                 'autocomplete': 'off', 'class': 'w3-input w3-border'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'description', 'autocomplete': 'off',
                                                               'class': 'w3-input w3-border', 'rows': '3'}))
    amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'amount', 'autocomplete': 'off',
                                                           'class': 'w3-input w3-border',
                                                           'style': 'margin: 18px 6px 0px 6px'}))
