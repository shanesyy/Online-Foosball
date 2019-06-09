from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
	url(r'^ws/foosball/game/(?P<room_id>\d+)/$', consumers.GameConsumer),
	url(r'^ws/foosball/gameroom/(?P<room_id>\d+)/$', consumers.GameRoomConsumer)
]