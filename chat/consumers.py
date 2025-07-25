import json  
from channels.generic.websocket import AsyncWebsocketConsumer  
from django.contrib.auth.models import AnonymousUser  
from .models import Conversation, Message  

class ChatConsumer(AsyncWebsocketConsumer):  
    async def connect(self):  
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']  
        await self.channel_layer.group_add(  
            f"chat_{self.conversation_id}",  
            self.channel_name  
        )  
        await self.accept()  

    async def receive(self, text_data):  
        data = json.loads(text_data)  
        
        sender = self.scope.get('user', AnonymousUser())  
        if sender.is_anonymous:  
            sender = None    

        conversation = await Conversation.objects.aget(id=self.conversation_id)  
        message = await Message.objects.acreate(  
            conversation=conversation,  
            sender=sender,  
            content=data['message']  
        )  

        await self.channel_layer.group_send(  
            f"chat_{self.conversation_id}",  
            {  
                'type': 'chat_message',  
                'message': data['message'],  
                'sender_id': str(sender.id) if sender else None,  
                'timestamp': str(message.timestamp)  
            }  
        )  

    async def chat_message(self, event):  
        await self.send(text_data=json.dumps(event))  