import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Message
 
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#     async def disconnect(self , close_code):
#         await self.channel_layer.group_discard(
#             self.roomGroupName , 
#             self.channel_layer 
#         )
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         username = text_data_json["username"]
#         await self.channel_layer.group_send(
#             self.roomGroupName,{
#                 "type" : "sendMessage" ,
#                 "message" : message , 
#                 "username" : username ,
#             })
#     async def sendMessage(self , event) : 
#         message = event["message"]
#         username = event["username"]
#         await self.send(text_data = json.dumps({"message":message ,"username":username}))


class ChatConsumer(AsyncJsonWebsocketConsumer):
    

    async def connect(self):
        print("Connected")
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")

    async def receive_json(self, content):
        message = content['message']
        username = content['username']

        # Save the message to the database
        await self.save_message(message, username)

        # Get all the messages in the table
        messages = await self.get_messages()

        # Send the messages back to the WebSocket
        await self.send_json(list(messages))

    @database_sync_to_async
    def save_message(self, message, username):
        # This is a synchronous function
        Message.objects.create(message=message, username=username)

    @database_sync_to_async
    def get_messages(self):
        # This is a synchronous function
        return list(Message.objects.values('message', 'username'))