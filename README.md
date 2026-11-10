# VH.Medeiros — Portfólio

Portfólio pessoal de desenvolvedor Python backend, no ar em **[vhmedeiros.dev.br](https://vhmedeiros.dev.br)**.

O HTML é renderizado no servidor pelo Django, e as interações parciais (filtro de projetos e formulário de contato) usam HTMX. Não há framework JavaScript nem build com Node. Os projetos são cadastrados pelo Django Admin, e cada push na `main` publica o site automaticamente numa VM da Oracle Cloud.

**Stack:** Python 3.11 · Django 4.2 · HTMX · Tailwind CSS 3 · SQLite · Gunicorn · Nginx · Docker Compose · GitHub Actions · Oracle Cloud

---

## Sumário

1. [Arquitetura](#arquitetura)
2. [Rodando localmente](#rodando-localmente)
3. [Variáveis de ambiente](#variáveis-de-ambiente)
4. [CSS com Tailwind](#css-com-tailwind)
5. [Conteúdo pelo Admin](#conteúdo-pelo-admin)
6. [Estrutura do projeto](#estrutura-do-projeto)
7. [Deploy](#deploy)
8. [Comandos úteis](#comandos-úteis)

---

## Arquitetura

```
navegador ──► Nginx :443 (HTTPS, Let's Encrypt; :80 redireciona) ──► /static/, /media/
                   └──────► Gunicorn :8000 (só rede interna) ──► Django ──► SQLite
                                                 └──────► Gmail SMTP (aviso do formulário de contato)
```

| App | Responsabilidade |
|---|---|
| `core` | Página inicial (até 3 projetos em destaque) e layout base (`base.html`) |
| `projects` | Modelos `Tag`, `Project` e `ProjectImage`, lista com filtro por tag (HTMX) e página de detalhe com descrição em Markdown |
| `contact` | Formulário de contato via HTMX. Salva um `ContactMessage` e envia um e-mail de aviso |

Quando a requisição vem do HTMX (`request.htmx`, via `django-htmx`), as views devolvem só um *partial* (`templates/<app>/partials/`) em vez da página inteira.

---

## Rodando localmente

**Pré-requisito:** Docker com Docker Compose.

```bash
# 1. Crie o .env na raiz (veja a seção "Variáveis de ambiente")
cat > .env <<'EOF'
DEBUG=True
SECRET_KEY=qualquer-string-longa
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

# 2. Suba os containers (o arquivo dev troca o Nginx HTTPS de produção por um só HTTP)
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# 3. Em outro terminal: banco e usuário do admin
docker exec portfolio_web python manage.py migrate
docker exec -it portfolio_web python manage.py createsuperuser
```

| O quê | URL |
|---|---|
| Site (via Nginx, só HTTP) | http://localhost |
| Site (direto no Gunicorn) | http://localhost:8000 |
| Admin | http://localhost/admin |

> A pasta do projeto é montada dentro do container (`.:/app`), então mudanças em templates e no CSS aparecem ao recarregar a página. O Gunicorn não tem *auto-reload*: depois de mudar código Python, rode `docker compose restart web`.

---

## Variáveis de ambiente

Todas são lidas em `config/settings.py` e ficam no `.env`, que **não** vai para o git.

| Variável | Padrão | Observação |
|---|---|---|
| `SECRET_KEY` | chave insegura de desenvolvimento | Obrigatória em produção |
| `DEBUG` | `True` | Só liga com o valor exato `True`. Em produção use `False` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Lista separada por vírgula |
| `EMAIL_HOST_USER` | — | Conta Gmail que envia **e recebe** o aviso do formulário de contato |
| `EMAIL_HOST_PASSWORD` | — | Senha de app do Gmail (não a senha da conta) |

Sem as variáveis de e-mail, o formulário continua funcionando: a mensagem é salva no banco e o envio do aviso falha em silêncio.

---

## CSS com Tailwind

O CSS é compilado pelo **executável standalone do Tailwind v3**, que não precisa de Node:

| Arquivo | Papel |
|---|---|
| `assets/tailwind.css` | Fonte: diretivas do Tailwind e CSS customizado (grade do hero, animações, foco) |
| `tailwind.config.js` | Tema (cores `accent` e `surface`, fontes) e plugin de tipografia |
| `core/static/core/css/site.css` | **Gerado e versionado.** É o arquivo que o site carrega |

O `site.css` vai para o git porque o deploy é só um `git pull`. **Sempre que mudar classes nos templates, gere o CSS de novo:**

```bash
# instalar uma vez (Linux x64)
curl -fsSL -o ~/.local/bin/tailwindcss \
  https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.17/tailwindcss-linux-x64
chmod +x ~/.local/bin/tailwindcss

# gerar o CSS (use --watch enquanto edita)
tailwindcss -i assets/tailwind.css -o core/static/core/css/site.css --minify
```

Não edite o `site.css` à mão. CSS novo vai em `assets/tailwind.css`, dentro de `@layer components`. A exceção são as classes que só aparecem em tempo de execução, como `.htmx-request`: essas ficam fora de qualquer `@layer`, senão o Tailwind as remove do CSS final.

---

## Conteúdo pelo Admin

Todo o conteúdo de projetos é gerenciado em **/admin** e não fica no código.

**Tags** (`Admin → Tags`): tecnologias ou categorias usadas no filtro da página de projetos. O campo `color` existe no modelo, mas o visual atual exibe todas as tags em tom neutro.

**Projetos** (`Admin → Projects`):

| Campo | Uso |
|---|---|
| `title` / `slug` | Nome e URL (`/projects/<slug>/`). O slug é preenchido automaticamente |
| `short_description` | Resumo exibido nos cards e no topo da página do projeto |
| `full_description` | Texto completo em **Markdown** (tabelas, blocos de código e quebras de linha) |
| `tags` | Tags do projeto |
| `thumbnail` | Imagem de capa (recomendado 1280×720) |
| `demo_url` / `repo_url` | Links opcionais de demo e repositório |
| `featured` | Exibe na home. Aparecem os 3 mais recentes marcados |
| Imagens (inline) | Galeria "Telas do sistema", com legenda e ordem |

> O Markdown é renderizado sem sanitização, então só usuários do admin devem escrever esse conteúdo.

**Mensagens de contato** (`Admin → Contact messages`): tudo que chega pelo formulário. Marque `read` nas que já foram respondidas.

---

## Estrutura do projeto

```
portfolio/
├── config/                 # settings, urls e wsgi
├── core/
│   ├── templates/core/     # base.html (layout) e home.html
│   └── static/core/
│       ├── css/site.css    # CSS gerado pelo Tailwind (não editar)
│       └── images/         # logo e favicon
├── projects/
│   ├── models.py           # Tag, Project, ProjectImage
│   ├── templatetags/       # filtro render_markdown
│   └── templates/projects/
│       ├── project_list.html, project_detail.html
│       └── partials/       # project_grid.html (HTMX) e project_card.html
├── contact/
│   ├── models.py, forms.py # ContactMessage e ContactForm
│   └── templates/contact/  # contact.html e partials/form.html (HTMX)
├── assets/tailwind.css     # fonte do CSS
├── tailwind.config.js
├── nginx/
│   ├── nginx.conf          # produção: HTTPS, proxy reverso, estáticos e mídia
│   └── nginx.dev.conf      # desenvolvimento: só HTTP
├── Dockerfile
├── docker-compose.yml      # produção
├── docker-compose.dev.yml  # ajustes para rodar localmente
└── .github/workflows/deploy.yml
```

---

## Deploy

O deploy é automático: **todo push na `main` publica em produção** pelo workflow `.github/workflows/deploy.yml`, que:

1. Conecta por SSH na VM da Oracle Cloud.
2. Garante que `EMAIL_HOST_USER` e `EMAIL_HOST_PASSWORD` existam no `.env` da VM. Só adiciona as que faltam, ou seja, **não atualiza** valores que já existem.
3. Roda `git pull`, `docker compose up --build -d`, `migrate` e `collectstatic`.

**Secrets do repositório** (Settings → Secrets and variables → Actions):

| Secret | Conteúdo |
|---|---|
| `SSH_PRIVATE_KEY` | Chave privada com acesso à VM |
| `SSH_HOST` / `SSH_USER` | Endereço e usuário da VM |
| `DEPLOY_PATH` | Pasta do projeto na VM |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | Credenciais do Gmail |

**Primeira instalação numa VM nova:** instale Docker e o plugin Compose, libere as portas 80 e 443 na VCN e no firewall, clone o repositório em `DEPLOY_PATH` e crie o `.env` de produção:

```env
DEBUG=False
SECRET_KEY=uma-string-longa-e-aleatoria
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
```

O HTTPS usa certificados do **Let's Encrypt** gerados na própria VM: o Nginx lê `/etc/letsencrypt` do host, que é montado no container. Emita o certificado (por exemplo com `certbot certonly --standalone`, antes de subir o Nginx) e garanta a renovação automática.

Depois, crie o usuário do admin uma única vez: `docker exec -it portfolio_web python manage.py createsuperuser`.

> O banco SQLite (`db.sqlite3`) e a pasta `media/` ficam na VM e não vão para o git. Faça backup deles.
>
> **Não edite arquivos versionados direto na VM.** Qualquer mudança local faz o `git pull` do deploy falhar. Mude no repositório e faça push.

---

## Comandos úteis

```bash
docker compose up -d                 # sobe em background
docker compose down                  # para tudo
docker compose logs -f web           # logs do Django/Gunicorn
docker compose restart web           # recarrega depois de mudar código Python

docker exec portfolio_web python manage.py migrate
docker exec portfolio_web python manage.py makemigrations
docker exec portfolio_web python manage.py collectstatic --noinput
docker exec -it portfolio_web python manage.py createsuperuser
docker exec -it portfolio_web python manage.py shell

ruff check . && ruff format .        # lint e formatação (config em ruff.toml)
```
