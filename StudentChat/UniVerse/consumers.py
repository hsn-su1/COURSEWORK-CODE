from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync # used to convert asynchronous layer functions to synchronus as we are writing in synchronusly
import json # we are going to convert the jason formatted values in text_data
from . import models
from django.contrib.auth.models import User
import datetime

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()

        try:

            user_channel = models.UserChannel.objects.get(user=self.scope.get("user")) # If there is a channel containing this user dont create a new one just change the channel name
            user_channel.channel_name = self.channel_name
            user_channel.save()

        except:

            user_channel = models.UserChannel() # If there is no channel containing this user create new user with new channel name
            user_channel.user = self.scope.get("user")
            user_channel.channel_name = self.channel_name
            user_channel.save()

        self.person_id = self.scope.get("url_route").get("kwargs").get("id")

    def receive(self, text_data):
        text_data = json.loads(text_data)
        other_user_id = User.objects.get(id=self.person_id)

        if text_data.get("type") == "text":

            now = datetime.datetime.now()
            date = now.date()
            time = now.time()

            new_message = models.Message()
            new_message.from_whom = self.scope.get("user")
            new_message.to_whom = other_user_id
            new_message.message = text_data.get("message")
            new_message.date = date
            new_message.time = time
            new_message.has_been_seen = False
            new_message.save()

            try:

                other_user = models.UserChannel.objects.get(user=other_user_id)

                data = {
                    "type":"recevier_function",
                    "type_of_data":"text",
                    "data":text_data.get("message") 
                }

                async_to_sync(self.channel_layer.send)(other_user.channel_name, data)

            except:
                
                pass

        elif text_data.get("type") == "i_have_seen_the_messages":

            try:

                other_user = models.UserChannel.objects.get(user=other_user_id)

                data = {"type":"recevier_function",
                        "type_of_data":"the_messages_have_been_seen_from_the_other"}

                async_to_sync(self.channel_layer.send)(other_user.channel_name, data)

                messages_have_not_been_seen = models.Message.objects.filter(from_whom=other_user_id, to_whom=self.scope.get("user"))
                messages_have_not_been_seen.update(has_been_seen=True)

            except:
                
                pass

    def recevier_function(self, data_from_layer):
        data = json.dumps(data_from_layer)
        self.send(data)