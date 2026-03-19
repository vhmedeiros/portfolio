# 🗂️ Portfolio — vhmedeiros

Stack: **Django 4.2 · HTMX · Tailwind CSS · AOS · Docker · Nginx · SQLite**

---

## 📋 Índice

1. [Rodando localmente](#-rodando-localmente)
2. [Acessos importantes](#-acessos-importantes)
3. [Como personalizar o site](#-como-personalizar-o-site)
4. [Gerenciando projetos pelo Admin](#-gerenciando-projetos-pelo-admin)
5. [Estrutura do projeto](#-estrutura-do-projeto)
6. [Comandos úteis do Docker](#-comandos-úteis-do-docker)
7. [Deploy na Oracle Cloud](#-deploy-na-oracle-cloud)

---

## 🚀 Rodando localmente

### Pré-requisitos
- Docker Desktop instalado e rodando

### Passo a passo

```bash
# 1. Entre na pasta do projeto
cd portfolio

# 2. Configure o ambiente local
# Edite o .env e deixe assim:
# DEBUG=True
# SECRET_KEY=qualquer-string-longa-aqui
# ALLOWED_HOSTS=localhost,127.0.0.1

# 3. Suba os containers
docker compose up --build

# 4. Em outro terminal, crie as tabelas
docker exec portfolio_web python manage.py migrate

# 5. Crie seu usuário administrador
docker exec -it portfolio_web python manage.py createsuperuser

# 6. Acesse o site
# http://localhost
```

---

## 🔑 Acessos importantes

| O quê | URL |
|---|---|
| Site (home) | http://localhost |
| Lista de projetos | http://localhost/projects/ |
| Formulário de contato | http://localhost/contact/ |
| Painel administrativo | http://localhost/admin |

---

## 🎨 Como personalizar o site

### 1. Seus dados pessoais (hero da home)

Edite o arquivo `core/templates/core/home.html`.

**Texto principal:**
```html
<!-- Linha ~47 -->
<h1 ...>
  Construo soluções.<br/>
  <span class="text-brand-400">Automatizo</span> o resto.
</h1>
```
Troque pelo seu próprio headline.

**Parágrafo de apresentação:**
```html
<!-- Linha ~54 -->
<p ...>
  Desenvolvedor Full Stack especializado em automações com ...
</p>
```

**Card de stack (bloco de código visual):**
```html
<!-- Linha ~75 -->
<code>
  "backend":   ["Python", "Django", "FastAPI"],
  "frontend":  ["HTMX", "Tailwind", "JS"],
  ...
</code>
```
Ajuste com as tecnologias que você realmente usa.

**Badge de disponibilidade:**
```html
<!-- Linha ~41 -->
disponível para projetos
```
Pode trocar por "em férias", "ocupado no momento", etc.

---

### 2. Informações de contato

Edite `contact/templates/contact/contact.html`:

```html
<p class="text-slate-300 text-sm">contato@seudominio.com</p>
<p class="text-slate-300 text-sm">+55 (XX) XXXXX-XXXX</p>
```

---

### 3. Logo e nome no navbar

Edite `core/templates/core/base.html`, linha ~52:

```html
<span ...>dev<span class="text-brand-400">.</span>portfolio</span>
```

Troque `dev.portfolio` pelo seu nome ou marca pessoal.

---

### 4. Cor principal (brand color)

Toda a paleta está centralizada no `base.html`, bloco `tailwind.config`:

```js
colors: {
  brand: {
    400: "#38bdf8",   // ← cor clara (hover, destaques)
    500: "#0ea5e9",   // ← cor principal (botões, links)
    600: "#0284c7",   // ← cor escura
  },
}
```

Exemplo para trocar para verde:
```js
400: "#4ade80",
500: "#22c55e",
600: "#16a34a",
```

---

### 5. Texto do CTA final (home)

Edite `core/templates/core/home.html`, seção `CTA FINAL`:

```html
<h2 ...>Tem um projeto em mente?</h2>
<p ...>Vamos conversar sobre como posso ajudar...</p>
```

---

### 6. Créditos no footer

Edite `core/templates/core/base.html`, seção `FOOTER`:

```html
<p>© {% now "Y" %} dev.portfolio — Feito com Django + HTMX</p>
```

---

## 📦 Gerenciando projetos pelo Admin

Acesse **http://localhost/admin** com o usuário criado no `createsuperuser`.

---

### Criando Tags

Tags são as tecnologias/categorias dos seus projetos (ex: Python, n8n, Docker).

1. Acesse **Admin → Tags → Adicionar Tag**
2. Preencha:
   - **Name**: `Python`
   - **Slug**: `python` *(preenchido automaticamente)*
   - **Color**: `#3b82f6` *(cor hex — define a cor da pill no site)*
3. Salve

**Sugestão de cores por tecnologia:**

| Tag | Cor |
|---|---|
| Python | `#3b82f6` |
| n8n | `#f97316` |
| Django | `#16a34a` |
| Docker | `#0ea5e9` |
| Rust | `#ef4444` |
| JavaScript | `#eab308` |
| FastAPI | `#06b6d4` |
| Automação | `#a855f7` |

---

### Criando Projetos

1. Acesse **Admin → Projects → Adicionar Project**
2. Preencha os campos:

| Campo | O que colocar |
|---|---|
| **Title** | Nome do projeto (ex: `Disparador de WhatsApp`) |
| **Slug** | Preenchido automaticamente (ex: `disparador-whatsapp`) |
| **Short description** | Resumo de 1~2 linhas — aparece nos cards da listagem |
| **Full description** | Descrição completa — aparece na página de detalhe. Suporta parágrafos com Enter. |
| **Tags** | Selecione as tags criadas |
| **Thumbnail** | Imagem de capa (recomendado: 1280×720px) |
| **Demo url** | Link para demo ou vídeo (opcional) |
| **Repo url** | Link do GitHub (opcional) |
| **Featured** | ✅ Marque para aparecer na home em destaque |

> Projetos com **Featured** marcado aparecem na seção "Trabalhos recentes" da home (máximo 3 exibidos).

---

### Visualizando mensagens de contato

1. Acesse **Admin → Contact Messages**
2. Veja todas as mensagens com nome, e-mail, assunto e data
3. Marque como **Read** para controlar o que já foi respondido

---

## 🗂️ Estrutura do projeto

```
portfolio/
│
├── config/                  # Configurações globais do Django
│   ├── settings.py          # banco, apps, middleware, static
│   ├── urls.py              # roteamento raiz
│   └── wsgi.py
│
├── core/                    # App base
│   ├── templates/core/
│   │   ├── base.html        # layout principal (navbar, footer, CSS, JS)
│   │   └── home.html        # página inicial
│   ├── views.py
│   └── urls.py
│
├── projects/                # App de projetos
│   ├── models.py            # modelos Tag e Project
│   ├── views.py             # lista (filtro HTMX) e detalhe
│   ├── admin.py
│   ├── templates/projects/
│   │   ├── project_list.html
│   │   ├── project_detail.html
│   │   └── partials/
│   │       └── project_grid.html   # fragmento HTMX (só o grid)
│   └── urls.py
│
├── contact/                 # App de contato
│   ├── models.py            # modelo ContactMessage
│   ├── forms.py
│   ├── views.py
│   ├── admin.py
│   ├── templates/contact/
│   │   ├── contact.html
│   │   └── partials/
│   │       └── form.html           # fragmento HTMX (form + estado de sucesso)
│   └── urls.py
│
├── nginx/
│   └── nginx.conf           # proxy reverso para o gunicorn
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                     # variáveis de ambiente — NÃO commitar
└── .gitignore
```

---

## 🐳 Comandos úteis do Docker

```bash
# Subir os containers (com rebuild)
docker compose up --build

# Subir em background
docker compose up -d

# Parar tudo
docker compose down

# Ver logs em tempo real
docker compose logs -f web

# Acessar o shell dentro do container
docker exec -it portfolio_web bash

# Comandos Django
docker exec portfolio_web python manage.py migrate
docker exec portfolio_web python manage.py collectstatic --noinput
docker exec -it portfolio_web python manage.py createsuperuser

# Reiniciar só o web (após mudar código)
docker compose restart web
```

---

## ☁️ Deploy na Oracle Cloud

### Pré-requisitos na VM
- Docker e Docker Compose instalados
- Portas 80 e 443 abertas na VCN e no `iptables`

### Passo a passo

```bash
# Via Git (recomendado):
git clone https://github.com/seu-usuario/portfolio.git
cd portfolio

# Configure o .env de produção
nano .env
```

```env
DEBUG=False
SECRET_KEY=uma-string-muito-longa-e-aleatoria-aqui
ALLOWED_HOSTS=147.15.99.16,seudominio.com,www.seudominio.com
```

```bash
# Suba os containers
docker compose up --build -d

# Migre e crie o admin
docker exec portfolio_web python manage.py migrate
docker exec -it portfolio_web python manage.py createsuperuser
```

---

## 🔜 Próximos passos

- [ ] Subir no GitHub
- [ ] Configurar CI/CD com GitHub Actions
- [ ] Configurar HTTPS com Let's Encrypt (Certbot)
- [ ] Personalizar textos e cores
- [ ] Cadastrar os primeiros projetos no admin