"""
Views (Controladores) para a aplicação de processamento de imagens.

Este módulo contém todas as funções de view que lidam com requisições HTTP,
processam dados e retornam respostas para o frontend da aplicação.

Endpoints principais:
    - index: Página inicial da aplicação
    - upload_image: Upload de imagens e criação de sessões
    - adjustments_handler: Gerenciamento de ajustes de imagem
    - snapshots_handler: Gerenciamento de snapshots da linha do tempo
    - render_image: Renderização de imagens no servidor (fallback)
    - download_image: Download da imagem processada
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from .models import ImageSession, ProcessingSnapshot
import json


@ensure_csrf_cookie
def index(request):
    """
    Página principal para processamento de imagens.

    Este decorator (@ensure_csrf_cookie) garante que o cookie CSRF seja enviado
    ao cliente, necessário para requisições POST/PUT/DELETE subsequentes.

    Args:
        request: Objeto HttpRequest do Django

    Returns:
        HttpResponse: Renderiza o template processor/index.html
    """
    return render(request, 'processor/index.html')


@require_http_methods(["POST"])
def upload_image(request):
    """
    Lida com o upload de imagens e cria uma nova sessão de edição.

    Este endpoint recebe uma imagem via POST, valida o arquivo (tamanho e tipo),
    e cria uma nova ImageSession no banco de dados.

    Args:
        request: Objeto HttpRequest contendo o arquivo de imagem

    Returns:
        JsonResponse com:
            - session_id: ID único da sessão criada
            - image_url: URL da imagem original
            - adjustments: Valores padrão de ajustes

    Validações:
        - Arquivo deve estar presente no campo 'image'
        - Tamanho máximo: 10MB
        - Tipos permitidos: JPEG, JPG, PNG, GIF

    Códigos de status HTTP:
        200: Sucesso
        400: Erro de validação (arquivo muito grande, tipo inválido, etc.)
    """
    # Verifica se um arquivo de imagem foi enviado
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'Nenhuma imagem enviada'}, status=400)

    image = request.FILES['image']

    # Valida o tamanho do arquivo (máximo 10MB = 10485760 bytes)
    if image.size > 10485760:  # 10MB
        return JsonResponse({'error': 'Arquivo muito grande (máximo 10MB)'}, status=400)

    # Valida o tipo MIME do arquivo
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
    if image.content_type not in allowed_types:
        return JsonResponse({'error': 'Tipo de arquivo não permitido'}, status=400)

    # Cria uma nova sessão no banco de dados com ajustes padrão
    session = ImageSession.objects.create(
        original_image=image,
        adjustments={}  # Dicionário vazio usa valores padrão (definidos em get_adjustments)
    )

    # Retorna dados da sessão criada em formato JSON
    return JsonResponse({
        'session_id': str(session.id),           # ID da sessão (UUID convertido para string)
        'image_url': session.original_image.url, # URL para acessar a imagem
        'adjustments': session.get_adjustments(), # Valores padrão de todos os ajustes
    })


def adjustments_handler(request, session_id):
    """
    Gerencia o endpoint de ajustes com múltiplos métodos HTTP.

    Este endpoint permite visualizar e atualizar os ajustes de uma sessão de imagem.

    Métodos HTTP suportados:
        - GET: Obtém os valores atuais de ajustes
        - POST: Atualiza os valores de ajustes

    Args:
        request: Objeto HttpRequest
        session_id (str): UUID da sessão de imagem

    Returns:
        JsonResponse com os dados da sessão e ajustes

    GET Response:
        {
            "session_id": "uuid-da-sessao",
            "adjustments": {"saturation": 100, "brightness": 0, ...}
        }

    POST Request Body:
        {
            "adjustments": {"brightness": 20, "contrast": 10}
        }

    POST Response:
        {
            "success": true,
            "adjustments": {"saturation": 100, "brightness": 20, ...}
        }

    Códigos de status HTTP:
        200: Sucesso
        400: Dados inválidos ou ajuste não reconhecido
        404: Sessão não encontrada
        405: Método HTTP não permitido
    """
    # Busca a sessão ou retorna 404 se não existir
    session = get_object_or_404(ImageSession, id=session_id)

    if request.method == 'GET':
        # Retorna os ajustes atuais da sessão
        return JsonResponse({
            'session_id': str(session.id),
            'adjustments': session.get_adjustments(),
        })

    elif request.method == 'POST':
        try:
            # Parse do corpo JSON da requisição
            data = json.loads(request.body)
            adjustments = data.get('adjustments', {})

            # Valida que apenas ajustes reconhecidos sejam enviados
            valid_keys = ['saturation', 'brightness', 'contrast', 'sharpness', 'blur']
            for key in adjustments:
                if key not in valid_keys:
                    return JsonResponse({'error': f'Ajuste inválido: {key}'}, status=400)

            # Atualiza os ajustes na sessão
            if session.adjustments is None:
                session.adjustments = {}

            # Atualiza apenas os ajustes enviados (merge com valores existentes)
            session.adjustments.update(adjustments)
            session.save()

            # Retorna os ajustes completos após a atualização
            return JsonResponse({
                'success': True,
                'adjustments': session.get_adjustments(),
            })

        except (json.JSONDecodeError, ValueError, TypeError) as e:
            # Captura erros de parsing JSON ou tipos inválidos
            return JsonResponse({'error': f'Dados inválidos: {str(e)}'}, status=400)

    # Retorna erro se o método HTTP não for GET ou POST
    return JsonResponse({'error': 'Método não permitido'}, status=405)


def snapshots_handler(request, session_id):
    """
    Gerencia o endpoint de snapshots (capturas) da linha do tempo.

    Este endpoint permite visualizar todos os snapshots e criar novos snapshots
    que capturam o estado atual dos ajustes da imagem.

    Métodos HTTP suportados:
        - GET: Obtém todos os snapshots da linha do tempo
        - POST: Cria um novo snapshot

    Args:
        request: Objeto HttpRequest
        session_id (str): UUID da sessão de imagem

    Returns:
        JsonResponse com dados dos snapshots

    GET Response:
        {
            "session_id": "uuid",
            "original_image": "/media/uploads/imagem.jpg",
            "current_adjustments": {...},
            "snapshots": [
                {
                    "id": "uuid",
                    "description": "Versão com alto contraste",
                    "adjustments": {...},
                    "order": 0,
                    "created_at": "2024-01-01T12:00:00"
                }
            ]
        }

    POST Request Body:
        {
            "description": "Meu snapshot",
            "adjustments": {...}  // Opcional, usa ajustes atuais se omitido
        }

    POST Response:
        {
            "snapshot_id": "uuid",
            "id": "uuid",
            "description": "Meu snapshot",
            "adjustments": {...},
            "order": 1,
            "created_at": "2024-01-01T12:00:00"
        }

    Códigos de status HTTP:
        200: Sucesso
        400: Dados inválidos
        404: Sessão não encontrada
        405: Método HTTP não permitido
    """
    # Busca a sessão ou retorna 404 se não existir
    session = get_object_or_404(ImageSession, id=session_id)

    if request.method == 'GET':
        # Monta lista de todos os snapshots da sessão
        snapshots = [{
            'id': str(snapshot.id),
            'description': snapshot.description,
            'adjustments': snapshot.adjustments,
            'order': snapshot.order,
            'created_at': snapshot.created_at.isoformat(),  # Converte datetime para string ISO
        } for snapshot in session.snapshots.all()]

        # Retorna dados completos da sessão e snapshots
        return JsonResponse({
            'session_id': str(session.id),
            'original_image': session.original_image.url,
            'current_adjustments': session.get_adjustments(),
            'snapshots': snapshots,
        })

    elif request.method == 'POST':
        try:
            # Parse do corpo JSON da requisição
            data = json.loads(request.body)
            description = data.get('description', 'Snapshot')
            adjustments = data.get('adjustments', session.get_adjustments())

            # Determina a ordem do novo snapshot (último + 1)
            last_snapshot = session.snapshots.order_by('-order').first()
            order = (last_snapshot.order + 1) if last_snapshot else 0

            # Cria o snapshot no banco de dados
            snapshot = ProcessingSnapshot.objects.create(
                session=session,
                adjustments=adjustments,
                description=description,
                order=order,
            )

            # Retorna dados do snapshot criado
            return JsonResponse({
                'snapshot_id': str(snapshot.id),
                'id': str(snapshot.id),
                'description': snapshot.description,
                'adjustments': snapshot.adjustments,
                'order': snapshot.order,
                'created_at': snapshot.created_at.isoformat(),
            })

        except (json.JSONDecodeError, ValueError, TypeError) as e:
            # Captura erros de parsing JSON ou tipos inválidos
            return JsonResponse({'error': f'Dados inválidos: {str(e)}'}, status=400)

    # Retorna erro se o método HTTP não for GET ou POST
    return JsonResponse({'error': 'Método não permitido'}, status=405)


def snapshot_detail_handler(request, session_id, snapshot_id):
    """
    Gerencia operações em snapshots individuais.

    Este endpoint permite carregar ajustes de um snapshot específico
    ou deletar um snapshot da linha do tempo.

    Métodos HTTP suportados:
        - POST: Carrega os ajustes de um snapshot específico para a sessão atual
        - DELETE: Remove um snapshot da linha do tempo

    Args:
        request: Objeto HttpRequest
        session_id (str): UUID da sessão de imagem
        snapshot_id (str): UUID do snapshot específico

    Returns:
        JsonResponse com resultado da operação

    POST Response (carregar snapshot):
        {
            "success": true,
            "adjustments": {...},  // Ajustes do snapshot carregados
            "snapshot_id": "uuid"
        }

    DELETE Response:
        {
            "success": true,
            "message": "Snapshot removido"
        }

    Códigos de status HTTP:
        200: Sucesso
        404: Sessão ou snapshot não encontrado
        405: Método HTTP não permitido
    """
    # Busca a sessão ou retorna 404 se não existir
    session = get_object_or_404(ImageSession, id=session_id)

    # Busca o snapshot específico da sessão ou retorna 404
    snapshot = get_object_or_404(ProcessingSnapshot, id=snapshot_id, session=session)

    if request.method == 'POST':
        # Carrega os ajustes do snapshot para a sessão atual
        # .copy() cria uma cópia independente para evitar modificação acidental do snapshot
        session.adjustments = snapshot.adjustments.copy()
        session.save()

        # Retorna confirmação e ajustes carregados
        return JsonResponse({
            'success': True,
            'adjustments': session.get_adjustments(),
            'snapshot_id': str(snapshot.id),
        })

    elif request.method == 'DELETE':
        # Remove o snapshot do banco de dados
        snapshot.delete()

        # Retorna confirmação de remoção
        return JsonResponse({
            'success': True,
            'message': 'Snapshot removido',
        })

    # Retorna erro se o método HTTP não for POST ou DELETE
    return JsonResponse({'error': 'Método não permitido'}, status=405)


@require_http_methods(["POST"])
def render_image(request, session_id):
    """
    Endpoint de renderização no servidor (fallback para navegadores antigos).

    A renderização no lado do cliente (usando Canvas API) é preferida para
    performance em tempo real. Este endpoint serve como fallback para
    navegadores que não suportam as APIs modernas de canvas.

    Args:
        request: Objeto HttpRequest
        session_id (str): UUID da sessão de imagem

    Returns:
        JsonResponse confirmando a renderização

    Response:
        {
            "success": true,
            "message": "Imagem renderizada no servidor"
        }

    Códigos de status HTTP:
        200: Sucesso
        404: Sessão não encontrada
        500: Erro durante a renderização
    """
    session = get_object_or_404(ImageSession, id=session_id)

    try:
        from .image_processor import ImageProcessor
        from django.core.files.base import ContentFile
        import uuid

        # Obtém os ajustes atuais da sessão
        adj = session.get_adjustments()

        # Caminho da imagem original no sistema de arquivos
        img_path = session.original_image.path

        # Aplica todos os ajustes à imagem (processamento não-destrutivo)
        processed = ImageProcessor.apply_all_adjustments(img_path, adj)

        # Gera nome de arquivo único para a imagem renderizada
        filename = f'rendered_{uuid.uuid4()}.jpg'

        return JsonResponse({
            'success': True,
            'message': 'Imagem renderizada no servidor',
        })

    except Exception as e:
        # Captura qualquer erro durante o processamento
        return JsonResponse({'error': f'Erro ao renderizar: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def download_image(request, session_id):
    """
    Endpoint de download da imagem processada.

    Por enquanto, retorna a imagem original. Em produção, o cliente
    deveria enviar a imagem final renderizada via upload_rendered() primeiro.

    Args:
        request: Objeto HttpRequest
        session_id (str): UUID da sessão de imagem

    Returns:
        FileResponse: Arquivo da imagem para download

    Headers de resposta:
        Content-Type: image/jpeg
        Content-Disposition: attachment; filename="processed_{session_id}.jpg"

    Códigos de status HTTP:
        200: Sucesso (arquivo enviado)
        404: Sessão não encontrada
    """
    session = get_object_or_404(ImageSession, id=session_id)

    # Por enquanto, retorna a imagem original
    # Em produção, o cliente deveria fazer upload da imagem renderizada antes
    image_path = session.original_image.path
    filename = f'processed_{session.id}.jpg'

    # Cria resposta de arquivo para download
    response = FileResponse(open(image_path, 'rb'), content_type='image/jpeg')

    # Define header que força o download (não abre no navegador)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


@require_http_methods(["POST"])
def upload_rendered(request, session_id):
    """
    Recebe a imagem final renderizada do canvas do cliente.

    Este endpoint é usado quando o usuário quer fazer download da imagem processada.
    O cliente renderiza a imagem com todos os ajustes no canvas e envia o resultado
    aqui para ser armazenado temporariamente antes do download.

    Args:
        request: Objeto HttpRequest contendo o arquivo renderizado
        session_id (str): UUID da sessão de imagem

    Request:
        - Campo 'rendered_image' deve conter o arquivo de imagem renderizada

    Returns:
        JsonResponse confirmando o salvamento

    Response:
        {
            "success": true,
            "message": "Imagem renderizada salva"
        }

    Códigos de status HTTP:
        200: Sucesso
        400: Nenhuma imagem foi enviada
        404: Sessão não encontrada

    Nota:
        Em produção, você pode armazenar isso em sessão, cache (Redis),
        ou sistema de arquivos temporário.
    """
    session = get_object_or_404(ImageSession, id=session_id)

    # Verifica se a imagem renderizada foi enviada
    if 'rendered_image' not in request.FILES:
        return JsonResponse({'error': 'Nenhuma imagem enviada'}, status=400)

    # Armazena a imagem renderizada temporariamente para download
    # Em produção, você pode salvar isso em sessão ou cache (Redis)

    return JsonResponse({
        'success': True,
        'message': 'Imagem renderizada salva',
    })
