from django.contrib import admin

from .models import Grupo, Mensagem, UsuarioGrupo


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
