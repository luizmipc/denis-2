# 🚀 Guia Rápido - Image Processor

## Setup em 30 Segundos

### Docker (Mais Fácil!)

```bash
git clone <repository-url>
cd denis-2
docker-compose up --build
```

Acesse: **http://localhost:8000** ✨

### Local com uv

```bash
git clone <repository-url>
cd denis-2
./run.sh
```

Acesse: **http://localhost:8000** ✨

---

## Como Usar

1. **📤 Upload**: Arraste uma imagem ou clique para selecionar
2. **🎨 Edite**: Use os controles para ajustar
   - Escala de Cinza
   - Brilho (0 - 2.0)
   - Contraste (0 - 2.0)
   - Nitidez (0 - 2.0)
   - Desfoque (0 - 10)
3. **📜 Timeline**: Visualize todo o histórico
4. **⏪ Desfazer**: Volte atrás quando quiser
5. **💾 Download**: Baixe a imagem final

---

## Comandos Úteis

### Docker

```bash
# Iniciar
docker-compose up

# Parar
docker-compose down

# Rebuild (após mudanças no código)
docker-compose up --build

# Ver logs
docker-compose logs -f

# Acessar shell do container
docker-compose exec web bash
```

### Local

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Iniciar servidor
python manage.py runserver

# Criar superusuário (admin)
python manage.py createsuperuser

# Acessar shell Django
python manage.py shell

# Migrations
python manage.py makemigrations
python manage.py migrate
```

---

## URLs Importantes

- **App Principal**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Upload**: http://localhost:8000/api/upload/

---

## Estrutura de Pastas

```
📁 denis-2/
├── 🐍 processor/          # App Django
│   ├── models.py          # ImageSession, ProcessingStep
│   ├── views.py           # API endpoints
│   ├── image_processor.py # Processamento de imagens
│   └── urls.py            # Rotas
├── 🎨 templates/          # HTML
├── 💅 static/             # CSS e JS
├── 📦 media/              # Imagens (criado automaticamente)
├── 🐳 Dockerfile          # Config Docker
├── 🐳 docker-compose.yml  # Orquestração
└── 📝 README.md           # Documentação completa
```

---

## Troubleshooting

### Porta 8000 já em uso?

```bash
# Mude a porta no docker-compose.yml:
ports:
  - "8080:8000"  # Agora acesse em localhost:8080
```

### Problemas com permissões de mídia?

```bash
# Docker
docker-compose exec web chmod -R 777 media/

# Local
chmod -R 777 media/
```

### Rebuild completo?

```bash
docker-compose down -v  # Remove volumes
docker-compose up --build
```

---

## Features Principais

✅ **Processamento de Imagens**
- Conversão para escala de cinza
- Ajustes de brilho, contraste e nitidez
- Aplicação de desfoque

✅ **Interface Moderna**
- Design cognitivo e ergonômico
- Drag & drop de arquivos
- Preview em tempo real
- Timeline visual de modificações

✅ **Funcionalidades**
- Histórico completo de edições
- Undo/Redo
- Download de imagens processadas
- Validação de arquivos

✅ **Tecnologias**
- Django 5.2 + Python 3.11
- uv para gerenciamento rápido
- Pillow para processamento
- Docker para deploy fácil

---

**Dúvidas?** Consulte o [README.md](README.md) completo!
