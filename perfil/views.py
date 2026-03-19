from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm
from .models import CadastroPerfil


def _get_perfil_logado(request):
    perfil_id = request.session.get("perfil_id")
    if not perfil_id:
        return None
    return CadastroPerfil.objects.filter(id=perfil_id).first()


def _is_admin(perfil):
    return bool(perfil and perfil.controle_acesso == "admin")


def lista_perfis(request):
    perfil_logado = _get_perfil_logado(request)
    if not perfil_logado:
        return redirect("login")

    perfis = CadastroPerfil.objects.order_by("nome_completo", "id")
    return render(
        request,
        "perfil/lista.html",
        {"perfis": perfis, "perfil_logado": perfil_logado, "is_admin": _is_admin(perfil_logado)},
    )


def cadastro_perfil(request):
    perfil_logado = _get_perfil_logado(request)
    if not perfil_logado:
        return redirect("login")

    if not _is_admin(perfil_logado):
        messages.error(request, "Apenas admin pode cadastrar perfis.")
        return redirect("lista_perfis")

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_perfis")
    else:
        form = ProfileForm()

    return render(request, "perfil/cadastro.html", {"form": form, "perfil_logado": perfil_logado, "is_admin": True})


def editar_perfil(request, pk):
    perfil_logado = _get_perfil_logado(request)
    if not perfil_logado:
        return redirect("login")

    if not _is_admin(perfil_logado):
        messages.error(request, "Apenas admin pode editar perfis.")
        return redirect("lista_perfis")

    perfil = get_object_or_404(CadastroPerfil, pk=pk)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("lista_perfis")
    else:
        form = ProfileForm(instance=perfil)

    return render(
        request,
        "perfil/cadastro.html",
        {"form": form, "perfil": perfil, "perfil_logado": perfil_logado, "is_admin": True},
    )


def excluir_perfil(request, pk):
    perfil_logado = _get_perfil_logado(request)
    if not perfil_logado:
        return redirect("login")

    if not _is_admin(perfil_logado):
        messages.error(request, "Apenas admin pode excluir perfis.")
        return redirect("lista_perfis")

    perfil = get_object_or_404(CadastroPerfil, pk=pk)
    if request.method == "POST":
        perfil.delete()
        messages.success(request, "Perfil excluído com sucesso.")
        return redirect("lista_perfis")

    return redirect("lista_perfis")
