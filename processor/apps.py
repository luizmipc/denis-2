"""
Configuração da aplicação Django 'processor'.

Este arquivo define metadados e configurações da aplicação de processamento de imagens.
"""
from django.apps import AppConfig


class ProcessorConfig(AppConfig):
    """
    Configuração da aplicação 'processor'.

    Esta classe define configurações básicas da aplicação, incluindo o tipo de campo
    padrão para chaves primárias e o nome interno da aplicação.

    Atributos:
        default_auto_field (str): Tipo padrão de campo para chaves primárias auto-incrementadas.
                                  BigAutoField suporta valores até 9,223,372,036,854,775,807
                                  (muito maior que AutoField que vai até 2,147,483,647)
        name (str): Nome interno da aplicação, usado para importações e referências
    """
    # Define que novas chaves primárias usarão BigAutoField por padrão
    # Isso permite IDs muito grandes, adequados para aplicações de longo prazo
    default_auto_field = 'django.db.models.BigAutoField'

    # Nome da aplicação (deve corresponder ao nome do diretório e ao INSTALLED_APPS)
    name = 'processor'
