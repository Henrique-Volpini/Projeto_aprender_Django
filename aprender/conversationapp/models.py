from django.conf import settings
from django.db import models


class Perfil(models.Model):
    THEME_DARK = "dark"
    THEME_PINK = "pink"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    theme = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "perfil"

    def __str__(self):
        return f"perfil user={self.user_id}"


class Amizade(models.Model):
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_BLOCKED = "blocked"

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="amizades_enviadas",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="amizades_recebidas",
    )
    status = models.CharField(
        max_length=20,
        default=STATUS_PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "amizades"
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(requester=models.F("recipient")),
                name="ck_amizade_user_diff",
            ),
            models.UniqueConstraint(
                fields=["requester", "recipient"],
                name="uniq_amizade_requester_recipient",
            ),
        ]

    def __str__(self):
        return f"{self.requester_id} -> {self.recipient_id} ({self.status})"


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
