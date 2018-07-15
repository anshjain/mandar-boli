# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.list import ListView

from events.models import Events


class EventListView(ListView):
    model = Events
    context_object_name = 'event'
    template_name = 'event_details.html'

    def get_queryset(self):
        """
        Return 1 random mandir records registered.
        """
        # import ipdb; ipdb.set_trace()
        event_id = self.kwargs['event_id']
        return self.model.objects.filter(id=event_id, status=True).first()