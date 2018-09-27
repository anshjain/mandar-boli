# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from itertools import groupby

import simplejson as json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from account.models import Account

from mandir.models import Record, Mandir
from mandir.forms import SearchForm, EntryForm, ContactForm, PaymentForm
# from punyaUday.run import PunyaUdayStack

Month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: "Jun",
              7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}


class HomeView(ListView):
    model = Mandir
    context_object_name = 'mandirs'
    template_name = 'temple_info.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # Mandir object into the context
        if self.request.user.is_authenticated() and not self.request.user.is_superuser:
            context['mandir'] = self.request.user.userprofile.mandir

        return context

    def get_queryset(self):
        """
        Return 1 random mandir records registered.
        """
        return self.model.objects.filter(status=True).order_by('?')[:1]

    def render_to_response(self, context):
        """
        Override based on login user
        """
        if self.request.user.is_superuser:
            return redirect('admin:index')
        elif self.request.user.is_authenticated():
            return redirect('record-list')

        return super(HomeView, self).render_to_response(context)


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
            if hasattr(profile, 'mandir'):
                return profile.mandir
        else:
            return Mandir.objects.filter(status=True, id=1).first()

    def get_context_data(self, *args, **kwargs):
        context = super(RecordListView, self).get_context_data(*args, **kwargs)

        phone_number = self.request.GET.get('phone_number')
        if phone_number and len(phone_number) == 10:
            amt = self.model.objects.filter(account__phone_number__icontains=phone_number,
                                                  paid=False, remaining_amt=0).aggregate(Sum('amount'))
            remaining_amt = self.model.objects.filter(account__phone_number__icontains=phone_number,
                                                      paid=False).aggregate(Sum('remaining_amt'))
            total_amt = amt['amount__sum']
            if remaining_amt['remaining_amt__sum']:
                total_amt += remaining_amt['remaining_amt__sum']

            context.update({'phone_number': phone_number, 'total_amt': total_amt})

        mandir = self.get_mandir_info()
        month_data, month_range = [], ''

        if mandir:
            month_data, month_range = self.get_month_details(mandir)

        context.update({'form': self.form_class(), 'mandir': mandir, 'payment_form': PaymentForm(),
                        'month_data': month_data, 'month_range': month_range})

        return context

    def get_month_details(self, mandir):
        """
        Will return list of grouped by month and count of paid and not paid records..
        """
        records = self.model.objects.filter(mandir=mandir).only('boli_date', 'paid').order_by('boli_date')
        month_data = [[str('Month'), str('Paid'), str('Not Paid')]]
        first_month = str(Month_dict.get(records[0].boli_date.month))

        for k, g in groupby(records, key=lambda i: i.boli_date.month):
            paid = not_paid = 0
            month = str(Month_dict.get(k))
            for x in g:
                paid += 1 if x.paid else 0
                not_paid += 1 if not x.paid else 0
            month_data.append([month, paid, not_paid])

        return month_data, "{}-{}".format(first_month, month)

    def get_queryset(self):
        form = self.form_class(self.request.GET)

        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            if len(phone_number) == 10:
                return self.model.objects.filter(account__phone_number__icontains=phone_number,
                                                 paid=False).order_by('-boli_date')

        # Default data will be displayed for two hours only after creation.
        mandir = self.get_mandir_info()
        time_threshold = datetime.now() - timedelta(hours=2)
        return self.model.objects.filter(boli_date__date=datetime.today(), created__gt=time_threshold,
                                         mandir=mandir, paid=False).order_by('-boli_date')


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
        amount = form.cleaned_data['amount']
        boil_date = form.cleaned_data['boli_date']

        _, record_created = self.model.objects.get_or_create(
            mandir=mandir,
            account=account,
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            amount=amount,
            boli_date=boil_date
        )
        if record_created:
            #send_sms(account.phone_number, amount)
            messages.success(self.request, "Record added successfully !!")

        return super(EntryCreateView, self).form_valid(form)


# def send_sms(phone_number, amount):
#     """
#         Will send an sms to end user.
#     """
#     try:
#         sms_mgs = """ Thats a dummy message !!\nThanks to donate {}/- \n Mandir Committee is very thankful to you.""".format(amount)
#         messages = [("91"+phone_number, sms_mgs)]
#         stack = PunyaUdayStack(messages)
#         stack.start()
#     except Exception:
#         pass


def contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('message', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')

            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }

            content = template.render(context)

            email = EmailMessage(
                "Feedback submitted on Punya Unday Funds", content,
                "Punya Unday Funds", ['jain.scs@gmail.com'],
                headers={'Reply-To': contact_email}
            )

            email.send()
            messages.success(request, "Thank you for contacting us !!")
            return redirect('contact-us')
        else:
            form_class = form
            messages.error(request, "Please provide correct email address !!")

    mandir = request.user.userprofile.mandir if request.user.is_authenticated() else None
    return render(request, 'contact.html', {'form': form_class, 'mandir': mandir})


def payment_complete(request):
    form_class = PaymentForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)
        phone_number = request.POST.get('phone_number')

        if form.is_valid():
            mod_pay = form.cleaned_data.get('payment_mode', '')
            send_to = [form.cleaned_data.get('send_to', '')]
            id_details = form.cleaned_data.get('id_details', '')
            partial_payment = form.cleaned_data.get('partial_payment', 1)

            try:
                # get record info
                record = get_object_or_404(Record, id=request.POST.get('record_id'), paid=False)
                description = record.account.description
                if not description:
                    description = record.description

                name = description.split(',')[0]
                mandir_email = record.mandir.email

                # Email the profile with the
                # contact information
                template = get_template('payment_template.txt')

                payment_detail = ''
                if mod_pay == 'Online':
                    payment_detail = 'Transaction Id: {}'.format(id_details)
                elif mod_pay == 'Check':
                    payment_detail = 'Check Number: {}'.format(id_details)

                # calculate based on partial payment percentage:
                paid_amount = record.amount
                if partial_payment:
                    paid_amount = (record.amount * int(partial_payment)) / 100

                context = {
                    'name': name,
                    'mod_pay': mod_pay,
                    'payment_detail': payment_detail,
                    'amount': paid_amount,
                    'mandir': record.mandir,
                    'remark': form.cleaned_data.get('remark'),
                }

                content = template.render(context)

                send_to.append(mandir_email)
                send_to.extend(settings.ADMIN_EMAILS)

                # update record mark it as paid and store email content as copy in description.
                record.description = content
                record.remaining_amt = record.amount - paid_amount
                if not partial_payment:
                    record.paid = True


                record.transaction_id = id_details if id_details else 'Cash'
                record.payment_date = datetime.now()
                record.save()

                email = EmailMessage(
                    "Thanks for the Payment", content,
                    record.mandir.name, send_to
                )
                email.send()

            except Exception:
                messages.error(request, "There is some error in updating the record, Please contact admin !!")
        else:
            messages.error(request, "There is something wrong, {}". format(form.errors))

    url = reverse('record-list') + "?phone_number={}#record".format(phone_number)
    return HttpResponseRedirect(url)


class AboutView(TemplateView):
    template_name = 'about_us.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)

        # Mandir object into the context
        if self.request.user.is_authenticated():
            context['mandir'] = self.request.user.userprofile.mandir

        return context


def ajax_single_account(request):
    """
    gets single item
    """
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
