from django import forms

from .models import CadastroPerfil


class ProfileForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        input_formats=["%Y-%m-%d", "%d/%m/%Y"],
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
    )

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
