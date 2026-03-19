from django import forms

from .models import CadastroPerfil


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CadastroPerfil
        fields = [
            "nome_completo",
            "email",
            "telefone",
            "cargo",
            "data_nascimento",
            "controle_acesso",
        ]
        labels = {
            "nome_completo": "Nome completo",
            "email": "E-mail",
            "telefone": "Telefone",
            "cargo": "Cargo",
            "data_nascimento": "Data de nascimento",
            "controle_acesso": "Controle de acesso",
        }
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date"}),
        }
