# Fampertec (Django)

Tela inicial com um icone/atalho chamado **Cadastro de Perfil**.

## Rodar (Windows / PowerShell)

1) Criar e ativar venv:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2) Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3) Subir o servidor:

```powershell
python manage.py migrate
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`.

