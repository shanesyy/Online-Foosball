from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.core import serializers
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.views.decorators.csrf import ensure_csrf_cookie
from django.forms.models import model_to_dict
from django.contrib.auth import views as auth_views
from mimetypes import guess_type
import datetime
import json
import random
import math

from foosball.forms import *
from foosball.models import *
from foosball.helper import *

# the init angle list
angle_list = [math.pi*(i+30)/72 for i in range(4)]+[math.pi*(i+39)/72 for i in range(4)]
# the team list being selected
team_enum = ["A_team","B_team","C_team","D_team","E_team","F_team","G_team","H_team","I_team","J_team"]

@login_required
def home(request):
    context = {}
    user = get_object_or_404(User, username = request.user)

    # check if the room is in game
    # if so, redirect to the game page
    rooms = user.room.all()
    for room in rooms:
        if room.status == 's4':
            return redirect(reverse('game', kwargs={'room_id':room.id}))

    # delete the gameprofile and update the room entry
    check_delete_user_from_game_room(user)

    user_profile = user.own
    context['followings'] = user_profile.following.all()
    context['gamerooms'] = RoomEntry.objects.all()
    context['page'] = 'home'

    return render(request, 'foosball/home.html', context)

@login_required
def idle(request):
    # redirect to the home page
    return redirect(reverse('home'))


def signup(request):
    return render(request, 'foosball/register.html', {})


def register(request):
    context = {}
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'foosball/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        print("form is not valid!")
        return render(request, 'foosball/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()
    # create profile for the user
    new_profile = Profile(user=new_user, total_scores=0)
    new_profile.save() 

    # Logs in the new user and redirects to the home page
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)
    return redirect(reverse('home'))


@login_required
def game_room(request,room_id):
    context = {}
    room = get_object_or_404(RoomEntry,id = room_id)
    user = get_object_or_404(User, username=request.user)
    # if get to the game room invalidly
    if user not in room.player.all():
        raise Http404

    context['user'] = user
    context['is_owner'] = user == room.owner
    context['players'] = room.players_info.all().order_by("number")
    context['room_id'] = room_id
    context['room_status'] = room.status
    context['is_ready'] = room.players_info.filter(user=user)[0].status
    context['page'] = 'gameroom'
    user_profile = get_object_or_404(Profile, user = user)
    context['followings'] = user_profile.following.all()
    return render(request, 'foosball/gameroom.html', context)


