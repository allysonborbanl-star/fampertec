from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_create_aviso_envio"),
        ("perfil", "0002_add_cargo_to_cadastroperfil"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuadroAvisoEnvio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("telefone_whats", models.CharField(max_length=20)),
                ("enviado_em", models.DateTimeField(blank=True, null=True)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                (
                    "perfil",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="perfil.cadastroperfil"),
                ),
                (
                    "quadro_aviso",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="envios",
                        to="core.quadroaviso",
                    ),
                ),
            ],
            options={
                "unique_together": {("quadro_aviso", "perfil")},
            },
        ),
    ]
