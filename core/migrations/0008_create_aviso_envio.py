from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_create_evento"),
        ("perfil", "0002_add_cargo_to_cadastroperfil"),
    ]

    operations = [
        migrations.CreateModel(
            name="AvisoEnvio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("telefone_whats", models.CharField(max_length=20)),
                ("enviado_em", models.DateTimeField(blank=True, null=True)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                (
                    "aviso",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="envios", to="core.aviso"),
                ),
                ("perfil", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="perfil.cadastroperfil")),
            ],
            options={
                "unique_together": {("aviso", "perfil")},
            },
        ),
    ]
