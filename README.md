# Aprendendo Django - Chat em Tempo Real

Projeto de estudo com Django para praticar:
- Django
- Python
- WebSocket e HTTP
- Banco de dados SQLite

## Stack

- Python 3.11
- Django 5.2
- Channels 4
- Daphne 4
- SQLite

## Como rodar localmente

1. Clone o repositorio
2. Crie e ative o ambiente virtual
3. Instale as dependencias
4. Rode as migracoes
5. Inicie o servidor

### Windows (PowerShell)

```powershell
cd Projeto_aprender_Django
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python aprender\manage.py migrate
python aprender\manage.py runserver
```

Abra no navegador:
- `http://127.0.0.1:8000/`

## Fluxo de uso

1. Faca login com um usuario existente (Henrique, 1234 ou Luiza, 1234)
3. Envie mensagens e acompanhe atualizacao em tempo real

## Comandos uteis

```powershell
# criar usuario admin
python aprender\manage.py createsuperuser

```

## Obs

- `aprender/db.sqlite3` fica versionado de proposito para facilitar testes entre maquinas.
- A pasta `Notas Pessoais/` tambem fica versionada de proposito.
