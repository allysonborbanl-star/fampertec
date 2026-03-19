from django.db import migrations
import os
import datetime


def create_admin_from_env(apps, schema_editor):
    CadastroPerfil = apps.get_model("perfil", "CadastroPerfil")

    email = os.getenv("ADMIN_EMAIL")
    if not email:
        return

    email = email.strip().lower()
    if not email:
        return

    if CadastroPerfil.objects.filter(email__iexact=email).exists():
        return

    nome = os.getenv("ADMIN_NOME", "Allyson Borba")
    cargo = os.getenv("ADMIN_CARGO", "Administrador")
    telefone = os.getenv("ADMIN_TELEFONE", "")
    data_nascimento = os.getenv("ADMIN_DATA_NASCIMENTO", "1990-01-01")

    try:
        data_nascimento = datetime.date.fromisoformat(data_nascimento)
    except ValueError:
        data_nascimento = datetime.date(1990, 1, 1)

    CadastroPerfil.objects.create(
        nome_completo=nome,
        email=email,
        telefone=telefone,
        data_nascimento=data_nascimento,
        controle_acesso="admin",
        cargo=cargo,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0012_create_videos"),
        ("perfil", "0002_add_cargo_to_cadastroperfil"),
    ]

    operations = [
        migrations.RunPython(create_admin_from_env, migrations.RunPython.noop),
    ]
