"""
Configuração WSGI para o projeto de processamento de imagens.

WSGI (Web Server Gateway Interface) é uma especificação que define como servidores web
se comunicam com aplicações web Python.

Este arquivo expõe o callable WSGI como uma variável de nível de módulo chamada ``application``.

Usado por servidores web em produção como:
    - Apache com mod_wsgi
    - uWSGI
    - Gunicorn

Para mais informações sobre este arquivo, consulte:
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Define o módulo de configurações do Django que deve ser usado
# Isso garante que o Django use as configurações corretas do projeto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Obtém a aplicação WSGI do Django
# Esta é a interface entre o servidor web e a aplicação Django
application = get_wsgi_application()
