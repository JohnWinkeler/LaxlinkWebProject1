"""
Definition of models.
"""

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import datetime_safe




GAMETYPES = (
    ('A', 'Any'),
    ('S', 'Scrimmage'),
    ('R', 'Regular Season'),
    ('P', 'Playoff'),
    ('C', 'Championship'),
    ('T', 'Tournament'),
)

DIVISIONS = (
    ('ANY', 'Any'),
    ('HSD1', 'High School D1'),
    ('HSD2', 'High School D2'),
    ('HSJV', 'High School JV'),
    ('NCAAD1', 'NCAA Division 1'),
    ('NCAAD2', 'NCAA Division 2'),
    ('NCAAD3', 'NCAA Division 3'),
) 

STATES = (
    ('ANY', 'Any'),
    ('LA', 'Lousiana'),
    ('OK', 'Oklahoma'),
    ('TX', 'Texas'),
  
)

CONFERENCE = (
    ('ANY', 'Any Conference'),
    ('TGHSLL-N', 'Texas (TGHSLL) North Conference'),
    ('TGHSLL-C', 'Texas (TGHSLL) Central Conference'),
    ('TGHSLL-S', 'Texas (TGHSLL) South Conference'),
)

SEASON = (
    ('FALL','Fall'),
    ('SPRING', 'Spring'),
    ('SUMMER', 'Summer'),
    ('WINTER', 'Winter'),
    ('INDOOR', 'Indoor'),
    ('TRAVEL', 'Travel'),
    ('ANY', 'Any'),
)

GENDER = (
    ('MENS', 'Mens'),
    ('WOMENS', 'Womens'),
    ('MIXED', 'Mixed'),
)

class Snippet(models.Model):
    name = models.CharField(max_length=100)
    body = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# Create your models here.

class TeamData(models.Model):
    name = models.CharField("Team Name", max_length=100, default="")
    coach = models.CharField(max_length=100, default="Unknown")
    contact_name = models.CharField(max_length=100, default="USER")
    coach_email = models.EmailField(default="unknown")
    state =  models.CharField(max_length=2, choices=STATES, default="Unknown")
    conference = models.CharField(max_length=8, choices=CONFERENCE, default="Any")
    division = models.CharField(max_length=6, choices=DIVISIONS, default="Unknown")
    gender = models.CharField(max_length=8, choices=GENDER, default="Mixed")

    powerrating = models.IntegerField(default=0)

    def __str__(self):
        return self.state + "-" + self.conference+ "-" + self.division + "-" + self.name 
    
    def getName(self):
        return self.name

class WinLossRecord(models.Model):
    season = models.CharField(max_length=10, choices=SEASON, default="None")
    wincount = models.IntegerField(default=0)
    losscount = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    teamkey =  models.ForeignKey(TeamData, default='0', related_name="team", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)

class GameInfo(models.Model): 
    #TODO: Add field for the individuals who validated score 2-3 mapping to a USER

    #Teams involved
    Home_team = models.ForeignKey(TeamData, default='0', related_name="home_team", on_delete=models.PROTECT)
    Away_team = models.ForeignKey(TeamData, default="0", related_name="away_team", on_delete=models.PROTECT)

    #Score - Updated  by users
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)


    #Data about each game - values stored at creation time to build a schedule
    date = models.DateField(default=datetime_safe.date.today)
    location = models.CharField(max_length = 100, default="Home Team Field")
    game_type = models.CharField(max_length=1, choices=GAMETYPES)
    game_validated = models.BooleanField(default=False)

    #Link to seasonal record, may reduce the traversal of table to generate stats
    winlosslink_winner =  models.ForeignKey(WinLossRecord, default='0', related_name='winners_record', on_delete=models.PROTECT)
    winlosslink_loser = models.ForeignKey(WinLossRecord, default='0', related_name='loserss_record', on_delete=models.PROTECT)

    #link to ScoreKeepers
    #scorekeeper1 = models.ForeignKey(User, default=0, related_name='scorekeeper1')
    #scorekeeper2 = models.ForeignKey(User, default=0, related_name='scorekeeper2')
    def __str__(self):
    #    return self.away_team.__str__ + "at" + self.home_team.__str__
        return str(self.id)
    


class Profile(models.Model):
    ROLE_CHOICES = (
        ('CURATOR','Curator'),
        ('REGIONAL_MANAGER','Regional Manager'),
        ('TEAM_MANAGER', 'Team Manager'),
        ('GENERAL_USER', 'General User')
        )



    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, 
                            choices=ROLE_CHOICES,
                            blank=True,
                            default='GENERAL_USER')
    favState = models.CharField(max_length=2, 
                                choices=STATES, 
                                default="Any")

    favDivision = models.CharField(max_length=6, 
                                   choices=DIVISIONS, 
                                   default="Any")
    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)    

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    instance.profile.save()


