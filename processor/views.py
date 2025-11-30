from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from .models import ImageSession, ProcessingSnapshot
import json


@ensure_csrf_cookie
def index(request):
    """Main page for image processing"""
    return render(request, 'processor/index.html')


@require_http_methods(["POST"])
def upload_image(request):
    """Handle image upload and create new session"""
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'Nenhuma imagem enviada'}, status=400)

    image = request.FILES['image']

    # Validate file size
    if image.size > 10485760:  # 10MB
        return JsonResponse({'error': 'Arquivo muito grande (máximo 10MB)'}, status=400)

    # Validate file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
    if image.content_type not in allowed_types:
        return JsonResponse({'error': 'Tipo de arquivo não permitido'}, status=400)

    # Create new session with default adjustments
    session = ImageSession.objects.create(
        original_image=image,
        adjustments={}  # Empty dict uses defaults
    )

    return JsonResponse({
        'session_id': str(session.id),
        'image_url': session.original_image.url,
        'adjustments': session.get_adjustments(),
    })


def adjustments_handler(request, session_id):
    """
    Handle adjustments endpoint with multiple HTTP methods:
    - GET: Get current adjustment values
    - POST: Update adjustment values
    """
    session = get_object_or_404(ImageSession, id=session_id)

    if request.method == 'GET':
        return JsonResponse({
            'session_id': str(session.id),
            'adjustments': session.get_adjustments(),
        })

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            adjustments = data.get('adjustments', {})

            # Validate adjustment values
            valid_keys = ['saturation', 'brightness', 'contrast', 'sharpness', 'blur']
            for key in adjustments:
                if key not in valid_keys:
                    return JsonResponse({'error': f'Ajuste inválido: {key}'}, status=400)

            # Update adjustments
            if session.adjustments is None:
                session.adjustments = {}

            session.adjustments.update(adjustments)
            session.save()

            return JsonResponse({
                'success': True,
                'adjustments': session.get_adjustments(),
            })

        except (json.JSONDecodeError, ValueError, TypeError) as e:
            return JsonResponse({'error': f'Dados inválidos: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


def snapshots_handler(request, session_id):
    """
    Handle snapshots endpoint with multiple HTTP methods:
    - GET: Get all snapshots for timeline display
    - POST: Create a new snapshot
    """
    session = get_object_or_404(ImageSession, id=session_id)

    if request.method == 'GET':
        snapshots = [{
            'id': str(snapshot.id),
            'description': snapshot.description,
            'adjustments': snapshot.adjustments,
            'order': snapshot.order,
            'created_at': snapshot.created_at.isoformat(),
        } for snapshot in session.snapshots.all()]

        return JsonResponse({
            'session_id': str(session.id),
            'original_image': session.original_image.url,
            'current_adjustments': session.get_adjustments(),
            'snapshots': snapshots,
        })

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            description = data.get('description', 'Snapshot')
            adjustments = data.get('adjustments', session.get_adjustments())

            # Get current order
            last_snapshot = session.snapshots.order_by('-order').first()
            order = (last_snapshot.order + 1) if last_snapshot else 0

            # Create snapshot with adjustments
            snapshot = ProcessingSnapshot.objects.create(
                session=session,
                adjustments=adjustments,
                description=description,
                order=order,
            )

            return JsonResponse({
                'snapshot_id': str(snapshot.id),
                'id': str(snapshot.id),
                'description': snapshot.description,
                'adjustments': snapshot.adjustments,
                'order': snapshot.order,
                'created_at': snapshot.created_at.isoformat(),
            })

        except (json.JSONDecodeError, ValueError, TypeError) as e:
            return JsonResponse({'error': f'Dados inválidos: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


def snapshot_detail_handler(request, session_id, snapshot_id):
    """
    Handle individual snapshot operations:
    - POST: Load adjustments from a specific snapshot
    - DELETE: Delete a snapshot from timeline
    """
    session = get_object_or_404(ImageSession, id=session_id)
    snapshot = get_object_or_404(ProcessingSnapshot, id=snapshot_id, session=session)

    if request.method == 'POST':
        # Update session with snapshot's adjustments
        session.adjustments = snapshot.adjustments.copy()
        session.save()

        return JsonResponse({
            'success': True,
            'adjustments': session.get_adjustments(),
            'snapshot_id': str(snapshot.id),
        })

    elif request.method == 'DELETE':
        snapshot.delete()

        return JsonResponse({
            'success': True,
            'message': 'Snapshot removido',
        })

    return JsonResponse({'error': 'Método não permitido'}, status=405)


@require_http_methods(["POST"])
def render_image(request, session_id):
    """
    Server-side rendering endpoint (backup for older browsers).
    Client-side rendering is preferred for real-time performance.
    """
    session = get_object_or_404(ImageSession, id=session_id)

    try:
        from .image_processor import ImageProcessor
        from django.core.files.base import ContentFile
        import uuid

        # Get current adjustments
        adj = session.get_adjustments()

        # Start with original image
        img_path = session.original_image.path

        # Apply adjustments in order (non-destructive on original)
        processed = ImageProcessor.apply_all_adjustments(img_path, adj)

        # Save temporarily
        filename = f'rendered_{uuid.uuid4()}.jpg'

        return JsonResponse({
            'success': True,
            'message': 'Imagem renderizada no servidor',
        })

    except Exception as e:
        return JsonResponse({'error': f'Erro ao renderizar: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def download_image(request, session_id):
    """
    Download endpoint - expects the final rendered image to be uploaded by client.
    For now, returns the original (client should handle rendering).
    """
    session = get_object_or_404(ImageSession, id=session_id)

    # For now, return original image
    # In production, client would upload the final rendered canvas
    image_path = session.original_image.path
    filename = f'processed_{session.id}.jpg'

    response = FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@require_http_methods(["POST"])
def upload_rendered(request, session_id):
    """
    Upload the final rendered image from client-side canvas.
    Used for download functionality.
    """
    session = get_object_or_404(ImageSession, id=session_id)

    if 'rendered_image' not in request.FILES:
        return JsonResponse({'error': 'Nenhuma imagem enviada'}, status=400)

    # Store rendered image temporarily for download
    # In production, you might store this in session or cache

    return JsonResponse({
        'success': True,
        'message': 'Imagem renderizada salva',
    })
