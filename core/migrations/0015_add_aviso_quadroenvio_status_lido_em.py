from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_add_comunicadoenvio_status_lido_em"),
    ]

    operations = [
        migrations.AddField(
            model_name="avisoenvio",
            name="status",
            field=models.CharField(
                choices=[("PENDENTE", "Pendente"), ("LIDO", "Lido")],
                default="PENDENTE",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="avisoenvio",
            name="lido_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="quadroavisoenvio",
            name="status",
            field=models.CharField(
                choices=[("PENDENTE", "Pendente"), ("LIDO", "Lido")],
                default="PENDENTE",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="quadroavisoenvio",
            name="lido_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
