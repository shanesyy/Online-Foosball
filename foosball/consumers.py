from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from foosball.models import *
import random
import math
from django.utils import timezone

# the init angle list
angle_list = [math.pi*(i+30)/72 for i in range(4)]+[math.pi*(i+39)/72 for i in range(4)]

#################################################
# Websocket Consumer for communication in games #
#################################################
class GameConsumer(WebsocketConsumer):
    # the variable indicated whether the player is alone in the game
    is_alone = False

    #################################
    # Websocket connection function #
    #################################
    def connect(self):
        # get the room id from the url
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        # create the channel group based on the room id
        self.room_group_id = 'game_{}'.format(self.room_id)
        # get the room instance and the room owner id
        try:
            self.room = RoomEntry.objects.get(id=self.room_id)
            self.room_owner_id = self.room.owner.id
        except:
            self.room = None
        # added into the group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_id,
            self.channel_name
        )
        # broadcast the log in to all the members in the group if reconected
        if self.room:
            game_profile = self.room.players_info.filter(user = self.scope['user']).first()
            if game_profile.valid:
                side = 'left' if self.room_owner_id == self.scope['user'].id else 'right'
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_id, {'type': 'enter', 'from': side})
            else:
                game_profile.valid = True
                game_profile.save()

        self.accept()

    ####################################
    # Websocket disconnection function #
    ####################################
    def disconnect(self, close_code):
        # broadcast the log out to all the members in the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_id, {'type': 'exit'})
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_id,
            self.channel_name
        )

    ##################################
    # Receive message from WebSocket #
    ##################################
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # handle the paddle movement message
        if text_data_json.get('type') == 'paddle_data':
            # broadcast the paddle movement message to all group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_id,
                {
                    'type': 'paddle_data',
                    'direction': text_data_json['direction'],
                    'username': self.scope['user'].username,
                }
            )

        # handle the ball-paddle collision message
        elif text_data_json.get('type') == 'ball_data':
            # if the message is from the owner or only one player in the game
            # broadcast the collision message to the group
            if self.room and (self.room_owner_id == self.scope['user'].id or self.is_alone):
                async_to_sync(self.channel_layer.group_send)(self.room_group_id, text_data_json)
        
        # handle the goal message
        elif text_data_json.get('type') == 'goal_data':
            # if the message is from the owner or only one player in the game
            # broadcast the goal message to the group
            if self.room and (self.room_owner_id == self.scope['user'].id or self.is_alone):
                # check if the goal is the final goal
                finished = self.goal_helper(text_data_json['goal_side'])
                game_state = self.room.game_state
                if finished:
                    # if the goal finished the game, broadcast game over in the group
                    async_to_sync(self.channel_layer.group_send)(self.room_group_id, 
                        {
                            'type': 'game_over',
                            'side': text_data_json['goal_side'],
                            'left_score': game_state.score1,
                            'right_score': game_state.score2,
                        }
                    )
                else:
                    # if the game is not finished
                    # broadcast data to the group to initialize the next round
                    angle_index = random.randint(0, 7)
                    async_to_sync(self.channel_layer.group_send)(self.room_group_id,
                        {
                            'type': 'goal_data',
                            'side': text_data_json['goal_side'],
                            'angle': angle_list[angle_index],
                            'left_score': game_state.score1,
                            'right_score': game_state.score2,
                        }
                    )

        # handle the timeout game over message
        elif text_data_json.get('type') == 'game_over':
            game_state = self.room.game_state
            current_time = timezone.now()
            # update the game profile for each player
            for game_profile in self.room.players_info.all():
                if game_profile.user == self.room.owner:
                    game_profile.score = game_state.score1
                else:
                    game_profile.score = game_state.score2
                game_profile.end_time = current_time
                game_profile.result = game_profile.user == self.scope['user']
                game_profile.save()
            # update the current player's total score in profile
            profile = Profile.objects.get(id = self.scope['user'].id)
            profile.total_scores += 10
            profile.save()
            # delete the game room
            self.room.delete()

        # handle the sync message
        elif text_data_json.get('type') == 'sync_data':
            # check if the sync message from in-game or count-down
            if text_data_json['counts'] > -1:
                # if the sync message from count-down
                # update the ball angle for next round
                text_data_json['angle'] = angle_list[random.randint(0, 7)]
            async_to_sync(self.channel_layer.group_send)(self.room_group_id, text_data_json)

    # helper function for handling the goal message
    # update the models in the database after goal 
    def goal_helper(self, side):
        game_state = self.room.game_state
        win_score = 3
        # update the game state
        if side == 'left':
            game_state.score1 += 1
            score = game_state.score1
        else:
            game_state.score2 += 1
            score = game_state.score2
        game_state.save()
        # check if the game is finished after the goal
        if score >= win_score:
            current_time = timezone.now()
            # update the game profile if the game is finished
            for game_profile in self.room.players_info.all():
                if game_profile.user == self.room.owner:
                    game_profile.score = game_state.score1
                else:
                    game_profile.score = game_state.score2

                if game_profile.score == win_score:
                    # update the corresponding profiles if the player wins the game
                    game_profile.result = True
                    profile = game_profile.user.own
                    profile.total_scores += 10
                    profile.save()
                else:
                    # if lose the game
                    game_profile.result = False
                game_profile.end_time = current_time
                game_profile.save()
            # delete the room
            self.room.delete()
            return True
        return False

    ###################################
    # Receive message from room group #
    ###################################

    # send paddle movement message to client
    def paddle_data(self, event):
        self.send(text_data=json.dumps({
            'type': 'paddle_data',
            'direction': event['direction'],
            'from': event['username'],
        }))

    # send ball-paddle collision message to client
    def ball_data(self, event):
        self.send(text_data=json.dumps(event))

    # send goal message to client
    def goal_data(self, event):
        event['is_alone'] = self.is_alone
        self.send(text_data=json.dumps(event))

    # send game over message to client
    def game_over(self, event):
        self.send(text_data=json.dumps(event))

    # send reconnect message to client
    def enter(self, event):
        self.is_alone = False
        self.send(text_data=json.dumps(event))

    # update the state if receiving exit message from another player
    def exit(self, event):
        self.is_alone = True

    # send sync message to client
    def sync_data(self, event):
        self.send(text_data=json.dumps(event))


