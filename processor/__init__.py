"""
Aplicação Django 'processor' - Processamento de Imagens.

Este arquivo __init__.py marca o diretório 'processor' como um pacote Python,
permitindo que módulos dentro dele sejam importados.

A aplicação 'processor' contém:
    - models.py: Modelos de dados (ImageSession, ProcessingSnapshot)
    - views.py: Views/controladores da aplicação
    - urls.py: Configuração de rotas da aplicação
    - admin.py: Configuração do painel administrativo
    - image_processor.py: Lógica de processamento de imagens
    - apps.py: Configuração da aplicação

Funcionalidades principais:
    - Upload e gerenciamento de imagens
    - Edição não-destrutiva com ajustes em tempo real
    - Sistema de snapshots (linha do tempo)
    - Renderização e download de imagens processadas

Nota:
    Este arquivo normalmente fica vazio. Ele existe apenas para indicar
    ao Python que este diretório deve ser tratado como um pacote.
"""
