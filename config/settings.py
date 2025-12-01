"""
Configurações do Django para o projeto de processamento de imagens.

Este arquivo contém todas as configurações necessárias para o funcionamento do projeto Django,
incluindo banco de dados, aplicativos instalados, middleware, templates e configurações personalizadas.

Gerado por 'django-admin startproject' usando Django 5.2.8.

Para mais informações sobre este arquivo, consulte:
https://docs.djangoproject.com/en/5.2/topics/settings/

Para a lista completa de configurações e seus valores, consulte:
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

# Constrói caminhos dentro do projeto usando: BASE_DIR / 'subdir'
# BASE_DIR representa o diretório raiz do projeto (onde está o manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CONFIGURAÇÕES DE DESENVOLVIMENTO - NÃO ADEQUADAS PARA PRODUÇÃO
# ==============================================================================
# Veja: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# AVISO DE SEGURANÇA: mantenha a chave secreta usada em produção em segredo!
# Esta chave é usada para criptografia e deve ser alterada em produção
SECRET_KEY = 'django-insecure-jm07&a)$g$nc$5#9^&tzkr3p)a7d@9d85rrrt%*!g8ucp^%31f'

# AVISO DE SEGURANÇA: não execute com debug ligado em produção!
# DEBUG=True mostra informações detalhadas de erro, útil para desenvolvimento
DEBUG = True

# Lista de hosts/domínios que este site Django pode servir
# Em produção, defina para domínios específicos: ['meusite.com', 'www.meusite.com']
ALLOWED_HOSTS = []


# ==============================================================================
# DEFINIÇÃO DE APLICAÇÕES
# ==============================================================================

# Lista de todas as aplicações Django ativadas neste projeto
INSTALLED_APPS = [
    # Aplicações nativas do Django
    'django.contrib.admin',           # Interface de administração
    'django.contrib.auth',            # Sistema de autenticação
    'django.contrib.contenttypes',    # Framework de tipos de conteúdo
    'django.contrib.sessions',        # Framework de sessões
    'django.contrib.messages',        # Framework de mensagens
    'django.contrib.staticfiles',     # Gerenciamento de arquivos estáticos

    # Aplicações de terceiros
    'corsheaders',                    # Gerencia Cross-Origin Resource Sharing (CORS)

    # Aplicações do projeto
    'processor',                      # Aplicação principal de processamento de imagens
]

# ==============================================================================
# MIDDLEWARE
# ==============================================================================

# Lista de middleware que processa requisições/respostas
# A ordem é importante! Cada middleware é executado na ordem da lista
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',              # Adiciona headers de segurança
    'django.contrib.sessions.middleware.SessionMiddleware',       # Gerencia sessões
    'corsheaders.middleware.CorsMiddleware',                      # Lida com CORS (deve vir antes do CommonMiddleware)
    'django.middleware.common.CommonMiddleware',                  # Adiciona funcionalidades comuns
    'django.middleware.csrf.CsrfViewMiddleware',                  # Proteção contra CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',    # Associa usuários com requisições
    'django.contrib.messages.middleware.MessageMiddleware',       # Gerencia mensagens temporárias
    'django.middleware.clickjacking.XFrameOptionsMiddleware',     # Proteção contra clickjacking
]

# Define o módulo principal de configuração de URLs
ROOT_URLCONF = 'config.urls'

# ==============================================================================
# TEMPLATES
# ==============================================================================

# Configuração do sistema de templates Django
TEMPLATES = [
    {
        # Motor de templates padrão do Django
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Diretórios onde o Django procurará por templates
        'DIRS': [BASE_DIR / 'templates'],

        # Se True, procura templates dentro do diretório 'templates' de cada app
        'APP_DIRS': True,

        'OPTIONS': {
            # Processadores de contexto adicionam variáveis aos templates automaticamente
            'context_processors': [
                'django.template.context_processors.request',   # Adiciona 'request' aos templates
                'django.contrib.auth.context_processors.auth',  # Adiciona 'user' e 'perms' aos templates
                'django.contrib.messages.context_processors.messages',  # Adiciona 'messages' aos templates
                'django.template.context_processors.media',     # Adiciona MEDIA_URL aos templates
            ],
        },
    },
]

# Aplicação WSGI usada pelo servidor de aplicação
WSGI_APPLICATION = 'config.wsgi.application'


# ==============================================================================
# BANCO DE DADOS
# ==============================================================================
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        # Usa SQLite como banco de dados (ideal para desenvolvimento)
        'ENGINE': 'django.db.backends.sqlite3',
        # Arquivo do banco de dados SQLite (criado no diretório raiz do projeto)
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==============================================================================
# VALIDAÇÃO DE SENHAS
# ==============================================================================
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

# Lista de validadores que verificam a força das senhas
AUTH_PASSWORD_VALIDATORS = [
    {
        # Verifica se a senha não é muito similar aos atributos do usuário
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Verifica se a senha tem um comprimento mínimo (padrão: 8 caracteres)
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Verifica se a senha não está na lista de senhas comuns
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Verifica se a senha não é totalmente numérica
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==============================================================================
# INTERNACIONALIZAÇÃO
# ==============================================================================
# https://docs.djangoproject.com/en/5.2/topics/i18n/

# Define o idioma padrão da interface (português brasileiro)
LANGUAGE_CODE = 'pt-br'

# Define o fuso horário do projeto (horário de Brasília)
TIME_ZONE = 'America/Sao_Paulo'

# Habilita o sistema de internacionalização (i18n)
USE_I18N = True

# Habilita o uso de fuso horário (armazena datas em UTC no banco de dados)
USE_TZ = True


# ==============================================================================
# ARQUIVOS ESTÁTICOS (CSS, JavaScript, Imagens)
# ==============================================================================
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# URL base para servir arquivos estáticos (ex: /static/css/style.css)
STATIC_URL = 'static/'

# Diretórios adicionais onde o Django procurará arquivos estáticos
STATICFILES_DIRS = [BASE_DIR / 'static']

# ==============================================================================
# ARQUIVOS DE MÍDIA (Uploads de usuários)
# ==============================================================================

# URL base para servir arquivos de mídia enviados pelos usuários
MEDIA_URL = 'media/'

# Diretório do sistema de arquivos onde os arquivos de mídia serão armazenados
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================================================================
# CONFIGURAÇÕES DE CORS (Cross-Origin Resource Sharing)
# ==============================================================================

# Permite requisições de qualquer origem (útil para desenvolvimento)
# ATENÇÃO: Em produção, defina origins específicas por segurança
CORS_ALLOW_ALL_ORIGINS = True

# ==============================================================================
# OUTRAS CONFIGURAÇÕES
# ==============================================================================

# Tipo de campo padrão para chaves primárias
# BigAutoField suporta IDs maiores que AutoField
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# CONFIGURAÇÕES PERSONALIZADAS DO PROJETO
# ==============================================================================

# Tamanho máximo permitido para upload de imagens (10MB em bytes)
MAX_UPLOAD_SIZE = 10485760  # 10MB
