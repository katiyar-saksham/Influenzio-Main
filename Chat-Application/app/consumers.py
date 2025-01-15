from channels.consumer import SyncConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User 
from .models import *
import json

class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        me_username = self.scope['url_route']['kwargs']['username']
        other_username = self.scope['url_route']['kwargs']['other_username']
        me = User.objects.get(username=me_username)
        other_user = User.objects.get(username=other_username)
        self.thread_obj = Thread.objects.get_or_create_personal_thread(me, other_user)

        self.room_name = f'personal_thread_{self.thread_obj.id}'
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.send({
            'type':'websocket.accept'
        })
    
    def websocket_receive(self, event):
        me_username = self.scope['url_route']['kwargs']['username']
        msg = json.dumps({
            'text':event.get('text'),
            'username': me_username,
        })

        self.store_message(event.get('text'))

        async_to_sync(self.channel_layer.group_send)(
            self.room_name, 
            {
                'type':'websocket.message',
                'text': msg
            }
        )

    def websocket_message(self, event):
        self.send({
                'type':'websocket.send',
                'text': event.get('text')
        })
        
    def store_message(self, text):
        me_username = self.scope['url_route']['kwargs']['username']
        me = User.objects.get(username=me_username)
        Message.objects.create(
            thread = self.thread_obj,
            sender = me,
            text = text
        )

    def websocket_disconnect(self, event):
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

class EchoConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.room_name = 'broadcast'
        self.send({
            'type':'websocket.accept'
        })
        # whenever a websocket is created a unique channel_name is assigned to it.
        # group_add function is asynchronous so to utilise it in a synchronous consumer we need to import asyn_to_sync method and use it.
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
    
    def websocket_receive(self, event):

        # The group_send method will send the dictionary mentioned after self.room_name in the list of parameters to the group/room created. This dictionary will also have an event which will be executed in every channel/ socket connection.
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, 
            {
                'type':'websocket.message',
                'text': event.get('text')
            }
        )

    # Every channel/ socket connection created in the same group will execute the following method using the data provide by group_send method above.
    def websocket_message(self, event):
        self.send({
                'type':'websocket.send',
                'text': event.get('text')
        })
        

    def websocket_disconnect(self, event):
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
       


