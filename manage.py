#!/usr/bin/env python
"""
Script de linha de comando do Django para tarefas administrativas.

Este é o ponto de entrada principal para executar comandos de gerenciamento do Django,
como runserver, migrate, makemigrations, createsuperuser, etc.
"""
import os
import sys


def main():
    """
    Executa tarefas administrativas do Django.

    Esta função configura o ambiente Django e executa comandos passados via linha de comando.
    Exemplos de uso:
        python manage.py runserver - Inicia o servidor de desenvolvimento
        python manage.py migrate - Aplica migrações ao banco de dados
        python manage.py createsuperuser - Cria um usuário administrador
    """
    # Define o módulo de configurações padrão do Django para o projeto
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    try:
        # Importa a função que executa comandos Django da linha de comando
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Se o Django não estiver instalado, lança um erro informativo
        raise ImportError(
            "Não foi possível importar o Django. Você tem certeza que ele está instalado e "
            "disponível na variável de ambiente PYTHONPATH? Você esqueceu de "
            "ativar o ambiente virtual?"
        ) from exc

    # Executa o comando passado via argumentos da linha de comando (sys.argv)
    execute_from_command_line(sys.argv)


# Verifica se o script está sendo executado diretamente (não importado)
if __name__ == '__main__':
    main()
