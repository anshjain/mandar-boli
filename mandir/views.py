# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from account.models import Account

from mandir.models import Record, Mandir
from mandir.forms import SearchForm, EntryForm


class RecordListView(ListView):
    model = Record
    form_class = SearchForm
    context_object_name = 'records'
    template_name = 'records.html'

    def get_context_data(self, *args, **kwargs):
        # Just include the form
        context = super(RecordListView, self).get_context_data(*args, **kwargs)
        context['form'] = self.form_class()
        # Mandir object into the context
        context['mandir'] = Mandir.objects.all()[0]
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return self.model.objects.filter(account__phone_number__icontains=form.cleaned_data['phone_number'])
        return self.model.objects.filter(created__date=datetime.today())


class EntryCreateView(FormView):
    form_class = EntryForm
    model = Record
    template_name = 'entry.html'
    success_url = '/'

    def form_valid(self, form):
        # check account present with phone number or not.
        account, created = Account.objects.get_or_create(
            phone_number=form.cleaned_data['phone_number'],
        )
        if created:
            account.description = form.cleaned_data['description']
            account.save()
        # hard code as of now
        mandir = Mandir.objects.all().first()

        self.model(
            mandir=mandir,
            account=account,
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            amount=form.cleaned_data['amount'],
            boli_date=datetime.now()
        ).save()
        return super(EntryCreateView, self).form_valid(form)