"""
Definition of views.
"""

from datetime import datetime
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from app.forms import CreateTeamInfoForm, SnippetForm, TeamForm, RegistrationForm, FindTeamForm, QueryTeamInfoForm
from app.models import *


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
    verified='-'
    homescore=''
    awayscore=''
    bgColor=''

    def __init_(self):
        hometeamname='home'
        awayteamname='away'
        gamedate='date'
        verified='-'
        homescore='-'
        awayscore='-'
        bgColor=''


class RankRecord:
    teamname=''
    wincount=0
    losscount=0
    tiecount=0
    gamesbehind=0
    teamrating=0
    # used to calculate straight up rankings based on 
    # win loss and games behind
    winvalue=2
    losevalue=0
    gamesbehindvalue=1
    def __init__(self):
        teamname=''
        wincount=0
        losscount=0
        tiecount=0
        gamesbehind=0
        teamrating=0


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

    # Use the session information to choose the team to display
    # the correct team information 

    q_object = Q() 
    if (request.session['teamState']!= "Any"):
        q_object.add(Q(state = request.session['teamState']),Q.AND)
    if (request.session['teamConference']!= "Any"):
        q_object.add(Q(conference = request.session['teamConference']),Q.AND)
    if (request.session['dropTeamName']!= "Any"):
        q_object.add(Q( name = request.session['dropTeamName']),Q.AND)

    team_list = TeamData.objects.filter(q_object)

    teamrequested = team_list[0]
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

        #now add a flag so that background for games can be colored in html side
        # first figure out who won or lost
        winner = ''
        if (i.away_score < i.home_score):
            winner = tempGameRecord.hometeamname
        else:
            winner = tempGameRecord.awayteamname

        tempGameRecord.bgColor='ffffff'
        if (winner==teamrequested.name):
            # set the back ground color to green
            tempGameRecord.bgColor='33cc3c'


        #gamedatalist.append(str(gamedate)+ " "+ awayteamname + " at " + hometeamname + " " + verified)
        gamedatalist.append(tempGameRecord)


    return render_to_response('app/WebPage1.html', {'teamname': 'PlaceHolder', 'schedule': 'YES','display_record':'YES', 'games': gamedatalist })


def createteaminfo(request):
    'Renders the createTeamInfo page, stores user provided data in db'
   
    if request.method == 'POST':
        #creating a new form
        teamform = CreateTeamInfoForm(request.POST)
        if teamform.is_valid():
            name = teamform.cleaned_data['name']
            state = teamform.cleaned_data['state']
            division = teamform.cleaned_data['division']
            conference = teamform.cleaned_data['conference']
            
            #Check existing database for duplicate entries
            
            teamObjectset = TeamData.objects.filter(name = name, state=state, division=division, conference=conference)

            if not teamObjectset:
                #New entry for database go ahead and save it
                # and set up win loss record dB entry
                teamform.save()
                teamObject = TeamData.objects.get(name = name, state=state, division=division, conference=conference)
                temprecord=WinLossRecord()
                temprecord.teamkey = teamObject
                temprecord.save()
            else:
                #This is a duplicate entry do NOT save and screw up database
                return

            
    else:
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
    return redirect('app/accounts/failregister.html')
    #if request.method == 'POST':
    #    #list out the schedule as is known
    #    # will have to find all games for the team in question
    #    # display teams as home and away
    #    # put score if known - 
    #    # bonus - indicate win versus loss
   
    ##assert isinstance(request, HttpRequest)
    #return render(
    #    request,
    #    'app/team/gameschedule.html',
    #    {
    #        'title':'Game Schedule',
    #        'year':datetime.now().year,
    #    }
    #)

#def teamschedule(response):
#    return render(response.
#                  'app/teamschedule.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():         
            temp=form.save()   
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


