# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/test/', consumers.TestConsumer.as_asgi()),
    path('ws/new/', consumers.NewConsumer.as_asgi()),
]