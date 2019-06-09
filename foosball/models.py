from __future__ import unicode_literals
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.loader import render_to_string

class Profile(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name="own")
    bio           = models.CharField(max_length=200, null=True, blank=True)
    picture 	  = models.FileField(upload_to="images", default='images/anonymous.png', blank=True)
    update_time   = models.DateTimeField(auto_now=True)
    content_type  = models.CharField(max_length=50)
    following     = models.ManyToManyField(User, related_name="follower")
    total_scores  = models.IntegerField()

class RoomEntry(models.Model):
	player = models.ManyToManyField(User, related_name="room")
	player_num  = models.IntegerField(default=0)
	ROOM_STATUS = (
		( "s1", "room available" ), 
		( "s2", "room full" ),
		( "s3", "ready" ),
		( "s4", "in game" )
		)
	status = models.CharField(max_length=2, choices=ROOM_STATUS, default= "s1" )
	owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="my_room")

class WaitUserEntry(models.Model):
	"""docstring for WaitUserEntry"""	
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="apply_info")
	room = models.ForeignKey(RoomEntry,on_delete=models.CASCADE,related_name="waitlist")
	create_time = models.DateTimeField(auto_now=True)

class GameStateEntry(models.Model):
	game_room = models.OneToOneField(RoomEntry, on_delete=models.CASCADE, related_name= "game_state" )
	score1 = models.IntegerField()
	score2 = models.IntegerField()
	ball_init_angle_index = models.IntegerField()


class GameProfileEntry(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_info")
	number = models.IntegerField(default=0)
	team = models.IntegerField(default=1)
	score = models.IntegerField(default=0)
	status = models.BooleanField(default=False)
	game_room = models.ForeignKey(RoomEntry, on_delete=models.SET_NULL, null=True, related_name= "players_info")
	valid = models.BooleanField(default=False)
	guest = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, related_name="guest_game_info")
	start_time = models.DateTimeField(blank=True, null=True)
	end_time = models.DateTimeField(blank=True, null=True)
	result = models.BooleanField(default=False)		