"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
from app.forms import CreateTeamInfoForm, SnippetForm, TeamForm

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
    'Renders the createTeamInfo page, stores user provided data in db'
   
    if request.method == 'POST':
        #creating a new form
        teamform = CreateTeamInfoForm(request.POST)
        if teamform.is_valid():
            name = teamform.cleaned_data['name']
            print(name)
            teamform.save()
            

    teamform = CreateTeamInfoForm()
    return render( request, 
                  'app/createteaminfo.html', 
                  {
                      'title': 'TeamInfo',
                      'form' : teamform})

def snippet_detail(request):
    if request.method == 'POST':
        #creating a new form
        teamform = SnippetForm(request.POST)
        if teamform.is_valid():
            #teamform.save()
             print('VALID')

    teamform = SnippetForm()
    return render( request, 
                  'app/createteaminfo.html', 
                  {
                      'title': 'TeamInfo',
                      'form' : teamform
                  })

def teamSnippet_detail(request):
    if request.method == 'POST':
        #creating a new form
        tempForm=TeamForm(request.POST)
        if tempForm.is_valid():
            tempForm.save()
            

    tempForm=TeamForm()
    return render (request,
                   'app/createteaminfo.html',
                   {
                        'title': 'TeamInfo',
                        'form' : tempForm
                       })
    
#def teamschedule(response):
#    return render(response.
#                  'app/teamschedule.html')