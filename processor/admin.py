from django.contrib import admin
from .models import ImageSession, ProcessingSnapshot


class ProcessingSnapshotInline(admin.TabularInline):
    model = ProcessingSnapshot
    extra = 0
    readonly_fields = ('created_at', 'preview_image')
    fields = ('description', 'order', 'preview_image', 'created_at')


@admin.register(ImageSession)
class ImageSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'snapshot_count')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [ProcessingSnapshotInline]

    def snapshot_count(self, obj):
        return obj.snapshots.count()
    snapshot_count.short_description = 'Total Snapshots'


@admin.register(ProcessingSnapshot)
class ProcessingSnapshotAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'description', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('session__id', 'description')
    readonly_fields = ('id', 'created_at')
    ordering = ('session', 'order', 'created_at')
