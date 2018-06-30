# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
import simplejson as json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from account.models import Account

from mandir.models import Record
from mandir.forms import SearchForm, EntryForm


class RecordListView(ListView):
    model = Record
    form_class = SearchForm
    context_object_name = 'records'
    template_name = 'records.html'

    def get_mandir_info(self):
        """
        Get the mandir info.
        """
        user = self.request.user
        if hasattr(user, 'userprofile'):
            profile = user.userprofile
            return profile.mandir if hasattr(profile, 'mandir') else None

    def get_context_data(self, *args, **kwargs):
        context = super(RecordListView, self).get_context_data(*args, **kwargs)
        context.update({'form': self.form_class(), 'mandir': self.get_mandir_info()})
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)

        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            return self.model.objects.filter(account__phone_number__icontains=phone_number)

        # Default data will be displayed for two hours only after creation.
        mandir = self.get_mandir_info()
        time_threshold = datetime.now() - timedelta(hours=2)
        return self.model.objects.filter(created__date=datetime.today(), created__gt=time_threshold, mandir=mandir)


@method_decorator(login_required, name='dispatch')
class EntryCreateView(LoginRequiredMixin, FormView):
    form_class = EntryForm
    model = Record
    template_name = 'entry.html'
    success_url = '/add/#entry'

    def get_context_data(self, *args, **kwargs):
        context = super(EntryCreateView, self).get_context_data(*args, **kwargs)

        # Mandir object into the context
        context['mandir'] = self.request.user.userprofile.mandir
        return context

    def form_valid(self, form):
        # check account present with phone number or not.
        account, created = Account.objects.get_or_create(
            phone_number=form.cleaned_data['phone_number'],
        )
        if created:
            account.description = form.cleaned_data['description']
            account.save()
        # hard code as of now
        mandir = self.request.user.userprofile.mandir

        _, record_created = self.model.objects.get_or_create(
            mandir=mandir,
            account=account,
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            amount=form.cleaned_data['amount'],
            boli_date=datetime.now()
        )
        if record_created:
            messages.success(self.request, "Record added successfully !!")

        return super(EntryCreateView, self).form_valid(form)


def ajax_single_account(request):
    '''gets single item'''
    if not request.is_ajax():
        return HttpResponse(json.dumps({'result': False}))

    # get slug from data
    phone_number = request.GET.get('phone_number', None)

    # get item from slug
    account = get_object_or_404(Account, phone_number=phone_number)
    return HttpResponse(json.dumps(
        {
            'result': True,
            'description': account.description,
        }))