"""
Configuração ASGI para o projeto de processamento de imagens.

ASGI (Asynchronous Server Gateway Interface) é uma especificação para servidores web
assíncronos Python, permitindo comunicação em tempo real e conexões WebSocket.

Este arquivo expõe o callable ASGI como uma variável de nível de módulo chamada ``application``.

Usado por servidores assíncronos em produção como:
    - Daphne (servidor ASGI do Django Channels)
    - Uvicorn
    - Hypercorn

ASGI é o sucessor moderno do WSGI, suportando:
    - Requisições HTTP síncronas (como WSGI)
    - WebSockets para comunicação bidirecional em tempo real
    - HTTP/2 e Server-Sent Events (SSE)

Para mais informações sobre este arquivo, consulte:
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Define o módulo de configurações do Django que deve ser usado
# Isso garante que o Django use as configurações corretas do projeto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Obtém a aplicação ASGI do Django
# Esta é a interface entre o servidor web assíncrono e a aplicação Django
application = get_asgi_application()
