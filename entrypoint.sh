#!/bin/bash

# Image Processor - Docker Entrypoint Script
# This script automates all setup steps for Docker deployment

set -e  # Exit on error

echo "🚀 Image Processor - Starting..."
echo ""

# Wait for any dependencies if needed
sleep 2

echo "📦 Installing Python dependencies with uv..."
uv pip install --system django pillow numpy django-cors-headers
echo "✅ Dependencies installed"
echo ""

echo "🗄️  Running database migrations..."
python manage.py migrate --noinput
echo "✅ Migrations completed"
echo ""

echo "📁 Creating media directories..."
mkdir -p media/uploads media/processed
echo "✅ Media directories ready"
echo ""

echo "📊 Collecting static files..."
python manage.py collectstatic --noinput --clear 2>/dev/null || echo "⚠️  No static files to collect (optional)"
echo ""

echo "✅ Setup completed successfully!"
echo ""
echo "🌐 Starting Django development server..."
echo "📍 Access the application at: http://localhost:8000"
echo ""

# Start the Django development server
exec python manage.py runserver 0.0.0.0:8000
