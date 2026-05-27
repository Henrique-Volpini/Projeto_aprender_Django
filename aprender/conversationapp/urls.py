from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("conversas/", views.conversas, name="conversas"),
    path(
        "conversas/grupos/<int:grupo_id>/mensagens/",
        views.mensagens_grupo,
        name="grupo_mensagens",
    ),
]
