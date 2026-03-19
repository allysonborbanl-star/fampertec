from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("perfil", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cadastroperfil",
            name="cargo",
            field=models.CharField(blank=True, default="", max_length=80),
        ),
    ]
