"""
Definition of models.
"""

from django.db import models
from django.utils import datetime_safe


GAMETYPES = (
    ('S', 'Scrimmage'),
    ('R', 'Regular Season'),
    ('P', 'Playoff'),
    ('C', 'Championship'),
    ('T', 'Tournament'),
)

DIVISIONS = (
    ('HSD1', 'High School D1'),
    ('HSD2', 'High School D2'),
    ('HSJV', 'High School JV'),
    ('NCAAD1', 'NCAA Division 1'),
    ('NCAAD2', 'NCAA Division 2'),
    ('NCAAD3', 'NCAA Division 3'),
) 

STATES = (
    ('TX', 'Texas'),
    ('LA', 'Lousiana'),
    ('OK', 'Oklahoma')
)

CONFERENCE = (
    ('NONE', 'No Conference Specified'),
    ('TGHSLL-N', 'Texas (TGHSLL) North Conference'),
    ('TGHSLL-C', 'Texas (TGHSLL) Central Conference'),
    ('TGHSLL-S', 'Texas (TGHSLL) South Conference'),
)

class Snippet(models.Model):
    name = models.CharField(max_length=100)
    body = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# Create your models here.

class TeamData(models.Model):
    name = models.CharField("Team Name", max_length=100)
    coach = models.CharField(max_length=100, default="Unknown")
    contact_name = models.CharField(max_length=100, default="USER")
    coach_email = models.EmailField(default="unknown")
    state =  models.CharField(max_length=2, choices=STATES)
    conference = models.CharField(max_length=8, choices=CONFERENCE, default="NONE")
    division = models.CharField(max_length=6, choices=DIVISIONS)

    def __str__(self):
        return self.state + "-" + self.conference+ "-" + self.division + "-" + self.name 
    
    def getName(self):
        return self.name

class GameInfo(models.Model): 
    #TODO: Add field for the individuals who validated score 2-3 mapping to a USER
    #home_team = models.ManyToManyField(TeamData, related_name="home_team")
    Home_team = models.ForeignKey(TeamData, default='0', related_name="home_team")
    home_score = models.IntegerField(default=0)
    #away_team = models.ManyToManyField(TeamData, related_name="away_team")
    Away_team = models.ForeignKey(TeamData, default="0", related_name="away_team")
    away_score = models.IntegerField(default=0)
    date = models.DateField(default=datetime_safe.date.today)
    location = models.CharField(max_length = 100, default="Home Team Field")
    game_type = models.CharField(max_length=1, choices=GAMETYPES)
    game_validated = models.BooleanField(default=False)
    #key to attach to TeamSomehow
    def __str__(self):
    #    return self.away_team.__str__ + "at" + self.home_team.__str__
        return str(self.id)
    
    



