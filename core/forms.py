from django import forms
from django.utils import timezone

from .models import Aviso, QuadroAviso, Comunicado, Evento, FotoPostagem, VideoPostagem


class AvisoForm(forms.ModelForm):
    visualizacao = forms.MultipleChoiceField(
        choices=Aviso.VISUALIZACAO_CHOICES,
        label="Visualização",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Aviso
        fields = [
            "titulo",
            "descricao",
            "link",
            "data_fim_publicacao",
            "imagem_capa",
            "visualizacao",
        ]
        labels = {
            "titulo": "Título",
            "descricao": "Descrição",
            "link": "Link",
            "data_fim_publicacao": "Data fim publicação",
            "imagem_capa": "Imagem de capa",
        }
        widgets = {
            "data_fim_publicacao": forms.DateInput(attrs={"type": "date"}),
        }


class QuadroAvisoForm(forms.ModelForm):
    visualizacao = forms.MultipleChoiceField(
        choices=QuadroAviso.VISUALIZACAO_CHOICES,
        label="Visualização",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = QuadroAviso
        fields = [
            "titulo",
            "descricao",
            "link",
            "data_fim_publicacao",
            "imagem_capa",
            "visualizacao",
        ]
        labels = {
            "titulo": "Título",
            "descricao": "Descrição",
            "link": "Link",
            "data_fim_publicacao": "Data fim publicação",
            "imagem_capa": "Imagem de capa",
        }
        widgets = {
            "data_fim_publicacao": forms.DateInput(attrs={"type": "date"}),
        }


class ComunicadoForm(forms.ModelForm):
    visualizacao = forms.MultipleChoiceField(
        choices=Comunicado.VISUALIZACAO_CHOICES,
        label="Visualização",
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance or not self.instance.pk:
            self.fields["data_emissao"].initial = timezone.localdate()

    class Meta:
        model = Comunicado
        fields = [
            "numero_comunicado",
            "data_emissao",
            "titulo",
            "descricao",
            "link",
            "imagem_capa",
            "visualizacao",
        ]
        labels = {
            "numero_comunicado": "Número do comunicado",
            "data_emissao": "Data emissão",
            "titulo": "Título",
            "descricao": "Descrição",
            "link": "Link",
            "imagem_capa": "Imagem de capa",
            "visualizacao": "Visualização",
        }
        widgets = {
            "data_emissao": forms.DateInput(attrs={"type": "date"}),
        }


class EventoForm(forms.ModelForm):
    visualizacao = forms.MultipleChoiceField(
        choices=Evento.VISUALIZACAO_CHOICES,
        label="Visualização",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Evento
        fields = [
            "data_inicio",
            "horario_inicio",
            "data_final",
            "horario_final",
            "evento",
            "local",
            "imagem_capa",
            "descricao",
            "visualizacao",
        ]
        labels = {
            "data_inicio": "Data Início",
            "horario_inicio": "Horário Início",
            "data_final": "Data Final",
            "horario_final": "Horário Final",
            "evento": "Evento",
            "local": "Local",
            "imagem_capa": "Imagem de capa",
            "descricao": "Descrição",
        }
        widgets = {
            "data_inicio": forms.DateInput(attrs={"type": "date"}),
            "horario_inicio": forms.TimeInput(attrs={"type": "time"}),
            "data_final": forms.DateInput(attrs={"type": "date"}),
            "horario_final": forms.TimeInput(attrs={"type": "time"}),
        }


class FotoPostagemForm(forms.ModelForm):
    class Meta:
        model = FotoPostagem
        fields = ["data_postagem", "descricao"]
        labels = {
            "data_postagem": "Data postagem",
            "descricao": "Descrição",
        }
        widgets = {
            "data_postagem": forms.DateInput(attrs={"type": "date"}),
        }


class VideoPostagemForm(forms.ModelForm):
    class Meta:
        model = VideoPostagem
        fields = ["data_postagem", "descricao"]
        labels = {
            "data_postagem": "Data postagem",
            "descricao": "Descrição",
        }
        widgets = {
            "data_postagem": forms.DateInput(attrs={"type": "date"}),
        }
