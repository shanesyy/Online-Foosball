from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.db import transaction
import json
from foosball.models import *
import datetime
from django.utils import timezone


# helper function for getting the new leader board
def get_update_leaders(user):
    leaders = Profile.objects.order_by("-total_scores")[:10]
    followed = user.own.following.all()
    update_leaders = [{'html':render_to_string('foosball/leader.html', context={"leader": x, "user_id": user.id, "followed": x.user in followed})} for x in leaders]
    response_leaders_data = json.dumps(update_leaders)
    return response_leaders_data

# helper function for getting the existed game rooms
def get_update_game_rooms():
    rooms = RoomEntry.objects.order_by("id")
    update_rooms = [{'html':render_to_string('foosball/hp_gameroom.html', context={"room": x})} for x in rooms]
    response_rooms_data = json.dumps(update_rooms)
    return response_rooms_data

# helper function for getting the player's status in the given game room
def get_update_player_status(user, room_id):
    try:
        room = RoomEntry.objects.get(id=room_id)
    except:
        return json.dumps("room_closed"), False
    players = room.players_info.all().order_by("number")
    update_players = [{'html':render_to_string('foosball/player_status.html', context={"player": x})} for x in players]
    response_players_data = json.dumps(update_players)
    if room.owner == user:
        can_start = sum([x.status for x in players]) >= 1
    else:
        can_start = False
    return response_players_data, can_start

# helper function for updating the waitlist of the given game room
def get_update_waitlist(user,room_id):
    try:
        room = RoomEntry.objects.get(id=room_id)
    except:
        return json.dumps("room_closed"), False

    room.waitlist.all().filter(create_time__lt=timezone.now() - datetime.timedelta(seconds=50)).delete()
    room.save()
    applicants =room.waitlist.all()
    update_applicants = [{'html':render_to_string('foosball/waitlist.html', context={"id": x.user.id,"username":x.user.username,"score":x.user.own.total_scores,"room_player_num":x.room.player_num})} for x in applicants]
    response_applicants_data = json.dumps(update_applicants)
    return response_applicants_data

# helper function for deleting the invalid game profiles and updating the room after a user exit a room
@transaction.atomic
def check_delete_user_from_game_room(user): 
    try:
        with transaction.atomic():
            rooms = user.room.all()
            for room in rooms:
                game_profile = room.players_info.filter(user = user).filter(valid = False)

                for profile in game_profile:
                    profile.delete()

                if room.status != 's4':
                    if room.owner == user:
                        guest_profile = room.players_info.exclude(user = user)
                        if guest_profile:
                            guest_profile[0].delete()
                        room.delete()
                    else:
                        if room:
                            room.player.remove(user)
                            room.player_num -= 1
                            room.save()
    except:
        pass