######################################################
# Websocket Consumer for communication in game rooms #
######################################################
class GameRoomConsumer(WebsocketConsumer):

    #################################
    # Websocket connection function #
    #################################
    def connect(self):
        # get the room id from the url
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        # create the group
        self.group_id = 'game_room_{}'.format(self.room_id)
        
        # get the instance of the room
        try:
            self.room = RoomEntry.objects.get(id=self.room_id)
            self.room_owner_id = self.room.owner.id
        except:
            self.room = None
        
        # added self into the group
        async_to_sync(self.channel_layer.group_add)(
            self.group_id,
            self.channel_name
        )

        self.accept()

    ####################################
    # Websocket disconnection function #
    ####################################
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_id,
            self.channel_name
        )

    ##################################
    # Receive message from WebSocket #
    ##################################
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # if the message is from the owner or only one player in the game
        if self.room and self.room_owner_id == self.scope['user'].id:
            # create the game state
            game_state = GameStateEntry(game_room=self.room, score1=0, score2=0, 
                ball_init_angle_index=random.randint(0, 7))
            game_state.save()

            # update the game profile
            current_time = timezone.now()
            for game_profile in self.room.players_info.all():
                guest = self.room.players_info.exclude(user = game_profile.user)[0]
                game_profile.guest = guest          
                game_profile.start_time = current_time
                game_profile.save()
           
            # broadcast the start game message to the group members
            async_to_sync(self.channel_layer.group_send)(
                self.group_id,
                {
                    'type': 'message',
                }
            )

    ###################################
    # Receive message from room group #
    ###################################

    # send startgame message to the client    
    def message(self, event):
        self.send(text_data=json.dumps({
            'start': True,
        }))