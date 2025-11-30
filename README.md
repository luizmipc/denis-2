# Editor de Imagens - Image Processor

Um aplicativo Django moderno para processamento de imagens com interface intuitiva, desenvolvido com princípios de design cognitivo e ergonômico.

## 🎨 Características

### Funcionalidades de Processamento
- **Conversão para Escala de Cinza**: Transforme imagens coloridas em preto e branco
- **Ajuste de Brilho**: Controle a luminosidade da imagem (0.0 - 2.0)
- **Ajuste de Contraste**: Modifique o contraste (0.0 - 2.0)
- **Ajuste de Nitidez**: Controle a nitidez da imagem (0.0 - 2.0)
- **Desfoque**: Aplique desfoque gaussiano (0 - 10)

### Interface e UX
- **Timeline Visual**: Visualize todo o histórico de modificações
- **Undo/Desfazer**: Volte atrás em qualquer modificação
- **Preview em Tempo Real**: Veja os valores dos controles enquanto ajusta
- **Download Rápido**: Baixe a imagem processada em um clique
- **Drag & Drop**: Arraste imagens diretamente para o upload
- **Feedback Visual**: Notificações claras de sucesso e erro

### Design Principles Aplicados

#### 1. **Design Cognitivo**
- **Clareza Visual**: Hierarquia clara com contraste alto
- **Affordance**: Elementos interativos visualmente distintos
- **Feedback Imediato**: Respostas visuais instantâneas para todas as ações
- **Modelo Mental**: Interface intuitiva que reflete processos de edição familiares

#### 2. **Design Ergonômico**
- **Lei de Fitts**: Botões e controles grandes e fáceis de clicar
- **Chunking**: Informações agrupadas logicamente
- **Proximidade**: Controles relacionados ficam próximos
- **Espaçamento**: Uso generoso de espaço em branco para reduzir fadiga visual

#### 3. **Princípios Gestalt**
- **Proximidade**: Elementos relacionados agrupados
- **Similaridade**: Elementos similares têm aparência similar
- **Continuidade**: Fluxo visual suave através da interface
- **Closure**: Elementos visuais completos e fechados

## 🚀 Tecnologias