@login_required
def get_profile(request, usr_id):
    context = {}
    user = get_object_or_404(User, username = request.user)
    # delete the user's invalid profiles
    check_delete_user_from_game_room(user)
    # get the following list of the user
    user_profile = get_object_or_404(Profile, user = user)
    context['followings'] = user_profile.following.all()
    # get the game profiles of the given user directed by the user id
    if user.id == usr_id:
        cur_profile = user_profile
        gameprofiles = user.game_info.filter(valid = True).filter(end_time__isnull=False).filter(start_time__isnull=False)
    else:
        cur_user = get_object_or_404(User, id = usr_id)
        cur_profile = get_object_or_404(Profile, user = cur_user)
        gameprofiles = cur_user.game_info.filter(valid = True).filter(end_time__isnull=False).filter(start_time__isnull=False)
        if cur_user in context['followings']:
            context['is_followed'] = True
        else:
            context['is_followed'] = False

    durations = []
    teams = []
    # calculate the durations for each game
    for profile in gameprofiles:
        s = int((profile.end_time-profile.start_time).total_seconds())
        durations.append('{:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60))
        teams.append(team_enum[profile.team])

    context["gameprofiles"] = zip(durations,teams,gameprofiles)
    context['form'] = ProfileForm()
    context["user"] = user
    context["cur_profile"] = cur_profile
    context['cur_id'] = usr_id
    return render(request, 'foosball/person_bio.html', context)


@login_required
def get_photo(request, usr_id):
    user = get_object_or_404(User, id=usr_id)
    profile = get_object_or_404(Profile, user=user)
    content_type = guess_type(profile.picture.name)
    return HttpResponse(profile.picture, content_type=content_type) 

@login_required
# function for getting the team image
def team_photo(request, team_id):
    valid_image = "foosball/static/foosball/img/player"+str(int(team_id)+1)+".jpg"
    content_type = guess_type(valid_image)
    try:
        with open(valid_image, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        response = HttpResponse(content_type="image/jpeg")
    return response


@login_required
def upload_photo(request,usr_id):
    context = {}
    user = get_object_or_404(User, id=usr_id)
    profile = get_object_or_404(Profile,user=user)
    DEFAULT_PHOTO_PATH = profile.picture

    context["cur_id"] = usr_id
    context['form'] = ProfileForm()
    context["user"] = user
    
    if request.method == 'GET':
        context["cur_profile"] = profile
        return render(request, 'foosball/person_bio.html', context)
    # get and store the uploaded image
    if request.method == "POST":
        if 'picture' in request.FILES and profile.picture != "images/anonymous.png":
            profile.picture.delete()
        form = ProfileForm(request.POST, request.FILES, instance = profile)
        if not profile:
            raise Http404
        if "picture" in request.POST:
            if request.POST['picture']:
                profile.picture = request.POST['picture']
            else:
                profile.picture = DEFAULT_PHOTO_PATH        
        else:
            print("no photo upload!")
    try:
        form.save()
    except:
        profile.save()
    context['cur_profile'] = profile
    # get all the game profiles of the current user
    gameprofiles = user.game_info.filter(valid = True).filter(end_time__isnull=False).filter(start_time__isnull=False)
    durations = []
    teams = []
    for profile in gameprofiles:
        s = int((profile.end_time-profile.start_time).total_seconds())
        durations.append('{:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60))
        teams.append(team_enum[profile.team])
    context["gameprofiles"] = zip(durations,teams,gameprofiles)
    return render(request, 'foosball/person_bio.html', context)

@login_required
def add_follow(request,usr_id):
    user = get_object_or_404(User,username=request.user)
    # delete the invalid profiles of the user
    check_delete_user_from_game_room(user)
    # get the followed user and profile
    follow_user = get_object_or_404(User, id = usr_id)
    follow_profile = follow_user.own

    # update the login user's profile
    user_profile = user.own
    user_profile.following.add(follow_user)
    user_profile.save()

    user_followings = user_profile.following.all()
    context = {'followings': user_followings,'user':user,'cur_profile':follow_profile, 'cur_id':usr_id, 'is_followed': True}
    
    # get all the game profiles of the given user
    gameprofiles = follow_user.game_info.filter(valid = True).filter(end_time__isnull=False).filter(start_time__isnull=False)
    durations = []
    teams = []
    for profile in gameprofiles:
        s = int((profile.end_time-profile.start_time).total_seconds())
        durations.append('{:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60))
        teams.append(team_enum[profile.team])
    context["gameprofiles"] = zip(durations,teams,gameprofiles)
    user_profile = get_object_or_404(Profile, user = user)
    context['followings'] = user_profile.following.all()
    return render(request, 'foosball/person_bio.html',context)

@login_required
def cancel_follow(request,usr_id):

    user = get_object_or_404(User,username=request.user)

    check_delete_user_from_game_room(user)

    follow_user = get_object_or_404(User, id = usr_id)
    follow_profile = follow_user.own
    
    # update the login user's profile
    user_profile = user.own
    user_profile.following.remove(follow_user)
    user_profile.save()

    user_followings = user_profile.following.all()
    context = {'followings': user_followings,'user':user,'cur_profile':follow_profile, 'cur_id':usr_id, 'is_followed': False}
    
    # get all the game profiles of the given user
    gameprofiles = follow_user.game_info.filter(valid = True).filter(end_time__isnull=False).filter(start_time__isnull=False)
    durations = []
    teams = []
    for profile in gameprofiles:
        s = int((profile.end_time-profile.start_time).total_seconds())
        durations.append('{:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60))
        teams.append(team_enum[profile.team])
    context["gameprofiles"] = zip(durations,teams,gameprofiles)
    user_profile = get_object_or_404(Profile, user = user)
    context['followings'] = user_profile.following.all()
    return render(request, 'foosball/person_bio.html',context)

@login_required
# function for communicating with the ajax
def update_page(request):
    response_data = {}
    if request.method != "POST":
        raise Http404
    response_data['leaders'] = get_update_leaders(request.user)
    cur_page = request.POST['cur_page'].split('foosball/')[-1]
    user = get_object_or_404(User,username=request.user)
    
    # if the current page is home page
    if not cur_page or cur_page == 'home':
        response_data['rooms'] = get_update_game_rooms()
        if user.room:
            for room in user.room.all():
                print("my room is", room.id)
                response_data['url'] = "/foosball/game_room/{}".format(room.id)
    
    # if the current page is the game room page
    if cur_page.startswith('game_room'):
        room_id = cur_page.split('/')[-1]
        response_data['players'],response_data['can_start'] = get_update_player_status(request.user, room_id)
        if not user.room.all():
            response_data['url'] = "foosball/home"
        else:
            room = get_object_or_404(RoomEntry,id = room_id)
            if room.owner == user:
                response_data['applicants'] = get_update_waitlist(request.user,room_id)

    return HttpResponse(json.dumps(response_data), content_type='application/json')

@login_required
def game(request, room_id):
    user = get_object_or_404(User,username=request.user)
    # try to get the game room and game state
    try:
        game_room  = RoomEntry.objects.get(id = room_id)
        game_state = game_room.game_state
    except:
        return redirect(reverse('home'))
    
    # initialize the game state
    init_angle = angle_list[game_state.ball_init_angle_index]
    left_score = game_state.score1
    right_score = game_state.score2

    players = game_room.player.all()
    owner = game_room.owner
    guest = game_room.player.exclude(id = owner.id).first()

    game_profile = game_room.players_info.filter(user = user).first()
    if not game_profile.valid:
        first_in = 1
    else:
        first_in = 0
    # update the game room profile
    if game_room.status != 's4':
        game_room.status = 's4'
        game_room.save()

    side = 'left' if user == owner else 'right'

    return render(request, 'foosball/game.html', {'room_id':room_id, 
        'init_angle':init_angle, 'left_player':owner, 
        'right_player':guest, 'side': side, 
        'left_score': left_score, 'right_score': right_score, 'first_in': first_in})

@login_required
def create_room(request):
    context = {}
    user = get_object_or_404(User,username = request.user)
    # delete the invalid profiles
    check_delete_user_from_game_room(user)

    # create a new room entry
    room_item = RoomEntry(owner = user,player_num = 1)
    room_item.save()
    room_item.player.add(user)

    # create a new game profile
    game_profile_item = GameProfileEntry(user = user, number=1, game_room =room_item)
    game_profile_item.save()

    return redirect(reverse('game_room', kwargs={'room_id':room_item.id}))

@login_required
def join_room(request, room_id):
    context = {}
    user = get_object_or_404(User, username=request.user)
    room = get_object_or_404(RoomEntry, id=room_id)
    response_data = {}
    if request.method == "POST":
        room.player.add(request.user)
        game_profile_item = GameProfileEntry(user = user, number=room.player_num + 1, game_room =room, team=2)
        game_profile_item.save()

        room.player_num += 1
        room.save()

        response_data['url'] = "/foosball/game_room/{}".format(room_id)
    else:
        response_data['url'] = '/foosball/'
    return HttpResponse(json.dumps(response_data), content_type='application/json')

@login_required
def apply_room(request, room_id):
    response_data = {}
    user = get_object_or_404(User,username = request.user)
    room = get_object_or_404(RoomEntry, id = room_id)
    if request.method == "POST":
        if user.apply_info.first():
            message = "You have already applied one room. Please wait and try again later."
        else:
            waititem = WaitUserEntry(user = user,room = room)
            waititem.save()
            message = "Request sent successfully! Please wait for the response"
        response_data = {"message": message}
    else:
        check_delete_user_from_game_room(user)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


@login_required
def accept(request, usr_id):
    context = {}
    owner = get_object_or_404(User, username=request.user)
    applicant = get_object_or_404(User,id = usr_id)
    room = owner.my_room
    response_data = {}
    if request.method == "POST":
        room.player.add(applicant)
        game_profile_item = GameProfileEntry(user = applicant, number=room.player_num + 1, game_room =room, team=2)
        game_profile_item.save()
        room.player_num += 1
        applicant.apply_info.first().delete()
        room.save()
        response_data['url'] = "/foosball/game_room/{}".format(room.id)
    else:
        response_data['url'] = '/foosball/'
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@login_required
def select_team(request,team_id):
    user = get_object_or_404(User,username=request.user)
    room = user.room.all()
    roomid = 0
    for room in user.room.all():
        roomid = room.id
    team_id = int(team_id)
    if team_id >= 0 and team_id <= 8:
        game_profile = get_object_or_404(GameProfileEntry,user = user,game_room=roomid)
        game_profile.team = team_id + 1
        game_profile.save()
    return redirect(reverse('game_room', kwargs={'room_id':roomid}))


@login_required
def get_ready(request):
    user = get_object_or_404(User, username=request.user)
    room = user.room.all().first()
    if room:
        game_profile = room.players_info.filter(user=user).first()

        # if the user use the url to change the status invalidly
        if room.owner == user:
            other_game_profile = room.players_info.exclude(user=user).first()
            if not other_game_profile or not other_game_profile.status:
                return redirect(reverse('game_room', kwargs={'room_id':room.id}))

        game_profile.status = True
        game_profile.save()
        return redirect(reverse('game_room', kwargs={'room_id':room.id}))
    else:
        return redirect(reverse('home'))

@login_required
def cancel_ready(request):
    user = get_object_or_404(User, username=request.user)
    room = user.room.all().first()
    if room:
        game_profile = room.players_info.filter(user=user).first()
        game_profile.status = False
        game_profile.save()
        return redirect(reverse('game_room', kwargs={'room_id':room.id}))
    else:
        return redirect(reverse('home'))

@login_required
def quit_room(request, room_id):
    user = get_object_or_404(User,username=request.user)
    check_delete_user_from_game_room(user)
    return redirect(reverse('home'))

@login_required
def logout(request):
    user = get_object_or_404(User,username=request.user)
    check_delete_user_from_game_room(user)
    return auth_views.logout_then_login(request)
