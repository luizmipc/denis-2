"""
Modelos de dados para a aplicação de processamento de imagens.

Este módulo define os modelos que representam sessões de edição de imagens e snapshots
no banco de dados, permitindo edição não-destrutiva e histórico de alterações.
"""
from django.db import models
import uuid
import os
import json


def upload_path(instance, filename):
    """
    Gera um caminho único para upload de arquivos.

    Args:
        instance: Instância do modelo que está fazendo o upload
        filename: Nome original do arquivo enviado

    Returns:
        str: Caminho no formato 'uploads/uuid.extensão'

    Exemplo:
        'uploads/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg'
    """
    # Extrai a extensão do arquivo (ex: 'jpg', 'png')
    ext = filename.split('.')[-1]

    # Gera um nome único usando UUID para evitar conflitos
    filename = f"{uuid.uuid4()}.{ext}"

    # Retorna o caminho completo: uploads/uuid.extensao
    return os.path.join('uploads', filename)


class ImageSession(models.Model):
    """
    Representa uma sessão de usuário para processamento de uma imagem.

    Este modelo armazena a imagem original e todos os ajustes aplicados como metadados JSON,
    permitindo edição não-destrutiva (a imagem original nunca é alterada).

    Atributos:
        id (UUID): Identificador único da sessão
        original_image (ImageField): Imagem original enviada pelo usuário
        adjustments (JSONField): Dicionário com valores de ajustes (saturação, brilho, etc.)
        created_at (DateTime): Data/hora de criação da sessão
        updated_at (DateTime): Data/hora da última atualização
    """
    # UUID garante IDs únicos e não sequenciais para segurança
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Imagem original enviada pelo usuário (nunca é modificada)
    original_image = models.ImageField(upload_to=upload_path)

    # Armazena todos os ajustes como JSON para edição não-destrutiva
    # Exemplo: {"saturation": 80, "brightness": 10, "contrast": -5}
    adjustments = models.JSONField(default=dict, help_text="Valores de ajuste atuais")

    # Timestamps automáticos
    created_at = models.DateTimeField(auto_now_add=True)  # Definido uma vez na criação
    updated_at = models.DateTimeField(auto_now=True)      # Atualizado a cada save()

    class Meta:
        # Ordena sessões da mais recente para a mais antiga
        ordering = ['-created_at']

    def __str__(self):
        """Representação em string da sessão para o admin do Django"""
        return f"Session {self.id} - {self.created_at}"

    def get_adjustments(self):
        """
        Retorna os valores de ajuste atuais com valores padrão.

        Se um ajuste não foi definido, retorna o valor padrão.

        Returns:
            dict: Dicionário com todos os ajustes (definidos + padrões)

        Ajustes disponíveis:
            - saturation: 0-100% (0 = escala de cinza, 100 = saturação normal)
            - brightness: -100 a +100 (0 = normal)
            - contrast: -100 a +100 (0 = normal)
            - sharpness: -100 a +100 (0 = normal)
            - blur: 0 a 10 (0 = sem desfoque)
        """
        # Define valores padrão para todos os ajustes
        defaults = {
            'saturation': 100,  # 0-100% (0 = escala de cinza)
            'brightness': 0,    # -100 a +100
            'contrast': 0,      # -100 a +100
            'sharpness': 0,     # -100 a +100
            'blur': 0,          # 0 a 10
        }

        # Mescla defaults com ajustes salvos (ajustes salvos sobrescrevem defaults)
        return {**defaults, **self.adjustments}

    def update_adjustment(self, key, value):
        """
        Atualiza um único valor de ajuste.

        Args:
            key (str): Nome do ajuste (ex: 'brightness', 'saturation')
            value (int/float): Novo valor do ajuste

        Returns:
            dict: Dicionário completo de ajustes após a atualização

        Exemplo:
            session.update_adjustment('brightness', 20)
        """
        # Garante que adjustments seja um dicionário válido
        if self.adjustments is None:
            self.adjustments = {}

        # Atualiza o valor do ajuste específico
        self.adjustments[key] = value

        # Salva no banco de dados
        self.save()

        # Retorna todos os ajustes atualizados
        return self.get_adjustments()

    def reset_adjustments(self):
        """
        Reseta todos os ajustes para os valores padrão.

        Returns:
            dict: Dicionário de ajustes resetado (apenas valores padrão)

        Exemplo:
            session.reset_adjustments()
        """
        # Limpa todos os ajustes personalizados
        self.adjustments = {}

        # Salva no banco de dados
        self.save()

        # Retorna valores padrão
        return self.get_adjustments()


class ProcessingSnapshot(models.Model):
    """
    Armazena snapshots (capturas) na linha do tempo para comparação antes/depois.

    Cada snapshot representa um estado renderizado que o usuário salvou explicitamente,
    permitindo visualizar o histórico de edições e comparar diferentes versões.

    Atributos:
        id (UUID): Identificador único do snapshot
        session (ForeignKey): Referência à sessão de imagem associada
        adjustments (JSONField): Estado dos ajustes no momento do snapshot
        preview_image (ImageField): Imagem pré-renderizada opcional para visualização rápida
        description (str): Descrição do snapshot fornecida pelo usuário
        created_at (DateTime): Data/hora de criação do snapshot
        order (int): Ordem do snapshot na linha do tempo
    """
    # UUID garante IDs únicos e não sequenciais
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relacionamento com a sessão de imagem (CASCADE = deleta snapshots se a sessão for deletada)
    session = models.ForeignKey(
        ImageSession,
        on_delete=models.CASCADE,
        related_name='snapshots'  # Permite acessar: session.snapshots.all()
    )

    # Armazena o estado dos ajustes no momento em que o snapshot foi criado
    # Isso permite recriar a imagem exatamente como estava
    adjustments = models.JSONField(help_text="Valores de ajuste no momento do snapshot")

    # Imagem pré-renderizada opcional para exibição rápida na linha do tempo
    # Evita reprocessar a imagem toda vez que a linha do tempo é exibida
    preview_image = models.ImageField(upload_to='snapshots/', null=True, blank=True)

    # Descrição amigável do snapshot (ex: "Versão com alto contraste")
    description = models.CharField(max_length=200)

    # Data/hora de criação do snapshot
    created_at = models.DateTimeField(auto_now_add=True)

    # Ordem na linha do tempo (permite reordenação manual)
    order = models.IntegerField(default=0)

    class Meta:
        # Ordena por ordem personalizada primeiro, depois por data de criação
        ordering = ['order', 'created_at']

    def __str__(self):
        """Representação em string do snapshot para o admin do Django"""
        return f"{self.description} - {self.created_at}"
