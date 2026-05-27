from django.urls import path

from .consumers import GrupoConsumer

websocket_urlpatterns = [
    path("ws/grupos/<int:grupo_id>/", GrupoConsumer.as_asgi()),
]
