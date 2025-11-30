from django.urls import path
from . import views

app_name = 'processor'

urlpatterns = [
    # Main interface
    path('', views.index, name='index'),

    # Session management
    path('api/upload/', views.upload_image, name='upload'),

    # Adjustments (non-destructive)
    path('api/adjustments/<uuid:session_id>/', views.adjustments_handler, name='adjustments'),

    # Snapshots (timeline)
    path('api/snapshots/<uuid:session_id>/', views.snapshots_handler, name='snapshots'),
    path('api/snapshots/<uuid:session_id>/<uuid:snapshot_id>/', views.snapshot_detail_handler, name='snapshot_detail'),

    # Rendering & Download
    path('api/render/<uuid:session_id>/', views.render_image, name='render'),
    path('api/download/<uuid:session_id>/', views.download_image, name='download'),
    path('api/upload-rendered/<uuid:session_id>/', views.upload_rendered, name='upload_rendered'),
]
