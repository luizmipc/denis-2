"""
Configuração da interface administrativa do Django para a aplicação processor.

Este módulo define como os modelos ImageSession e ProcessingSnapshot
são exibidos e gerenciados no painel administrativo do Django.

Acesse o admin em: http://localhost:8000/admin/
"""
from django.contrib import admin
from .models import ImageSession, ProcessingSnapshot


class ProcessingSnapshotInline(admin.TabularInline):
    """
    Exibição inline de snapshots dentro da página de edição de ImageSession.

    Permite visualizar e editar snapshots diretamente na página da sessão,
    em formato de tabela compacta.

    Atributos:
        model: Modelo a ser exibido inline (ProcessingSnapshot)
        extra (int): Número de formulários vazios extras (0 = nenhum)
        readonly_fields: Campos que não podem ser editados
        fields: Campos a serem exibidos na tabela
    """
    model = ProcessingSnapshot
    extra = 0  # Não mostra formulários vazios extras
    readonly_fields = ('created_at', 'preview_image')  # Campos somente leitura
    fields = ('description', 'order', 'preview_image', 'created_at')  # Campos visíveis


@admin.register(ImageSession)
class ImageSessionAdmin(admin.ModelAdmin):
    """
    Configuração da interface administrativa para ImageSession.

    Define como as sessões de imagem são listadas e editadas no admin do Django.

    Atributos:
        list_display: Colunas exibidas na lista de sessões
        list_filter: Filtros laterais disponíveis
        search_fields: Campos pesquisáveis
        readonly_fields: Campos que não podem ser editados
        inlines: Modelos relacionados exibidos na mesma página
    """
    # Colunas exibidas na lista de sessões
    list_display = ('id', 'created_at', 'updated_at', 'snapshot_count')

    # Filtros disponíveis na barra lateral
    list_filter = ('created_at', 'updated_at')

    # Campos pesquisáveis via caixa de busca
    search_fields = ('id',)

    # Campos que não podem ser editados (auto-gerados)
    readonly_fields = ('id', 'created_at', 'updated_at')

    # Exibe snapshots relacionados inline (na mesma página)
    inlines = [ProcessingSnapshotInline]

    def snapshot_count(self, obj):
        """
        Método customizado para exibir a contagem de snapshots.

        Args:
            obj (ImageSession): Objeto da sessão de imagem

        Returns:
            int: Número de snapshots associados à sessão
        """
        return obj.snapshots.count()

    # Define o rótulo da coluna na lista
    snapshot_count.short_description = 'Total Snapshots'


@admin.register(ProcessingSnapshot)
class ProcessingSnapshotAdmin(admin.ModelAdmin):
    """
    Configuração da interface administrativa para ProcessingSnapshot.

    Define como os snapshots são listados e editados no admin do Django.

    Atributos:
        list_display: Colunas exibidas na lista de snapshots
        list_filter: Filtros laterais disponíveis
        search_fields: Campos pesquisáveis (inclusive em modelos relacionados)
        readonly_fields: Campos que não podem ser editados
        ordering: Ordem padrão de exibição dos snapshots
    """
    # Colunas exibidas na lista de snapshots
    list_display = ('id', 'session', 'description', 'order', 'created_at')

    # Filtros disponíveis na barra lateral
    list_filter = ('created_at',)

    # Campos pesquisáveis (session__id busca no ID da sessão relacionada)
    search_fields = ('session__id', 'description')

    # Campos que não podem ser editados
    readonly_fields = ('id', 'created_at')

    # Ordena por sessão, depois por ordem, depois por data de criação
    ordering = ('session', 'order', 'created_at')
