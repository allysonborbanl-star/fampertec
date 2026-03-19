from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_create_fotos"),
    ]

    operations = [
        migrations.CreateModel(
            name="VideoPostagem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("data_postagem", models.DateField(default=django.utils.timezone.localdate)),
                ("descricao", models.TextField()),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="VideoAnexo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("arquivo", models.FileField(upload_to="videos/")),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                (
                    "postagem",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="videos", to="core.videopostagem"),
                ),
            ],
        ),
    ]
