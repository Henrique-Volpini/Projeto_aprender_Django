from django.conf import settings
from django.db import models


class Grupo(models.Model):
    nome = models.CharField(max_length=120)
    participantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="UsuarioGrupo",
        related_name="grupos_conversa",
    )

    class Meta:
        db_table = "grupo"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class UsuarioGrupo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vinculos_grupo",
    )
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.CASCADE,
        related_name="vinculos_usuario",
    )

    class Meta:
        db_table = "users_grupos"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "grupo"],
                name="uniq_user_grupo",
            )
        ]

    def __str__(self):
        return f"user={self.user_id} grupo={self.grupo_id}"


class Mensagem(models.Model):
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.CASCADE,
        related_name="mensagens",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mensagens_enviadas",
    )
    conteudo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mensagens"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user_id} -> {self.grupo_id}"
