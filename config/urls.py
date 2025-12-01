"""
Configuração de URLs para o projeto de processamento de imagens.

Este arquivo define o roteamento de URLs principal do projeto, mapeando URLs para views.
A lista `urlpatterns` roteia URLs para views específicas.

Para mais informações, consulte:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

Exemplos de uso:

Views baseadas em funções:
    1. Adicione um import:  from my_app import views
    2. Adicione uma URL aos padrões:  path('', views.home, name='home')

Views baseadas em classes:
    1. Adicione um import:  from other_app.views import Home
    2. Adicione uma URL aos padrões:  path('', Home.as_view(), name='home')

Incluindo outro URLconf:
    1. Importe a função include():  from django.urls import include, path
    2. Adicione uma URL aos padrões:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Lista de padrões de URL do projeto
urlpatterns = [
    # URL da interface de administração do Django
    # Acesse via: http://localhost:8000/admin/
    path('admin/', admin.site.urls),

    # Inclui todas as URLs da aplicação 'processor'
    # O caminho vazio ('') significa que as URLs do processor estarão na raiz do site
    # Exemplo: http://localhost:8000/ irá para a página inicial do processor
    path('', include('processor.urls')),
]

# Em modo de desenvolvimento (DEBUG=True), serve arquivos de mídia e estáticos
# IMPORTANTE: Em produção, isso deve ser feito pelo servidor web (nginx, apache, etc.)
if settings.DEBUG:
    # Adiciona rota para servir arquivos de mídia (uploads de usuários)
    # Exemplo: http://localhost:8000/media/imagem.jpg
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Adiciona rota para servir arquivos estáticos (CSS, JS, imagens do projeto)
    # Exemplo: http://localhost:8000/static/css/style.css
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
