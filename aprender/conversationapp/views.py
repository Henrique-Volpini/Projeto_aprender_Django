from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


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
    return render(request, "conversationapp/conversas.html")