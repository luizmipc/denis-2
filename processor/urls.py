"""
Configuração de URLs da aplicação 'processor'.

Define todos os endpoints (rotas) da aplicação de processamento de imagens,
mapeando URLs para as views correspondentes.

Estrutura da API:
    - Interface: Página principal
    - Sessões: Upload e gerenciamento de imagens
    - Ajustes: Modificação não-destrutiva de parâmetros
    - Snapshots: Sistema de linha do tempo e capturas
    - Renderização: Processamento e download de imagens
"""
from django.urls import path
from . import views

# Namespace da aplicação (permite usar 'processor:nome_da_rota' em templates)
app_name = 'processor'

urlpatterns = [
    # ==============================================================================
    # INTERFACE PRINCIPAL
    # ==============================================================================

    # Página inicial do editor de imagens
    # GET / -> Renderiza o template com a interface do usuário
    path('', views.index, name='index'),

    # ==============================================================================
    # GERENCIAMENTO DE SESSÕES
    # ==============================================================================

    # Upload de imagem e criação de nova sessão
    # POST /api/upload/ -> Retorna session_id e image_url
    path('api/upload/', views.upload_image, name='upload'),

    # ==============================================================================
    # AJUSTES NÃO-DESTRUTIVOS
    # ==============================================================================

    # Gerenciamento de ajustes da imagem (brilho, contraste, etc.)
    # GET  /api/adjustments/<session_id>/ -> Retorna ajustes atuais
    # POST /api/adjustments/<session_id>/ -> Atualiza ajustes
    path('api/adjustments/<uuid:session_id>/', views.adjustments_handler, name='adjustments'),

    # ==============================================================================
    # SNAPSHOTS (LINHA DO TEMPO)
    # ==============================================================================

    # Gerenciamento de snapshots da linha do tempo
    # GET  /api/snapshots/<session_id>/ -> Lista todos os snapshots
    # POST /api/snapshots/<session_id>/ -> Cria novo snapshot
    path('api/snapshots/<uuid:session_id>/', views.snapshots_handler, name='snapshots'),

    # Operações em snapshot específico
    # POST   /api/snapshots/<session_id>/<snapshot_id>/ -> Carrega ajustes do snapshot
    # DELETE /api/snapshots/<session_id>/<snapshot_id>/ -> Remove snapshot
    path('api/snapshots/<uuid:session_id>/<uuid:snapshot_id>/', views.snapshot_detail_handler, name='snapshot_detail'),

    # ==============================================================================
    # RENDERIZAÇÃO E DOWNLOAD
    # ==============================================================================

    # Renderização server-side (fallback para navegadores antigos)
    # POST /api/render/<session_id>/ -> Renderiza imagem no servidor
    path('api/render/<uuid:session_id>/', views.render_image, name='render'),

    # Download da imagem processada
    # GET /api/download/<session_id>/ -> Retorna arquivo da imagem
    path('api/download/<uuid:session_id>/', views.download_image, name='download'),

    # Upload da imagem renderizada pelo cliente (para download posterior)
    # POST /api/upload-rendered/<session_id>/ -> Recebe imagem do canvas
    path('api/upload-rendered/<uuid:session_id>/', views.upload_rendered, name='upload_rendered'),
]