def queryteam(request):
    template_name = 'app/team/teamquery.html'
    #form = FindTeamForm()
    teamObject=TeamData()
    form = QueryTeamInfoForm()
  
    if request.method == 'GET':
        # disable buttons for team manipulation since no team is present
        form.renderButtons = False
        request.session['teamStateSelected'] =''
        request.session['teamConferenceSelected'] =''
        request.session['teamDivisionSelected'] =''
        request.session['teamNameSelected'] =''

        return render(request,'app/team/teamquery.html' , {'form':form, 'teamInfo': teamObject} )
    elif request.method == 'POST':
        
        q_object = Q()  

        if (request.POST.get('team_filters', False) or (request.POST.get('select_team', False))):
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

                #now store off session information for later lookups
                request.session['teamStateDict'] = stateasDict
                request.session['teamStateSelected'] = request.POST['teamState']
            else:
                request.session['teamState'] =''
                request.session['teamStateSelected'] =''
                #del request.session['teamState']
                #request.session.modified = True

            if (request.POST['teamConference'] != 'Any'):
                confasDict =(
                    (request.POST['teamConference']),
                    ("Any"),
                 )
                form.choiceTeamConf = forms.ChoiceField(choices = confasDict)
                q_object.add(Q(conference = request.POST['teamConference']),Q.AND)
                #request.session['teamConference'] = request.POST['teamConference']

                #now store off session information for later lookups
                request.session['teamConferenceDict'] = confasDict
                request.session['teamConferenceSelected'] = request.POST['teamConference']
            else:
                request.session['teamConference'] =''
                request.session['teamConferenceSelected'] =''
                #del request.session['teamConference']
                #request.session.modified = True

            if (request.POST['teamDivision'] != 'Any'):
                divisionsasDict =(
                    (request.POST['teamDivision']),
                    ("Any"),
                 )
                form.choiceTeamDivision = forms.ChoiceField(choices = divisionsasDict)
                q_object.add(Q(division = request.POST['teamDivision']),Q.AND)
                
                #now store off session information for later lookups
                request.session['teamDivisionDict'] = divisionsasDict
                request.session['teamDivisionSelected'] = request.POST['teamDivision']
            else:
                request.session['teamDivision'] =''
                request.session['teamDivisionSelected'] =''
                #del request.session['teamDivision']
                #request.session.modified = True

            team_list = TeamData.objects.filter(q_object)

            #build the team list for display
            teamnamesasList = []
            if team_list.count() > 0:
                for team in team_list:
                    #tempName = 
                    teamnamesasList.append(team.name)
                teamnamesasList.sort()
                form.choiceTeamNames = forms.ChoiceField(choices = teamnamesasList)
            
            
        if request.POST.get('select_team', False):
            # This means that a team has been selected from the dropdown list
            # and that information needs to be displayed
            # there a separate parts for display
            # - The general team info
            # - The team schedule
            # - the current ranking of the team  by division, region, state

            # Disable form buttons in case of error processing
            form.renderButtons = False

            # To get here we need to have been given a team name so build a q list 
            # of saved of values to select the entry
            
            q_object = Q()
            if request.session['teamDivisionSelected'] != '':
                q_object.add(Q(division = request.session['teamDivisionSelected']),Q.AND)
            if request.session['teamConferenceSelected'] != '':
                q_object.add(Q(conference = request.session['teamConferenceSelected']),Q.AND)
            if request.session['teamStateSelected'] != '':
                q_object.add(Q(state = request.session['teamStateSelected']),Q.AND)
            q_object.add(Q(name = request.POST['dropTeamName']),Q.AND)

            #team_list = TeamData.objects.filter(q_object)
            try:
                teamObject = TeamData.objects.get(q_object)
                #session.teamobject = teamObject
                form.renderButtons = True
            except:
               # this happens when the selection criteria allows multiple hits in the database
               # send a response to the user that this occured and to narrow criteria
               # TODO: THIS
               # TODO maybe return back all options

               #lets fill out a teamObject with data defining what happened
               teamObject.name = "Search Failed! -  Multiple Entries Found for " + request.POST['dropTeamName'] +" Use additional filters to narrow search"
               #raise ValueError(" Need more specific filters added - No specific team was found")
            
            #TODO: NEED to verify that this is a unique entry

            #request.session['dropTeamName'] = request.POST['dropTeamName']
            request.session['teamNameSelected'] = request.POST['dropTeamName']
            # we found a team that matches search criteria, setup
            # object return values so that new options can be rendered on the 
            # return screen and provide a means to interact with it
            # the idea here is to set return values for buttons and the
            # functions available will vary according to the type of user
            # general/manager/curator/etc
            #form.renderButtons = True
                
            return render(request,'app/team/teamquery.html' , {'form':form, 'teamInfo': teamObject} )

        if request.POST.get('team_actions', False):
            #  This section deals with the management of team info display
            # functions based around the buttons that return
            # name="team_actions" value="listSchedule"  for example
            gamedatalist = []
            q_object=Q()
            wins=0
            if request.POST['team_actions'] == 'listSchedule':
                # Build a Q object with all of the data that has been captured thus far
                q_object.add(Q(Away_team__name = request.session['teamNameSelected']),Q.OR)
                q_object.add(Q(Home_team__name = request.session['teamNameSelected']),Q.OR)
