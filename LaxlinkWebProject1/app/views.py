"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.forms import TeamInfoForm, SnippetForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def WebPage1(request):
    """Renders the WebPage1 page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/WebPage1.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def createteaminfo(request):
    'Renders the create TeamInfo page'
   
    if request.method == 'POST':
        #createing a new form
        teamform = TeamInfoForm(request.POST)
        if teamform.is_valid():
            name = teamform.cleaned_data['name']

            print(name)

    teamform = TeamInfoForm()
    return render( request, 
                  'app/teaminfo.html', 
                  {
                      'title': 'TeamInfo',
                      'form' : teamform})

def snippet_detail(request):
    if request.method == 'POST':
        #creating a new form
        teamform = SnippetForm(request.POST)
        if teamform.is_valid():
            teamform.save()
          

    teamform = SnippetForm()
    return render( request, 
                  'app/teaminfo.html', 
                  {
                      'title': 'TeamInfo',
                      'form' : teamform
                  })
