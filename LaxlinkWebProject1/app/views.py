"""
Definition of views.
"""

from datetime import datetime
from django import forms
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from app.forms import CreateTeamInfoForm, SnippetForm, TeamForm, RegistrationForm, FindTeamForm, QueryTeamInfoForm
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
                  'app/team/createteaminfo.html', 
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
                  'app/team/createteaminfo.html', 
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
                   'app/team/createteaminfo.html',
                   {
                        'title': 'TeamInfo',
                        'form' : tempForm
                       })
def gameschedule(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/team/gameschedule.html',
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

def filter_not_none(filter):
    if filter != "None":
        return Q(filter=filter)
    else:
        return Q()

def queryteam(request):
    template_name = 'app/team/teamquery.html'
    #form = FindTeamForm()
    teamObject=TeamData()
    form = QueryTeamInfoForm()
  
    if request.method == 'GET':
        #form = QueryTeamInfoForm()
        return render(request,'app/team/teamquery.html' , {'form':form, 'teamInfo': teamObject} )
    elif request.method == 'POST':
        
        q_object = Q()  
        #if request.POST['team_filters']:
        if request.POST.get('team_filters', False):
            #Build value list for representation in displayed user form
            # If the value is 'None' send the entire list back otherwise
            # build a form choicefield composed of Reset and dropdown value
            #Build the Q list for team lookaup as we go
            if (request.POST['teamState'] != "Any"):
                stateasDict = (
                    (request.POST['teamState']),
                    ("Any"),
                 )
                form.choiceTeamState = forms.ChoiceField(choices = stateasDict)
                q_object.add(Q(state = request.POST['teamState']),Q.AND)

            if (request.POST['teamConference'] != 'Any'):
                confasDict =(
                    (request.POST['teamConference']),
                    ("Any"),
                 )
                form.choiceFormConf = forms.ChoiceField(choices = confasDict)
                q_object.add(Q(conference = request.POST['teamConference']),Q.AND)


            team_list = TeamData.objects.filter(q_object)
            #build the team list for display
            teamnamesasList = []
            if team_list.count() > 0:
                for team in team_list:
                    #tempName = 
                    teamnamesasList.append(team.name)
                form.choiceTeamNames = forms.ChoiceField(choices = teamnamesasList)



            #now that filter are rebuilt for display in the template, populate the
            #appropriate teams in a list
            #Build filter chain and discard any None. All fields are required at team creation
            # the none is a human input to disregard that particular filter on a search
            #q_object = Q()                                    
            #if request.POST['teamState'] != "Any":
            #    q_object.add(Q(state = request.POST['teamState']),Q.AND)
            #if request.POST['teamConference'] != "Any":
            #    q_object.add(Q(conference = request.POST['teamConference']),Q.AND)
            #if request.POST['teamgender'] != "None":
            #    q_object.add(Q(gender = request.POST['teamGender']),Q.AND)

            
            
            #if team_list.count() == 1:
                
                # display the only matching team entry and try to 
                # pass it down to the reuest post for select team 
            #    team = team_list[0]
                #request.POST['select_team'] = "internal_selection"
                #request.POST["dropTeamName"] = team.name6    
                #stateasDict = (
                #    (request.POST['teamState']),
                #    ("Any"),
                #)
                #form.choiceTeamState = forms.ChoiceField(choices = stateasDict)
                #confasDict =(
                #    (request.POST['teamConference']),
                #    ("Any"),
                # )
                #form.choiceFormConf = forms.ChoiceField(choices = confasDict)

           #     nameasDict = (
           #        (team_list[0].name),
           #        ("Any"),
           #     )
           #     form.choiceTeamNames = forms.ChoiceField(choices = nameasDict)

           #     return render(request,'app/team/teamquery.html' , {'form':form, 'teamInfo': teamObject})
            #else:
                #more than one matching in database return team list
                #lets capture all of the not None filters sent and return the 
                #list of teams that match the filters provided. It will be important to use the 
                #captured filters in the final lookup to grab team data from the
                # database

            #     nameasDict = (
            #       (team_list[0].name),
            #       ("Any"),
            #    )

            #    form.choiceTeamNames = forms.ChoiceField(choices = nameasDict)







             #   return render(request,'app/team/teamquery.html' , {'form':form, 'teamInfo': teamObject})

            
            
        if request.POST.get('select_team', False):
            #if request.POST['select_team']:
            # lookup team and display team data
            #team2 = TeamData.objects.get(name = 'Team2')
            #team_filter = TeamData.objects.filter(name = 'Team3')
            #coach2=team2.name
            teamObject = TeamData.objects.get(name = (request.POST['dropTeamName']))
            form = QueryTeamInfoForm()
                
            return render(request,'app/team/teamquery.html' , {'form':form, 'teamInfo': teamObject} )


    return render(request,'app/team/teamquery.html' , {'form':form } )
