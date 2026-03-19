from django.contrib import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection
import re
from urllib.parse import quote

from .forms import AvisoForm, QuadroAvisoForm, ComunicadoForm, EventoForm, FotoPostagemForm, VideoPostagemForm
from perfil.models import CadastroPerfil
from .models import (
    Aviso,
    AvisoEnvio,
    QuadroAviso,
    QuadroAvisoEnvio,
    Comunicado,
    ComunicadoEnvio,
    Evento,
    EventoEnvio,
    FotoPostagem,
    FotoAnexo,
    VideoPostagem,
    VideoAnexo,
)


def _get_perfil_logado(request):
    perfil_id = request.session.get("perfil_id")
    if not perfil_id:
        return None
    return CadastroPerfil.objects.filter(id=perfil_id).first()


def _require_admin(request):
    perfil = _get_perfil_logado(request)
    if not perfil or perfil.controle_acesso != "admin":
        messages.error(request, "Apenas admin pode acessar esta página.")
        return None
    return perfil


def home(request):
    if not request.session.get("perfil_id"):
        return redirect("login")
    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    return render(request, "core/home.html", {"perfil": perfil})


def aniversariantes(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    hoje = timezone.localdate()
    aniversariantes_qs = CadastroPerfil.objects.filter(
        data_nascimento__month=hoje.month,
        data_nascimento__day=hoje.day,
    ).order_by("nome_completo")

    aniversariantes = []
    for pessoa in aniversariantes_qs:
        telefone = pessoa.telefone or ""
        telefone_digits = re.sub(r"\D", "", telefone)
        if telefone_digits and not telefone_digits.startswith("55"):
            telefone_digits = f"55{telefone_digits}"
        aniversariantes.append(
            {
                "id": pessoa.id,
                "nome_completo": pessoa.nome_completo,
                "cargo": pessoa.cargo,
                "telefone_whats": telefone_digits,
            }
        )

    return render(
        request,
        "core/aniversariantes.html",
        {
            "perfil": perfil,
            "aniversariantes": aniversariantes,
            "hoje": hoje,
        },
    )

def cadastro_avisos(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    if request.method == "POST":
        form = AvisoForm(request.POST, request.FILES)
        if form.is_valid():
            aviso = form.save()
            destinatarios = []
            for pessoa in CadastroPerfil.objects.order_by("nome_completo", "id"):
                if pessoa.controle_acesso not in (aviso.visualizacao or []):
                    continue
                telefone = pessoa.telefone or ""
                telefone_digits = re.sub(r"\D", "", telefone)
                if telefone_digits and not telefone_digits.startswith("55"):
                    telefone_digits = f"55{telefone_digits}"
                if not telefone_digits:
                    continue
                AvisoEnvio.objects.get_or_create(
                    aviso=aviso,
                    perfil=pessoa,
                    defaults={"telefone_whats": telefone_digits},
                )
                destinatarios.append(
                    {
                        "nome": pessoa.nome_completo,
                        "cargo": pessoa.cargo,
                        "telefone_whats": telefone_digits,
                    }
                )
            return render(
                request,
                "core/avisos_links.html",
                {"aviso": aviso, "destinatarios": destinatarios},
            )
    else:
        form = AvisoForm()

    return render(request, "core/cadastro_avisos.html", {"form": form})


def avisos_envios_pendentes(request):
    if not request.session.get("perfil_id"):
        return redirect("login")
    if not _require_admin(request):
        return redirect("home")

    pendentes = (
        AvisoEnvio.objects.select_related("aviso", "perfil")
        .filter(enviado_em__isnull=True)
        .order_by("-criado_em", "id")
    )
    return render(request, "core/avisos_envios_pendentes.html", {"pendentes": pendentes})


def aviso_enviar_whatsapp(request, envio_id):
    if not request.session.get("perfil_id"):
        return redirect("login")
    if not _require_admin(request):
        return redirect("home")

    envio = get_object_or_404(AvisoEnvio, pk=envio_id)
    if not envio.enviado_em:
        envio.enviado_em = timezone.now()
        envio.save(update_fields=["enviado_em"])

    mensagem = "Aviso Interno"
    link = f"https://api.whatsapp.com/send?phone={envio.telefone_whats}&text={quote(mensagem)}"
    return redirect(link)


def quadro_avisos_envios_pendentes(request):
    if not request.session.get("perfil_id"):
        return redirect("login")
    if not _require_admin(request):
        return redirect("home")

    pendentes = (
        QuadroAvisoEnvio.objects.select_related("quadro_aviso", "perfil")
        .filter(enviado_em__isnull=True)
        .order_by("-criado_em", "id")
    )
    return render(
        request,
        "core/quadro_avisos_envios_pendentes.html",
        {"pendentes": pendentes},
    )


def quadro_aviso_enviar_whatsapp(request, envio_id):
    if not request.session.get("perfil_id"):
        return redirect("login")
    if not _require_admin(request):
        return redirect("home")

    envio = get_object_or_404(QuadroAvisoEnvio, pk=envio_id)
    if not envio.enviado_em:
        envio.enviado_em = timezone.now()
        envio.save(update_fields=["enviado_em"])

    mensagem = "Aviso Interno"
    link = f"https://api.whatsapp.com/send?phone={envio.telefone_whats}&text={quote(mensagem)}"
    return redirect(link)


def comunicados_envios_pendentes(request):
    if not request.session.get("perfil_id"):
        return redirect("login")
    if not _require_admin(request):
        return redirect("home")

    pendentes = (
        ComunicadoEnvio.objects.select_related("comunicado", "perfil")
        .filter(enviado_em__isnull=True)
        .order_by("-criado_em", "id")
    )
    return render(
        request,
        "core/comunicados_envios_pendentes.html",
        {"pendentes": pendentes},
    )


def comunicado_enviar_whatsapp(request, envio_id):
    if not request.session.get("perfil_id"):
        return redirect("login")
    if not _require_admin(request):
        return redirect("home")

    envio = get_object_or_404(ComunicadoEnvio, pk=envio_id)
    if not envio.enviado_em:
        envio.enviado_em = timezone.now()
        envio.save(update_fields=["enviado_em"])

    mensagem = "Comunicado Interno"
    link = f"https://api.whatsapp.com/send?phone={envio.telefone_whats}&text={quote(mensagem)}"
    return redirect(link)


def eventos_envios_pendentes(request):
    if not request.session.get("perfil_id"):
        return redirect("login")
    if not _require_admin(request):
        return redirect("home")

    pendentes = (
        EventoEnvio.objects.select_related("evento", "perfil")
        .filter(enviado_em__isnull=True)
        .order_by("-criado_em", "id")
    )
    return render(
        request,
        "core/eventos_envios_pendentes.html",
        {"pendentes": pendentes},
    )


def evento_enviar_whatsapp(request, envio_id):
    if not request.session.get("perfil_id"):
        return redirect("login")
    if not _require_admin(request):
        return redirect("home")

    envio = get_object_or_404(EventoEnvio, pk=envio_id)
    if not envio.enviado_em:
        envio.enviado_em = timezone.now()
        envio.save(update_fields=["enviado_em"])

    mensagem = "Evento Interno"
    link = f"https://api.whatsapp.com/send?phone={envio.telefone_whats}&text={quote(mensagem)}"
    return redirect(link)


def lista_fotos(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    postagens = FotoPostagem.objects.order_by("-data_postagem", "-criado_em", "-id")
    perfil_logado = _get_perfil_logado(request)
    is_admin = bool(perfil_logado and perfil_logado.controle_acesso == "admin")
    return render(
        request,
        "core/lista_fotos.html",
        {"postagens": postagens, "is_admin": is_admin},
    )


def cadastro_fotos(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    if request.method == "POST":
        form = FotoPostagemForm(request.POST)
        if form.is_valid():
            postagem = form.save()
            for arquivo in request.FILES.getlist("fotos"):
                FotoAnexo.objects.create(postagem=postagem, imagem=arquivo)
            return redirect("lista_fotos")
    else:
        form = FotoPostagemForm()

    return render(request, "core/cadastro_fotos.html", {"form": form})


def detalhe_fotos(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    postagem = get_object_or_404(FotoPostagem, pk=pk)
    fotos = postagem.fotos.order_by("id")
    return render(
        request,
        "core/detalhe_fotos.html",
        {"postagem": postagem, "fotos": fotos},
    )


def editar_fotos(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")
    if not _require_admin(request):
        return redirect("home")

    postagem = get_object_or_404(FotoPostagem, pk=pk)
    if request.method == "POST":
        form = FotoPostagemForm(request.POST, instance=postagem)
        if form.is_valid():
            form.save()
            for arquivo in request.FILES.getlist("fotos"):
                FotoAnexo.objects.create(postagem=postagem, imagem=arquivo)
            return redirect("lista_fotos")
    else:
        form = FotoPostagemForm(instance=postagem)

    return render(request, "core/cadastro_fotos.html", {"form": form, "postagem": postagem})


def excluir_fotos(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")
    if not _require_admin(request):
        return redirect("home")

    postagem = get_object_or_404(FotoPostagem, pk=pk)
    if request.method == "POST":
        postagem.delete()
        return redirect("lista_fotos")

    return redirect("lista_fotos")


def lista_videos(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    postagens = VideoPostagem.objects.order_by("-data_postagem", "-criado_em", "-id")
    perfil_logado = _get_perfil_logado(request)
    is_admin = bool(perfil_logado and perfil_logado.controle_acesso == "admin")
    return render(
        request,
        "core/lista_videos.html",
        {"postagens": postagens, "is_admin": is_admin},
    )


def cadastro_videos(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    if request.method == "POST":
        form = VideoPostagemForm(request.POST)
        if form.is_valid():
            postagem = form.save()
            for arquivo in request.FILES.getlist("videos"):
                VideoAnexo.objects.create(postagem=postagem, arquivo=arquivo)
            return redirect("lista_videos")
    else:
        form = VideoPostagemForm()

    return render(request, "core/cadastro_videos.html", {"form": form})


def detalhe_videos(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    postagem = get_object_or_404(VideoPostagem, pk=pk)
    videos = postagem.videos.order_by("id")
    return render(
        request,
        "core/detalhe_videos.html",
        {"postagem": postagem, "videos": videos},
    )


def editar_videos(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")
    if not _require_admin(request):
        return redirect("home")

    postagem = get_object_or_404(VideoPostagem, pk=pk)
    if request.method == "POST":
        form = VideoPostagemForm(request.POST, instance=postagem)
        if form.is_valid():
            form.save()
            for arquivo in request.FILES.getlist("videos"):
                VideoAnexo.objects.create(postagem=postagem, arquivo=arquivo)
            return redirect("lista_videos")
    else:
        form = VideoPostagemForm(instance=postagem)

    return render(request, "core/cadastro_videos.html", {"form": form, "postagem": postagem})


def excluir_videos(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")
    if not _require_admin(request):
        return redirect("home")

    postagem = get_object_or_404(VideoPostagem, pk=pk)
    if request.method == "POST":
        postagem.delete()
        return redirect("lista_videos")

    return redirect("lista_videos")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        perfil = CadastroPerfil.objects.filter(email__iexact=email).first()
        if perfil:
            request.session["perfil_id"] = perfil.id
            request.session["perfil_email"] = perfil.email
            return redirect("home")

        messages.error(request, "E-mail não encontrado. Verifique e tente novamente.")

    return render(request, "core/login.html")


def lista_avisos(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    is_admin = bool(perfil and perfil.controle_acesso == "admin")
    if perfil:
        if is_admin:
            avisos = Aviso.objects.order_by("-criado_em", "-id")
        else:
            avisos = _filtrar_por_visualizacao(
                Aviso.objects.order_by("-criado_em", "-id"),
                perfil.controle_acesso,
            )
    else:
        avisos = Aviso.objects.none()
    return render(request, "core/lista_avisos.html", {"avisos": avisos, "is_admin": is_admin})


def detalhe_aviso(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    if not perfil:
        return redirect("login")

    if perfil.controle_acesso == "admin":
        aviso = get_object_or_404(Aviso, pk=pk)
    else:
        aviso = _get_objeto_com_visualizacao(Aviso, pk, perfil.controle_acesso)
    return render(request, "core/detalhe_aviso.html", {"aviso": aviso})


def editar_aviso(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    if not perfil or perfil.controle_acesso != "admin":
        messages.error(request, "Apenas admin pode editar avisos.")
        return redirect("lista_avisos")

    aviso = get_object_or_404(Aviso, pk=pk)
    if request.method == "POST":
        form = AvisoForm(request.POST, request.FILES, instance=aviso)
        if form.is_valid():
            form.save()
            messages.success(request, "Aviso atualizado com sucesso.")
            return redirect("lista_avisos")
    else:
        form = AvisoForm(instance=aviso)

    return render(request, "core/cadastro_avisos.html", {"form": form, "aviso": aviso})


def excluir_aviso(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    if not perfil or perfil.controle_acesso != "admin":
        messages.error(request, "Apenas admin pode excluir avisos.")
        return redirect("lista_avisos")

    aviso = get_object_or_404(Aviso, pk=pk)
    if request.method == "POST":
        aviso.delete()
        messages.success(request, "Aviso excluído com sucesso.")
        return redirect("lista_avisos")

    return redirect("lista_avisos")


def lista_quadro_avisos(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    is_admin = bool(perfil and perfil.controle_acesso == "admin")
    if perfil:
        if is_admin:
            avisos = QuadroAviso.objects.order_by("-criado_em", "-id")
        else:
            avisos = _filtrar_por_visualizacao(
                QuadroAviso.objects.order_by("-criado_em", "-id"),
                perfil.controle_acesso,
            )
    else:
        avisos = QuadroAviso.objects.none()
    return render(request, "core/lista_quadro_avisos.html", {"avisos": avisos, "is_admin": is_admin})


def detalhe_quadro_aviso(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    if not perfil:
        return redirect("login")

    if perfil.controle_acesso == "admin":
        aviso = get_object_or_404(QuadroAviso, pk=pk)
    else:
        aviso = _get_objeto_com_visualizacao(QuadroAviso, pk, perfil.controle_acesso)
    return render(request, "core/detalhe_quadro_aviso.html", {"aviso": aviso})


def cadastro_quadro_avisos(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    if request.method == "POST":
        form = QuadroAvisoForm(request.POST, request.FILES)
        if form.is_valid():
            aviso = form.save()
            destinatarios = []
            for pessoa in CadastroPerfil.objects.order_by("nome_completo", "id"):
                if pessoa.controle_acesso not in (aviso.visualizacao or []):
                    continue
                telefone = pessoa.telefone or ""
                telefone_digits = re.sub(r"\D", "", telefone)
                if telefone_digits and not telefone_digits.startswith("55"):
                    telefone_digits = f"55{telefone_digits}"
                if not telefone_digits:
                    continue
                QuadroAvisoEnvio.objects.get_or_create(
                    quadro_aviso=aviso,
                    perfil=pessoa,
                    defaults={"telefone_whats": telefone_digits},
                )
                destinatarios.append(
                    {
                        "nome": pessoa.nome_completo,
                        "cargo": pessoa.cargo,
                        "telefone_whats": telefone_digits,
                    }
                )
            return render(
                request,
                "core/quadro_avisos_links.html",
                {"aviso": aviso, "destinatarios": destinatarios},
            )
    else:
        form = QuadroAvisoForm()

    return render(request, "core/cadastro_quadro_avisos.html", {"form": form})


def editar_quadro_aviso(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    if not perfil or perfil.controle_acesso != "admin":
        messages.error(request, "Apenas admin pode editar avisos.")
        return redirect("lista_quadro_avisos")

    aviso = get_object_or_404(QuadroAviso, pk=pk)
    if request.method == "POST":
        form = QuadroAvisoForm(request.POST, request.FILES, instance=aviso)
        if form.is_valid():
            form.save()
            messages.success(request, "Aviso atualizado com sucesso.")
            return redirect("lista_quadro_avisos")
    else:
        form = QuadroAvisoForm(instance=aviso)

    return render(request, "core/cadastro_quadro_avisos.html", {"form": form, "aviso": aviso})


def excluir_quadro_aviso(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    if not perfil or perfil.controle_acesso != "admin":
        messages.error(request, "Apenas admin pode excluir avisos.")
        return redirect("lista_quadro_avisos")

    aviso = get_object_or_404(QuadroAviso, pk=pk)
    if request.method == "POST":
        aviso.delete()
        messages.success(request, "Aviso excluído com sucesso.")
        return redirect("lista_quadro_avisos")

    return redirect("lista_quadro_avisos")


def lista_comunicados(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    is_admin = bool(perfil and perfil.controle_acesso == "admin")
    if perfil:
        if is_admin:
            comunicados = Comunicado.objects.order_by("-criado_em", "-id")
        else:
            comunicados = _filtrar_por_visualizacao(
                Comunicado.objects.order_by("-criado_em", "-id"),
                perfil.controle_acesso,
            )
    else:
        comunicados = Comunicado.objects.none()
    return render(request, "core/lista_comunicados.html", {"comunicados": comunicados, "is_admin": is_admin})


def detalhe_comunicado(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    if not perfil:
        return redirect("login")

    if perfil.controle_acesso == "admin":
        comunicado = get_object_or_404(Comunicado, pk=pk)
    else:
        comunicado = _get_objeto_com_visualizacao(Comunicado, pk, perfil.controle_acesso)
    return render(request, "core/detalhe_comunicado.html", {"comunicado": comunicado})


def cadastro_comunicados(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    if request.method == "POST":
        form = ComunicadoForm(request.POST, request.FILES)
        if form.is_valid():
            comunicado = form.save()
            destinatarios = []
            for pessoa in CadastroPerfil.objects.order_by("nome_completo", "id"):
                if pessoa.controle_acesso not in (comunicado.visualizacao or []):
                    continue
                telefone = pessoa.telefone or ""
                telefone_digits = re.sub(r"\D", "", telefone)
                if telefone_digits and not telefone_digits.startswith("55"):
                    telefone_digits = f"55{telefone_digits}"
                if not telefone_digits:
                    continue
                ComunicadoEnvio.objects.get_or_create(
                    comunicado=comunicado,
                    perfil=pessoa,
                    defaults={"telefone_whats": telefone_digits},
                )
                destinatarios.append(
                    {
                        "nome": pessoa.nome_completo,
                        "cargo": pessoa.cargo,
                        "telefone_whats": telefone_digits,
                    }
                )
            return render(
                request,
                "core/comunicados_links.html",
                {"comunicado": comunicado, "destinatarios": destinatarios},
            )
    else:
        form = ComunicadoForm(initial={"data_emissao": timezone.localdate()})

    return render(request, "core/cadastro_comunicados.html", {"form": form})


def editar_comunicado(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    if not perfil or perfil.controle_acesso != "admin":
        messages.error(request, "Apenas admin pode editar comunicados.")
        return redirect("lista_comunicados")

    comunicado = get_object_or_404(Comunicado, pk=pk)
    if request.method == "POST":
        form = ComunicadoForm(request.POST, request.FILES, instance=comunicado)
        if form.is_valid():
            form.save()
            messages.success(request, "Comunicado atualizado com sucesso.")
            return redirect("lista_comunicados")
    else:
        form = ComunicadoForm(instance=comunicado)

    return render(request, "core/cadastro_comunicados.html", {"form": form, "comunicado": comunicado})


def excluir_comunicado(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    if not perfil or perfil.controle_acesso != "admin":
        messages.error(request, "Apenas admin pode excluir comunicados.")
        return redirect("lista_comunicados")

    comunicado = get_object_or_404(Comunicado, pk=pk)
    if request.method == "POST":
        comunicado.delete()
        messages.success(request, "Comunicado excluído com sucesso.")
        return redirect("lista_comunicados")

    return redirect("lista_comunicados")


def lista_eventos(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    is_admin = bool(perfil and perfil.controle_acesso == "admin")
    if perfil:
        if is_admin:
            eventos = Evento.objects.order_by("-data_evento", "-horario_evento", "-id")
        else:
            eventos = _filtrar_por_visualizacao(
                Evento.objects.order_by("-data_evento", "-horario_evento", "-id"),
                perfil.controle_acesso,
            )
    else:
        eventos = Evento.objects.none()
    return render(request, "core/lista_eventos.html", {"eventos": eventos, "is_admin": is_admin})


def detalhe_evento(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    if not perfil:
        return redirect("login")

    if perfil.controle_acesso == "admin":
        evento = get_object_or_404(Evento, pk=pk)
    else:
        evento = _get_objeto_com_visualizacao(Evento, pk, perfil.controle_acesso)
    return render(request, "core/detalhe_evento.html", {"evento": evento})


def _filtrar_por_visualizacao(queryset, controle_acesso):
    if connection.vendor == "sqlite":
        ids = [
            obj.id
            for obj in queryset
            if controle_acesso in (obj.visualizacao or [])
        ]
        return queryset.filter(id__in=ids)
    return queryset.filter(visualizacao__contains=[controle_acesso])


def _get_objeto_com_visualizacao(model, pk, controle_acesso):
    if connection.vendor == "sqlite":
        obj = get_object_or_404(model, pk=pk)
        if controle_acesso in (obj.visualizacao or []):
            return obj
        return get_object_or_404(model, pk=0)
    return get_object_or_404(model, pk=pk, visualizacao__contains=[controle_acesso])


def cadastro_eventos(request):
    if not request.session.get("perfil_id"):
        return redirect("login")

    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save()
            destinatarios = []
            for pessoa in CadastroPerfil.objects.order_by("nome_completo", "id"):
                if pessoa.controle_acesso not in (evento.visualizacao or []):
                    continue
                telefone = pessoa.telefone or ""
                telefone_digits = re.sub(r"\D", "", telefone)
                if telefone_digits and not telefone_digits.startswith("55"):
                    telefone_digits = f"55{telefone_digits}"
                if not telefone_digits:
                    continue
                EventoEnvio.objects.get_or_create(
                    evento=evento,
                    perfil=pessoa,
                    defaults={"telefone_whats": telefone_digits},
                )
                destinatarios.append(
                    {
                        "nome": pessoa.nome_completo,
                        "cargo": pessoa.cargo,
                        "telefone_whats": telefone_digits,
                    }
                )
            return render(
                request,
                "core/eventos_links.html",
                {"evento": evento, "destinatarios": destinatarios},
            )
    else:
        form = EventoForm()

    return render(request, "core/cadastro_eventos.html", {"form": form})


def editar_evento(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    if not perfil or perfil.controle_acesso != "admin":
        messages.error(request, "Apenas admin pode editar eventos.")
        return redirect("lista_eventos")

    evento = get_object_or_404(Evento, pk=pk)
    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento atualizado com sucesso.")
            return redirect("lista_eventos")
    else:
        form = EventoForm(instance=evento)

    return render(request, "core/cadastro_eventos.html", {"form": form, "evento": evento})


def excluir_evento(request, pk):
    if not request.session.get("perfil_id"):
        return redirect("login")

    perfil = CadastroPerfil.objects.filter(id=request.session.get("perfil_id")).first()
    if not perfil or perfil.controle_acesso != "admin":
        messages.error(request, "Apenas admin pode excluir eventos.")
        return redirect("lista_eventos")

    evento = get_object_or_404(Evento, pk=pk)
    if request.method == "POST":
        evento.delete()
        messages.success(request, "Evento excluído com sucesso.")
        return redirect("lista_eventos")

    return redirect("lista_eventos")
