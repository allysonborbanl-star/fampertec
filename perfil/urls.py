from django.urls import path

from . import views

urlpatterns = [
    path("", views.lista_perfis, name="lista_perfis"),
    path("detalhe/<int:pk>/", views.detalhe_perfil, name="detalhe_perfil"),
    path("cadastro/", views.cadastro_perfil, name="cadastro_perfil"),
    path("editar/<int:pk>/", views.editar_perfil, name="editar_perfil"),
    path("excluir/<int:pk>/", views.excluir_perfil, name="excluir_perfil"),
]
