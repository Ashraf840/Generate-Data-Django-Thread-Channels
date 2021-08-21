from django.shortcuts import render
from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# import json
# import time

from .models import *


async def index(request):
    # # Generating data in this method, then sends back to the consumer
    # for i in range(1, 10):
    #     data = { 'count': i }  # generating data manually
    #     print(data)

    #     # Each data is immediately sending to the channel-consumer-group
    #     channel_layers = get_channel_layer() # get all channel_layers
    #     await (channel_layers.group_send)(
    #         'new_consumer_group', # specify the group-name 
    #         # 'test_consumer_group', # specify the group-name 
    #         {
    #             'type': 'send_nofication',  # calling a consumer-method
    #             'value': json.dumps(data)   # Converts a python-dict into json-obj
    #         }
    #     )
    #     time.sleep(1)

    # Now, I'm connecting the consumer ("NewConsumer") from the frontend's ("index.html") websocket

    return render(request, 'home/index.html')


