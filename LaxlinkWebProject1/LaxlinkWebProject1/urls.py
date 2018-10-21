"""
Definition of urls for LaxlinkWebProject1.
"""

from datetime import datetime
from django.urls import path
import site
from django.conf.urls import url, include
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
admin.site.register(app.models.WinLossRecord)

urlpatterns = [
    # Examples:
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    path('admin', admin.site.urls),
    path('teamquery', app.views.queryteam),
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'WebPage1$', app.views.WebPage1, name='WebPage1'),
    url(r'snippet$', app.views.snippet_detail, name='snippet_detail'),
    url(r'teamsn$', app.views.teamSnippet_detail, name='teamSnippet_detail'),
    url(r'createteaminfo', app.views.createteaminfo, name='createteaminfo'),
    url(r'gameschedule', app.views.gameschedule, name='gameschedule'),
    url(r'reg_form', app.views.register, name='reg_form'),
    url('thankyouregister',app.views.thankyouregister),
    url('failregister',app.views.failregistration),
 

     
    url(r'^login/$',
        #django.contrib.auth.views.login,
        django.contrib.auth.login,
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
        #django.contrib.auth.views.logout,
        django.contrib.auth.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

   
]
