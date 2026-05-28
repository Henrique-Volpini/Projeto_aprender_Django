from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Perfil

User = get_user_model()


@receiver(post_save, sender=User)
def criar_perfil_para_novo_usuario(instance, created, **_kwargs):
    if not created:
        return
    Perfil.objects.get_or_create(user=instance)