#TODO: Add to query to only take current season or selected season into account
                games_set = GameInfo.objects.filter(q_object)

                for i in games_set:
                    tempGameRecord = GameRecord()
                    tempGameRecord.awayteamname=i.Away_team.name
                    tempGameRecord.awayscore=i.away_score
                    tempGameRecord.hometeamname=i.Home_team.name
                    tempGameRecord.homescore=i.home_score
                    tempGameRecord.gamedate = str(i.date)

                    if i.game_validated:
                        tempGameRecord.verified='V'
                    else:
                        tempGameRecord.verified='-'

                    # now add a flag so that background for games can be colored in html side
                    # first figure out who won or lost
                    winner = ''
                    if (i.away_score < i.home_score):
                        winner = tempGameRecord.hometeamname
                    else:
                        winner = tempGameRecord.awayteamname

                    tempGameRecord.bgColor='ffffff'
                    if (winner==request.session['teamNameSelected']):
                        # set the back ground color to green
                        tempGameRecord.bgColor='33cc3c'
                        wins = wins+1
                    
                    gamedatalist.append(tempGameRecord)

                #form.choiceTeamDivision = request.session['teamDivision'] 
                form.choiceTeamDivision = forms.ChoiceField(choices = (request.session['teamDivisionDict']))
                form.choiceTeamState = forms.ChoiceField(choices = (request.session['teamStateDict']))
                form.choiceTeamConf = forms.ChoiceField(choices = (request.session['teamConferenceDict']))

                q_object = Q()
                q_object.add(Q(name = request.session['teamNameSelected']),Q.AND)
                if request.session['teamDivisionSelected'] != '':
                    q_object.add(Q(division = request.session['teamDivisionSelected']),Q.AND)
                if request.session['teamConferenceSelected'] != '':
                    q_object.add(Q(conference = request.session['teamConferenceSelected']),Q.AND)
                if request.session['teamStateSelected'] != '':
                    q_object.add(Q(state = request.session['teamStateSelected']),Q.AND)
              
                teamObject = TeamData.objects.get(q_object)

                #Turn the buttons back on
                form.renderButtons = True
                losses = ((games_set.count())-wins)
            

                return render(request,'app/team/teamquery.html' , {'form':form, 
                                                               'schedule': 'YES', 
                                                               'games': gamedatalist, 
                                                               'teamInfo': teamObject, 
                                                               'wins': wins,
                                                               'losses': losses} )
            
            if request.POST['team_actions'] == 'listLeagueRanking':
                rankdatalist = []
                rankdatalist = RankTeams(request)
                form.renderButtons = True
                q_object = Q()
                if request.session['teamDivisionSelected'] != '':
                    q_object.add(Q(division = request.session['teamDivisionSelected']),Q.AND)
                if request.session['teamConferenceSelected'] != '':
                    q_object.add(Q(conference = request.session['teamConferenceSelected']),Q.AND)
                if request.session['teamStateSelected'] != '':
                    q_object.add(Q(state = request.session['teamStateSelected']),Q.AND)
                q_object.add(Q(name = request.session['teamNameSelected']),Q.AND)
                teamObject = TeamData.objects.get(q_object)

                return render(request,'app/team/teamquery.html' , {'form':form, 
                                                                   'teamInfo': teamObject, 
                                                                   'rankedlist': rankdatalist,
                                                                   'basicranking': 'YES'} )

        return render(request,'app/team/teamquery.html' , {'form':form, 'teamInfo': teamObject} )

