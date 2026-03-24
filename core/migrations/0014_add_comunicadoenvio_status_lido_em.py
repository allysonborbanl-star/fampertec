from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_create_admin_from_env"),
    ]

    operations = [
        migrations.AddField(
            model_name="comunicadoenvio",
            name="status",
            field=models.CharField(
                choices=[("PENDENTE", "Pendente"), ("LIDO", "Lido")],
                default="PENDENTE",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="comunicadoenvio",
            name="lido_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
