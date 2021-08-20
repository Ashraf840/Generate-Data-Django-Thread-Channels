from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json

# [Boilerplate Consumer/ Synchronous] [Portal-holder]
# The purpose of making a consumer, is to sent/receive data from the backend to the frontend where the server-gateway is always opened unless frontend/ backend closes the Socket-connection.
# Used inside the "home/models.py"
class TestConsumer(WebsocketConsumer):

    # ws://
    # Connects the channel-instance
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()   # Accepts the WebSocket connection
        
        # sending data from backend to frontend
        self.send(text_data=json.dumps({
            'status': 'Connected With a Django Channel Successfully!'
        }))

    # Receive data from frontend to backend using the parameterized "text_data" variable
    def receive(self, text_data):
        print(text_data)    # prints the frontend data to the runserver console
        # Sends data back to the client protocol/ websocket
        self.send(text_data=json.dumps({
            'msg-status': 'We got your message!'
        }))
    
    # Custom-made method in the consumer, so that it can be called in the "group_send()" of cahnnel_layer.
    # This method is called from the "home/models.py" file's 'save' method, which is inside the 'Notification' model. 
    # Everytime, a new notification is created, the 'save' method from the "Notification" model-class gets called, so do the "TestConsumer" gets called from the 'save' method.
    def send_nofication(self, event):
        print('Get notification to be sent!')
        # print(event)   # displaying the var-value in the 'runserver-console' sent from the 'notification' model
        print(event.get('value'))   # extract & display only the 'value' key-content

        # "event" variable is a json-obj
        data = json.loads(event.get('value'))   # converts the json-obj into python-dict
        # Sends data back to the client protocol/ frontend websocket
        self.send(text_data=json.dumps({
            'payload': data
        }))
        print('Get notification to be sent!')

    # Disconnects the channel-instance
    def disconnect(self, *args, **kwargs):
        print('Disconnected!')    # prints the frontend data to the runserver console



# Asynchronous Consumer [Portal-holder]
# Used inside the "home/views.py"
class NewConsumer(AsyncJsonWebsocketConsumer):
    # Connects the channel-instance
    async def connect(self):
        self.room_name = "new_consumer"
        self.room_group_name = "new_consumer_group"

        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        print('Connected with New Async Json Consumer Successfully!')

        await self.send(text_data=json.dumps({
            'status': 'Connected with New Async Json Consumer Successfully!'
        }))
    
    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data=json.dumps({
            'msg-status': 'We got your message!'
        }))
    
    # This method is called from the "home/views.py" file's 'index' method.
    # [not using in the 'index' view] Everytime, 'index' view/method gets called, it'll generate a range of numbers to be send back to this consumer, se that it can be sent back to the frontend-websocket.
    # Whenever the 'generate_student_data' api view/ method gets called, it'll call a thread-class ("CreateStudentsThread"), this thread will call the 'run' method, the 'run' method will create a specific num of students-rec in db, then call this func in the channel-layer-group-send
    # Working as a receiver to receive the payloads that are sent to the redis-server, and then sends back those received-payloads to each individual frontend-websocket-connections.
    # (Sends to redis-server. - not sure its correct or not)
    async def send_nofication(self, event):
        data = json.loads(event.get('value'))
        await self.send(text_data=json.dumps({
            'payload': data
        }))

    async def disconnect(self, *args, **kwargs):
        print('Disconnected!')
