"""Boli URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, static

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView


from mandir.views import RecordListView, EntryCreateView, ajax_single_account

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', LoginView.as_view(template_name='login.html'), name="login"),
    url(r'^accounts/logout/$', LogoutView.as_view(template_name='base.html'), name="logout"),
    url(r'^$', RecordListView.as_view(), name='home'),
    url(r'^search/$', RecordListView.as_view(), name='record-list'),
    url(r'^add/$', EntryCreateView.as_view(), name='add-record'),
    url(r'^get/description/$', ajax_single_account, name='des-search'),
    url(r'^about-us/$', TemplateView.as_view(template_name="about_us.html"), name='about'),
    url(r'^contact-us/$', TemplateView.as_view(template_name="contact.html"), name='contact-us'),
] + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

