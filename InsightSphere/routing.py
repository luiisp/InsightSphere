from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/c/(?P<username>\w+)/(?P<channel_id>\d+)/$', ChatConsumer.as_asgi()),
]