- **Backend**: Django 5.2.8
- **Gerenciamento de Pacotes**: [uv](https://docs.astral.sh/uv/) - Extremamente rápido
- **Processamento de Imagens**: Pillow 12.0.0
- **Computação Numérica**: NumPy 2.3.5
- **Containerização**: Docker & Docker Compose
- **Python**: 3.11+

## 📦 Instalação e Configuração

### ⚡ Setup Automático com Docker (Recomendado)

**Tudo é automatizado! Apenas um comando e está pronto!**

#### Pré-requisitos
- Docker e Docker Compose instalados
- Git

#### Instalação

```bash
# Clone o repositório
git clone <repository-url>
cd denis-2

# 🚀 Execute este ÚNICO comando:
docker-compose up --build

# Pronto! A aplicação estará disponível em http://localhost:8000
```

**O que acontece automaticamente:**
- ✅ Instalação de todas as dependências Python com uv
- ✅ Execução de migrações do banco de dados
- ✅ Criação de diretórios de mídia
- ✅ Coleta de arquivos estáticos
- ✅ Início do servidor de desenvolvimento

**Para parar:**
```bash
# Pressione Ctrl+C e depois:
docker-compose down
```

**Para reiniciar:**
```bash
docker-compose up
# Sem --build se não mudou o código
```

### 🛠️ Opção 2: Executar Localmente com uv

#### Script Automático
```bash
# Clone o repositório
git clone <repository-url>
cd denis-2

# Execute o script automático
chmod +x run.sh
./run.sh

# A aplicação estará disponível em http://localhost:8000
```

#### Instalação Manual
```bash
# Clone o repositório
git clone <repository-url>
cd denis-2

# Instale uv (se ainda não tiver)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Crie o ambiente virtual e instale dependências
uv venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
uv pip install django pillow numpy django-cors-headers

# Execute as migrações
python manage.py migrate

# Crie diretórios de mídia
mkdir -p media/uploads media/processed

# Execute o servidor de desenvolvimento
python manage.py runserver

# A aplicação estará disponível em http://localhost:8000
```

## 🎯 Como Usar

### 1. Upload de Imagem
- Clique na área de upload ou arraste uma imagem
- Formatos suportados: JPG, PNG, GIF
- Tamanho máximo: 10MB

### 2. Processamento
- Use os controles deslizantes para ajustar valores
- Clique em "Aplicar" para cada modificação
- O botão "Escala de Cinza" converte imediatamente

### 3. Timeline
- Visualize todo o histórico de modificações
- Clique em qualquer preview para ver aquele estado
- Use "Desfazer" para remover a última modificação

### 4. Download
- Clique em "Baixar Imagem" para salvar o resultado final
- A imagem será salva como JPEG de alta qualidade

## 📁 Estrutura do Projeto

```
denis-2/
├── config/                 # Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── processor/              # App principal
│   ├── models.py          # ImageSession, ProcessingStep
│   ├── views.py           # API endpoints e views
│   ├── urls.py            # Rotas
│   └── image_processor.py # Lógica de processamento
├── templates/
│   └── processor/
│       └── index.html     # Interface principal
├── static/
│   ├── css/
│   │   └── style.css     # Estilos com design cognitivo
│   └── js/
│       └── app.js        # Controlador interativo
├── media/                 # Arquivos de mídia (criado automaticamente)
│   ├── uploads/          # Imagens originais
│   └── processed/        # Imagens processadas
├── Dockerfile            # Configuração Docker
├── docker-compose.yml    # Orquestração Docker
├── pyproject.toml        # Dependências uv
└── README.md
```

## 🔧 API Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Interface principal |
| `/api/upload/` | POST | Upload de imagem |
| `/api/process/<session_id>/` | POST | Aplicar operação |
| `/api/timeline/<session_id>/` | GET | Obter histórico |
| `/api/download/<session_id>/` | GET | Baixar imagem |
| `/api/undo/<session_id>/` | POST | Desfazer última operação |

## 🎨 Princípios de Design Implementados

### Cores
- **Azul Primário** (#3b82f6): Confiança e profissionalismo
- **Verde** (#10b981): Sucesso e ações positivas
- **Vermelho** (#ef4444): Erros e avisos
- **Tons Neutros**: Alto contraste para acessibilidade

### Tipografia
- Fontes system-ui para melhor legibilidade
- Tamanhos escalonados (0.875rem - 1.875rem)
- Peso apropriado para hierarquia visual

### Espaçamento
- Sistema de espaçamento consistente (0.5rem - 3rem)
- Uso generoso de espaço em branco
- Alinhamento e grid precisos

### Animações
- Transições suaves (150ms - 350ms)
- Feedback visual em hover e click
- Loading states claros

### Acessibilidade
- Estados de foco visíveis
- Alto contraste de cores
- Ícons com texto descritivo
- Responsivo (mobile-first)

## 🔄 Fluxo de Processamento

1. **Upload**: Usuário envia imagem → Validação → Criação de sessão
2. **Processamento**: Seleção de operação → Ajuste de parâmetros → Aplicação
3. **Timeline**: Cada passo salvo → Preview gerado → Histórico atualizado
4. **Download**: Última versão processada → Conversão JPEG → Download

## 🐳 Docker

O projeto usa Docker para garantir consistência entre ambientes:

- **Base Image**: Python 3.11-slim
- **uv**: Instalado diretamente do ghcr.io
- **Volume**: Dados de mídia persistentes
- **Port**: 8000 (mapeado para host)

## 📝 Desenvolvimento

### Adicionar Nova Operação de Processamento

1. **Adicione ao modelo** (`processor/models.py`):
```python
OPERATION_CHOICES = [
    # ... existentes
    ('nova_operacao', 'Nova Operação'),
]
```

2. **Implemente o processador** (`processor/image_processor.py`):
```python
@staticmethod
def nova_operacao(image_path, param):
    # Sua lógica aqui
    pass
```

3. **Adicione à view** (`processor/views.py`):
```python
elif operation == 'nova_operacao':
    processed = ImageProcessor.nova_operacao(source_image.path, value)
```

4. **Adicione controle na UI** (`templates/processor/index.html` e `static/js/app.js`)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é desenvolvido para fins educacionais.

## 👨‍💻 Autor

Desenvolvido com foco em UX/UI, design cognitivo e ergonômico.

---

**Nota**: Este projeto demonstra a aplicação prática de princípios de design cognitivo e ergonômico em desenvolvimento web, com ênfase em usabilidade e experiência do usuário.