def logout_view(request):
    logout(request)
    return redirect('app/accounts/thankyouregister.html')

def login_view(request):
    login(request)
    return render(request, 'app/login.html')

def RankTeams(request):
    # This is used to build a list of all teams sorted by wins
    # this will handle the sorting determined by session info and
    # will return a list of games


    # Build a Q object with all of the data that can be inferred from the request
    # and the selected team
    # what we should be able to know
    # The conference the team is in
    # The league that the team is in
    # these values will be used to find all teams that have the same values
    # to determine the league ranking
    q_object = Q()
    team_filter_object = Q()
    if request.session['teamDivisionSelected'] != '':
        q_object.add(Q(Away_team__division = request.session['teamDivisionSelected']),Q.AND)
        q_object.add(Q(Home_team__division = request.session['teamDivisionSelected']),Q.AND)
        team_filter_object.add(Q(division = request.session['teamDivisionSelected']),Q.AND)

    if request.session['teamConferenceSelected'] != '':
        q_object.add(Q(Away_team__conference = request.session['teamConferenceSelected']),Q.AND)
        q_object.add(Q(Home_team__conference = request.session['teamConferenceSelected']),Q.AND)
        team_filter_object.add(Q(conference = request.session['teamConferenceSelected']),Q.AND)

#TODO: Add to query to only take current season or selected season into account
    games_set = GameInfo.objects.filter(q_object)
    teams_set = TeamData.objects.filter(team_filter_object)

    rankdatalist = []
    
    #First make a list of all teams in league 
    for team in teams_set:
        teamranknode = RankRecord()
        teamranknode.name = team.name
        #teamranknode.wincount = 0
        #teamranknode.losscount = 0
        #teamranknode.tiecount = 0
        rankdatalist.append(teamranknode)

    # now go through the game list and start marking wins and losses
    # in teamranknode
    for game in games_set:
## TODO: make this work for only verified scores
        #if i.game_validated:
        #    tempGameRecord.verified='V'
        #else:
        #    tempGameRecord.verified='-'
        tempGameRecord = GameRecord()
        tempGameRecord.awayteamname=game.Away_team.name
        tempGameRecord.awayscore=game.away_score
        tempGameRecord.hometeamname=game.Home_team.name
        tempGameRecord.homescore=game.home_score

        # first figure out who won or lost so that the counts can be tallied
        # in the followup loop through teams in league
        winner = ''
        loser = ''
        if (game.away_score < game.home_score):
            winner = tempGameRecord.hometeamname
            loser = tempGameRecord.awayteamname
        else:
            winner = tempGameRecord.awayteamname
            loser = tempGameRecord.hometeamname

        for team in rankdatalist:
            if team.name == winner:
                team.wincount += 1
            if team.name == loser:
                team.losscount +=1
        

    #Teamranklist contains a list of all teams in league and their wins and losses
    # tallied. Now we need to figure out:
    # Maximum number of games played
    # then calculate and populate the number of games behind
    highnumgames=0
    for eachteam in rankdatalist:
        gamesteamplayed = eachteam.wincount + eachteam.losscount + eachteam.tiecount
        if gamesteamplayed > highnumgames:
            highnumgames = gamesteamplayed

    #Now populate the games behind field and calculate the teamrating
    for eachteam in rankdatalist:
        eachteam.gamesbehind = highnumgames-eachteam.losscount-eachteam.wincount-eachteam.tiecount
        eachteam.teamrating = ((eachteam.gamesbehind*eachteam.gamesbehindvalue)+
                               (eachteam.wincount*eachteam.winvalue)+
                               (eachteam.losscount*eachteam.losevalue))


    rankdatalist.sort(key=lambda RankRecord: RankRecord.teamrating, reverse=True)    


    ## Figure out the return value
    return rankdatalist

