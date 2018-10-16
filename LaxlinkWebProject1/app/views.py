"""
Definition of views.
"""

from django.shortcuts import render, render_to_response, redirect
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
from app.forms import CreateTeamInfoForm, SnippetForm, TeamForm, RegistrationForm
from app.models import *
from django.contrib.auth.forms import UserCreationForm

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

class GameRecord:
    hometeamname=''
    awayteamname=''
    gamedate=''
    verified=''
    homescore=''
    awayscore=''

def WebPage1(request):
    """Renders the WebPage1 page."""
    #assert isinstance(request, HttpRequest)
    #return render(
    #    request,
    #   'app/WebPage1.html',
    #    {
    #        'title':'About',
    #        'message':'Your application description page.',
    #        'year':datetime.now().year,
    #    }
    #)
    #games = GameInfo.objects.filter(away_team = 2)


    teamrequested = 2
    games_set = GameInfo.objects.filter(Away_team = teamrequested)| GameInfo.objects.filter(Home_team = teamrequested)
    gamedatalist = []


    for i in games_set:
        tempGameRecord = GameRecord()
        tempGameRecord.awayteamname=i.Away_team.getName()
        tempGameRecord.awayscore=i.away_score
        tempGameRecord.hometeamname=i.Home_team.getName()
        tempGameRecord.homescore=i.home_score
        tempGameRecord.gamedate = str(i.date)

        if i.game_validated:
            tempGameRecord.verified='Score Validated'
        else:
            tempGameRecord.verified='Unverified'

        #gamedatalist.append(str(gamedate)+ " "+ awayteamname + " at " + hometeamname + " " + verified)
        gamedatalist.append(tempGameRecord)


    return render_to_response('app/WebPage1.html', {'teamname': 'PlaceHolder', 'schedule': 'YES','games':gamedatalist})


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
def gameschedule(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/gameschedule.html',
        {
            'title':'Game Schedule',
            'year':datetime.now().year,
        }
    )

#def teamschedule(response):
#    return render(response.
#                  'app/teamschedule.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app/accounts/thankyouregister.html')
        else:
            return redirect('app/accounts/failregister.html')
    else:
        form = RegistrationForm()

        args = {'form':form}
        return render(request, 'app/accounts/reg_form.html', args)

def thankyouregister(request):
    return render(request, 'app/accounts/thankyouregister.html')

def failregistration(request):
    return render(request, 'app/accounts/failregister.html')
