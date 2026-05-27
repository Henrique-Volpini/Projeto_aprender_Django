import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime

from .models import Grupo, Mensagem, UsuarioGrupo


class GrupoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        self.grupo_id = self.scope["url_route"]["kwargs"]["grupo_id"]

        if not user or user.is_anonymous:
            await self.close(code=4001)
            return

        if not await self._usuario_no_grupo(user.id, self.grupo_id):
            await self.close(code=4003)
            return

        self.group_name = f"grupo_{self.grupo_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        try:
            payload = json.loads(text_data)
        except json.JSONDecodeError:
            return

        conteudo = (payload.get("conteudo") or "").strip()
        if not conteudo:
            return

        mensagem = await self._criar_mensagem(
            user_id=self.scope["user"].id,
            grupo_id=self.grupo_id,
            conteudo=conteudo,
        )
        if not mensagem:
            return

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "mensagem": mensagem,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "tipo": "nova_mensagem",
                    "mensagem": event["mensagem"],
                },
                ensure_ascii=False,
            )
        )

    @database_sync_to_async
    def _usuario_no_grupo(self, user_id, grupo_id):
        return UsuarioGrupo.objects.filter(user_id=user_id, grupo_id=grupo_id).exists()

    @database_sync_to_async
    def _criar_mensagem(self, user_id, grupo_id, conteudo):
        if not UsuarioGrupo.objects.filter(user_id=user_id, grupo_id=grupo_id).exists():
            return None

        User = get_user_model()
        user = User.objects.get(id=user_id)
        grupo = Grupo.objects.get(id=grupo_id)

        msg = Mensagem.objects.create(
            grupo=grupo,
            user=user,
            conteudo=conteudo,
        )

        return {
            "id": msg.id,
            "conteudo": msg.conteudo,
            "autor": user.get_username(),
            "autor_id": user.id,
            "created_at": localtime(msg.created_at).strftime("%d/%m/%Y %H:%M"),
        }
