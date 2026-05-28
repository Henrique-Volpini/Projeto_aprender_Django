from django.contrib import admin

from .models import Amizade, Grupo, Mensagem, Perfil, UsuarioGrupo


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)


@admin.register(UsuarioGrupo)
class UsuarioGrupoAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "grupo")
    list_filter = ("grupo",)
    search_fields = ("user__username", "grupo__nome")


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ("id", "grupo", "user", "created_at")
    list_filter = ("grupo", "created_at")
    search_fields = ("conteudo", "user__username", "grupo__nome")


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("user__username",)


@admin.register(Amizade)
class AmizadeAdmin(admin.ModelAdmin):
    list_display = ("id", "requester", "recipient", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("requester__username", "recipient__username")
