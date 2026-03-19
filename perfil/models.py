from django.db import models


class CadastroPerfil(models.Model):
    CONTROLE_ACESSO_CHOICES = [
        ("admin", "Admin"),
        ("coordenador", "Coordenador"),
        ("protocolo", "Protocolo"),
        ("professor", "Professor"),
    ]

    nome_completo = models.CharField(max_length=120)
    email = models.EmailField()
    telefone = models.CharField(max_length=30, blank=True)
    cargo = models.CharField(max_length=80, blank=True, default="")
    data_nascimento = models.DateField()
    controle_acesso = models.CharField(max_length=20, choices=CONTROLE_ACESSO_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cadastr_perfil"

    def __str__(self) -> str:
        return self.nome_completo
