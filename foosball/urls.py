from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.idle, name="idle"),
    url(r'^home$', views.home,name="home"),

    url(r'^register$', views.register, name='register'),
    url(r'^login$', auth_views.login, {'template_name':'foosball/login.html'}, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^photo/(?P<usr_id>\d+)$', views.get_photo, name='photo'),
    url(r'^profile/(?P<usr_id>\d+)$', views.get_profile, name='profile'),
    url(r'^upload_photo/(?P<usr_id>\d+)$', views.upload_photo, name='upload_photo'),
    url(r'^follow/(?P<usr_id>\d+)$', views.add_follow, name='follow'),
    url(r'^unfollow/(?P<usr_id>\d+)$', views.cancel_follow, name='unfollow'),

    url(r'^update_page$', views.update_page),

    url(r'^game_room/(?P<room_id>\d+)$', views.game_room, name='game_room'),
    url(r'^create_room$', views.create_room, name='create_room'),
    url(r'^join_room/(?P<room_id>\d+)$', views.join_room, name='join_room'),
    url(r'^apply_room/(?P<room_id>\d+)$', views.apply_room, name='apply_room'),
    url(r'^get_ready$',views.get_ready,name='get_ready'),
    url(r'^cancel_ready$',views.cancel_ready,name='cancel_ready'),
    url(r'^quit_room/(?P<room_id>\d+)$',views.quit_room,name='quit_room'),
    url(r'^accept/(?P<usr_id>\d+)$',views.accept,name='accept'),
    url(r'^select_team/(?P<team_id>\d+)$',views.select_team,name='select_team'),
    url(r'^team_photo/(?P<team_id>\d+)$', views.team_photo, name='team_photo'),
    
    url(r'^game/(?P<room_id>\d+)$', views.game, name='game'),
]
