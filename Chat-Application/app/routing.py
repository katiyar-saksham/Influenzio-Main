from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/chat/<str:username>/<str:other_username>', ChatConsumer.as_asgi()),
    path('ws/chat', EchoConsumer.as_asgi()),
]