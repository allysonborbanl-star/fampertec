from django.db import models
from django.utils import timezone


class Aviso(models.Model):
    VISUALIZACAO_CHOICES = [
        ("admin", "Admin"),
        ("coordenador", "Coordenador"),
        ("protocolo", "Protocolo"),
        ("professor", "Professor"),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    link = models.URLField(blank=True)
    data_fim_publicacao = models.DateField()
    imagem_capa = models.ImageField(upload_to="avisos/", blank=True, null=True)
    imagem_1 = models.ImageField(upload_to="avisos/", blank=True, null=True)
    documento = models.FileField(upload_to="avisos/", blank=True, null=True)
    visualizacao = models.JSONField(default=list)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.titulo

    @property
    def visualizacao_display(self) -> str:
        labels = dict(self.VISUALIZACAO_CHOICES)
        return ", ".join(labels.get(item, item) for item in (self.visualizacao or []))


class AvisoEnvio(models.Model):
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("LIDO", "Lido"),
    ]

    aviso = models.ForeignKey(Aviso, on_delete=models.CASCADE, related_name="envios")
    perfil = models.ForeignKey("perfil.CadastroPerfil", on_delete=models.CASCADE)
    telefone_whats = models.CharField(max_length=20)
    enviado_em = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDENTE")
    lido_em = models.DateTimeField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("aviso", "perfil")]


class QuadroAviso(models.Model):
    VISUALIZACAO_CHOICES = [
        ("admin", "Admin"),
        ("coordenador", "Coordenador"),
        ("protocolo", "Protocolo"),
        ("professor", "Professor"),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    link = models.URLField(blank=True)
    data_fim_publicacao = models.DateField()
    imagem_capa = models.ImageField(upload_to="quadro_avisos/", blank=True, null=True)
    imagem_1 = models.ImageField(upload_to="quadro_avisos/", blank=True, null=True)
    documento = models.FileField(upload_to="quadro_avisos/", blank=True, null=True)
    visualizacao = models.JSONField(default=list)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.titulo

    @property
    def visualizacao_display(self) -> str:
        labels = dict(self.VISUALIZACAO_CHOICES)
        return ", ".join(labels.get(item, item) for item in (self.visualizacao or []))


class QuadroAvisoEnvio(models.Model):
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("LIDO", "Lido"),
    ]

    quadro_aviso = models.ForeignKey(QuadroAviso, on_delete=models.CASCADE, related_name="envios")
    perfil = models.ForeignKey("perfil.CadastroPerfil", on_delete=models.CASCADE)
    telefone_whats = models.CharField(max_length=20)
    enviado_em = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDENTE")
    lido_em = models.DateTimeField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("quadro_aviso", "perfil")]


class Comunicado(models.Model):
    VISUALIZACAO_CHOICES = [
        ("admin", "Admin"),
        ("coordenador", "Coordenador"),
        ("protocolo", "Protocolo"),
        ("professor", "Professor"),
    ]

    numero_comunicado = models.CharField(max_length=40)
    data_emissao = models.DateField(default=timezone.localdate)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    link = models.URLField(blank=True)
    imagem_capa = models.ImageField(upload_to="comunicados/", blank=True, null=True)
    documento_1 = models.FileField(upload_to="comunicados/", blank=True, null=True)
    documento_2 = models.FileField(upload_to="comunicados/", blank=True, null=True)
    visualizacao = models.JSONField(default=list)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.numero_comunicado} - {self.titulo}"

    @property
    def visualizacao_display(self) -> str:
        labels = dict(self.VISUALIZACAO_CHOICES)
        return ", ".join(labels.get(item, item) for item in (self.visualizacao or []))


class ComunicadoEnvio(models.Model):
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("LIDO", "Lido"),
    ]

    comunicado = models.ForeignKey(Comunicado, on_delete=models.CASCADE, related_name="envios")
    perfil = models.ForeignKey("perfil.CadastroPerfil", on_delete=models.CASCADE)
    telefone_whats = models.CharField(max_length=20)
    enviado_em = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDENTE")
    lido_em = models.DateTimeField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("comunicado", "perfil")]


class Evento(models.Model):
    VISUALIZACAO_CHOICES = [
        ("admin", "Admin"),
        ("coordenador", "Coordenador"),
        ("protocolo", "Protocolo"),
        ("professor", "Professor"),
    ]

    data_evento = models.DateField()
    horario_evento = models.TimeField()
    evento = models.CharField(max_length=200)
    local = models.CharField(max_length=200)
    imagem_capa = models.ImageField(upload_to="eventos/", blank=True, null=True)
    imagem_1 = models.ImageField(upload_to="eventos/", blank=True, null=True)
    documento = models.FileField(upload_to="eventos/", blank=True, null=True)
    descricao = models.TextField()
    visualizacao = models.JSONField(default=list)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.evento

    @property
    def visualizacao_display(self) -> str:
        labels = dict(self.VISUALIZACAO_CHOICES)
        return ", ".join(labels.get(item, item) for item in (self.visualizacao or []))


class EventoEnvio(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="envios")
    perfil = models.ForeignKey("perfil.CadastroPerfil", on_delete=models.CASCADE)
    telefone_whats = models.CharField(max_length=20)
    enviado_em = models.DateTimeField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("evento", "perfil")]


class FotoPostagem(models.Model):
    data_postagem = models.DateField(default=timezone.localdate)
    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Fotos {self.data_postagem:%d/%m/%Y}"


class FotoAnexo(models.Model):
    postagem = models.ForeignKey(FotoPostagem, on_delete=models.CASCADE, related_name="fotos")
    imagem = models.ImageField(upload_to="fotos/")
    criado_em = models.DateTimeField(auto_now_add=True)


class VideoPostagem(models.Model):
    data_postagem = models.DateField(default=timezone.localdate)
    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Vídeos {self.data_postagem:%d/%m/%Y}"


class VideoAnexo(models.Model):
    postagem = models.ForeignKey(VideoPostagem, on_delete=models.CASCADE, related_name="videos")
    arquivo = models.FileField(upload_to="videos/")
    criado_em = models.DateTimeField(auto_now_add=True)
