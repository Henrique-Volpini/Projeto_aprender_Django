import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime

from .models import Grupo, Mensagem


def _serializar_mensagem(msg):
    return {
        "id": msg.id,
        "conteudo": msg.conteudo,
        "autor": msg.user.get_username(),
        "autor_id": msg.user_id,
        "created_at": localtime(msg.created_at).strftime("%d/%m/%Y %H:%M"),
    }


def home(request):
    if request.user.is_authenticated:
        return redirect("conversas")  # evita mostrar tela de login em cache

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("conversas")

        return render(request, "conversationapp/base.html", {
            "erro": "Usuario ou senha invalidos."
        })

    return render(request, "conversationapp/base.html")


@login_required
def conversas(request):
    grupos = request.user.grupos_conversa.all()
    return render(
        request,
        "conversationapp/conversas.html",
        {"grupos": grupos},
    )


@login_required
def mensagens_grupo(request, grupo_id):
    grupo = get_object_or_404(
        Grupo.objects.prefetch_related("participantes"),
        id=grupo_id,
        participantes=request.user,
    )
    if request.method == "POST":
        conteudo = ""
        if request.content_type and "application/json" in request.content_type:
            try:
                payload = json.loads(request.body.decode("utf-8"))
            except json.JSONDecodeError:
                return JsonResponse({"erro": "JSON invalido."}, status=400)
            conteudo = (payload.get("conteudo") or "").strip()
        else:
            conteudo = (request.POST.get("conteudo") or "").strip()

        if not conteudo:
            return JsonResponse({"erro": "Mensagem vazia."}, status=400)

        msg = Mensagem.objects.create(
            grupo=grupo,
            user=request.user,
            conteudo=conteudo,
        )
        return JsonResponse({"mensagem": _serializar_mensagem(msg)}, status=201)

    mensagens = Mensagem.objects.filter(grupo=grupo).select_related("user").order_by("created_at")
    payload = [_serializar_mensagem(msg) for msg in mensagens]
    return JsonResponse({"grupo": {"id": grupo.id, "nome": grupo.nome}, "mensagens": payload})
