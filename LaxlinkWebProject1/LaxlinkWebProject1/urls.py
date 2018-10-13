"""
Definition of urls for LaxlinkWebProject1.
"""

from datetime import datetime
import site
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()
admin.site.register(app.models.Snippet)
admin.site.register(app.models.TeamData)
admin.site.register(app.models.GameInfo)

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'WebPage1$', app.views.WebPage1, name='WebPage1'),
    url(r'snippet$', app.views.snippet_detail, name='snippet_detail'),
    url(r'teamsn$', app.views.teamSnippet_detail, name='teamSnippet_detail'),
    url(r'createteaminfo', app.views.createteaminfo, name='createteaminfo'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
