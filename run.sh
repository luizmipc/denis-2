#!/bin/bash

# Image Processor - Quick Start Script

echo "🚀 Iniciando Image Processor..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual com uv..."
    uv venv
    echo "✅ Ambiente virtual criado"
    echo ""
fi

# Activate virtual environment
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Install dependencies
echo "📥 Instalando dependências..."
uv pip install django pillow numpy django-cors-headers

# Create media directories
echo "📁 Criando diretórios de mídia..."
mkdir -p media/uploads media/processed

# Run migrations
echo "🗄️  Executando migrações do banco de dados..."
python manage.py migrate

echo ""
echo "✅ Configuração concluída!"
echo ""
echo "🌐 Iniciando servidor de desenvolvimento..."
echo "📍 Acesse: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start server
python manage.py runserver
