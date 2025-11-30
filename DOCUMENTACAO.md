# Documentação Completa - Editor de Imagens Inteligente

## Índice
1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Funcionalidades Principais](#funcionalidades-principais)
4. [Modelos de Dados](#modelos-de-dados)
5. [API Endpoints](#api-endpoints)
6. [Processamento de Imagens](#processamento-de-imagens)
7. [Interface do Usuário](#interface-do-usuário)
8. [Fluxo de Trabalho](#fluxo-de-trabalho)
9. [Tecnologias Utilizadas](#tecnologias-utilizadas)
10. [Segurança](#segurança)

---

## Visão Geral

O **Editor de Imagens Inteligente** é uma aplicação web moderna que permite aos usuários processar e editar imagens com ajustes em tempo real. A aplicação implementa princípios de design cognitivo para criar uma experiência de usuário intuitiva e eficiente.

### Características Principais
- ✅ **Edição Não-Destrutiva**: Todos os ajustes são aplicados sobre a imagem original
- ✅ **Preview em Tempo Real**: Processamento no lado do cliente para feedback instantâneo
- ✅ **Timeline de Snapshots**: Sistema de histórico visual para comparações antes/depois
- ✅ **Persistência de Estado**: Ajustes salvos automaticamente no servidor
- ✅ **Download de Alta Qualidade**: Exportação da imagem processada em JPEG com 95% de qualidade
- ✅ **Interface Responsiva**: Design otimizado para diferentes tamanhos de tela

### Princípios de Design Implementados
1. **Feedback Imediato**: Preview em tempo real durante ajustes
2. **Edição Não-Destrutiva**: Preservação da imagem original
3. **Mensagens de Erro Claras**: Feedback contextual sobre problemas
4. **Divulgação Progressiva**: Interface organizada por níveis de complexidade
5. **Capacidade de Desfazer**: Timeline e reset para voltar ao estado anterior

---

## Arquitetura do Sistema

### Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Browser)                       │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │   app.js     │  │ image-processor  │  │  style.css   │  │
│  │ (Controller) │  │    -client.js    │  │   (UI)       │  │
│  │              │  │  (Canvas API)    │  │              │  │
│  └──────────────┘  └──────────────────┘  └──────────────┘  │
│         │                   │                               │
│         └───────────────────┴──── AJAX/Fetch API ───────┐  │
└─────────────────────────────────────────────────────────│──┘
                                                           │
                                    ┌──────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────┐
│                    BACKEND (Django)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   views.py   │  │   models.py  │  │   admin.py       │  │
│  │ (API Logic)  │  │  (Database)  │  │  (Admin Panel)   │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│         │                   │                               │
│         └───────────────────┴────── SQLite Database ───────│
└──────────────────────────────────────────────────────────────┘
```

### Componentes

#### Backend (Django)
- **Framework**: Django 5.2.8
- **Banco de Dados**: SQLite (desenvolvimento)
- **Armazenamento de Mídia**: Sistema de arquivos local
- **Autenticação**: Django Admin built-in

#### Frontend
- **HTML5**: Estrutura semântica
- **CSS3**: Estilos customizados com variáveis CSS
- **Vanilla JavaScript**: Sem frameworks, para máxima performance
- **Canvas API**: Processamento de imagens no cliente

#### Infraestrutura
- **Docker**: Containerização da aplicação
- **uv**: Gerenciador de pacotes Python otimizado
- **Nginx**: Servidor de arquivos estáticos (produção)

---

## Funcionalidades Principais

### 1. Upload de Imagens

#### Descrição
Permite aos usuários fazer upload de imagens através de:
- Clique no botão de upload
- Drag & drop de arquivos

#### Validações
- **Tipos permitidos**: JPG, JPEG, PNG, GIF
- **Tamanho máximo**: 10MB
- **Validação MIME type**: Verifica o tipo real do arquivo

#### Processo
1. Usuário seleciona ou arrasta arquivo
2. Validação no frontend (tipo e tamanho)
3. Upload via FormData para `/api/upload/`
4. Backend cria uma `ImageSession` com UUID único
5. Arquivo armazenado em `media/uploads/` com nome UUID
6. Retorna session_id e URL da imagem

#### Código de Exemplo (Frontend)
```javascript
async uploadImage(file) {
    const formData = new FormData();
    formData.append('image', file);

    const response = await fetch('/api/upload/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': this.csrfToken,
        },
        body: formData
    });

    const data = await response.json();
    // data.session_id, data.image_url
}
```

---

### 2. Ajustes de Imagem em Tempo Real

#### 2.1 Saturação (0-200%)
**Descrição**: Controla a intensidade das cores na imagem.

- **0%**: Escala de cinza (totalmente dessaturado)
- **100%**: Cores originais
- **200%**: Cores super saturadas

**Algoritmo**:
```javascript
// Conversão para escala de cinza usando luminosidade ponderada
const gray = 0.299 * r + 0.587 * g + 0.114 * b;
const satFactor = saturation / 100;

// Interpolação entre cinza e cor original
r = gray + (r - gray) * satFactor;
g = gray + (g - gray) * satFactor;
b = gray + (b - gray) * satFactor;
```

**Casos de Uso**:
- Criar efeito vintage (30-50%)
- Converter para preto e branco (0%)
- Intensificar cores (120-150%)

---

#### 2.2 Brilho (-100 a +100)
**Descrição**: Ajusta a luminosidade geral da imagem.

- **Valores negativos**: Escurece a imagem
- **0**: Brilho original
- **Valores positivos**: Clareia a imagem

**Algoritmo**:
```javascript
const brightnessFactor = brightness * 2.55; // Converte para range 0-255
r += brightnessFactor;
g += brightnessFactor;
b += brightnessFactor;
```

**Casos de Uso**:
- Corrigir fotos subexpostas (+30 a +60)
- Criar efeito de silhueta (-80 a -100)
- Ajustar iluminação inadequada

---

#### 2.3 Contraste (-100 a +100)
**Descrição**: Ajusta a diferença entre áreas claras e escuras.

- **Valores negativos**: Reduz contraste (imagem mais "plana")
- **0**: Contraste original
- **Valores positivos**: Aumenta contraste (maior diferença entre claro/escuro)

**Algoritmo**:
```javascript
const contrastFactor = (contrast + 100) / 100;
const factor = (259 * (contrastFactor * 255 + 255)) /
              (255 * (259 - contrastFactor * 255));

r = factor * (r - 128) + 128;
g = factor * (g - 128) + 128;
b = factor * (b - 128) + 128;
```

**Casos de Uso**:
- Melhorar legibilidade de texto em imagens (+20 a +40)
- Criar efeito dramático (+60 a +80)
- Suavizar imagens muito contrastadas (-20 a -40)

---

#### 2.4 Nitidez (-100 a +100)
**Descrição**: Ajusta a definição de bordas e detalhes.

- **Valores negativos**: Suaviza a imagem
- **0**: Nitidez original
- **Valores positivos**: Acentua bordas e detalhes

**Algoritmo**: Usa matriz de convolução (kernel 3x3)
```javascript
// Kernel de nitidez (unsharp mask)
const factor = sharpness / 100;
const kernel = [
    0, -factor, 0,
    -factor, 1 + 4 * factor, -factor,
    0, -factor, 0
];
```

**Aplicação**:
- Loop através de cada pixel
- Aplica convolução com pixels vizinhos
- Realça diferenças (bordas ficam mais definidas)

**Casos de Uso**:
- Melhorar fotos desfocadas (+30 a +50)
- Criar efeito HDR (+70 a +90)
- Reduzir ruído digital (-20 a -30)

---

#### 2.5 Desfoque (0 a 10)
**Descrição**: Aplica efeito de blur/desfoque à imagem.

- **0**: Sem desfoque
- **1-3**: Desfoque leve
- **4-7**: Desfoque médio
- **8-10**: Desfoque intenso

**Algoritmo**: Box blur (média de pixels vizinhos)
```javascript
const r = Math.round(blur);

// Para cada pixel
for (let dy = -r; dy <= r; dy++) {
    for (let dx = -r; dx <= r; dx++) {
        // Acumula valores RGB dos pixels vizinhos
        rSum += data[neighborIdx];
        gSum += data[neighborIdx + 1];
        bSum += data[neighborIdx + 2];
        count++;
    }
}

// Calcula média
pixel.r = rSum / count;
pixel.g = gSum / count;
pixel.b = bSum / count;
```

**Casos de Uso**:
- Efeito de profundidade de campo (2-4)
- Criar fundo desfocado (6-8)
- Efeito artístico abstrato (9-10)

---

### 3. Toggle de Escala de Cinza

**Descrição**: Botão dedicado para converter rapidamente para preto e branco.

**Funcionamento**:
- Define saturação para 0% (grayscale)
- Atualiza UI e estado visual
- Pode ser revertido clicando novamente (volta para 100%)

**Vantagem**: Mais rápido que ajustar manualmente o slider de saturação.

---

### 4. Sistema de Snapshots (Timeline)

#### Descrição
Sistema de histórico visual que permite:
- Salvar estados específicos da edição
- Comparar antes/depois
- Retornar a estados anteriores
- Criar múltiplas versões

#### Componentes

**4.1 Salvar Snapshot**
- Captura estado atual de todos os ajustes
- Gera descrição automática baseada nos ajustes aplicados
- Cria thumbnail do estado atual
- Armazena no banco de dados
- Adiciona ao timeline visual

**Descrição Automática**:
```javascript
// Exemplo de descrição gerada
"Escala de cinza, Brilho +30, Contraste +20"
"Saturação 150%, Desfoque 3"
"Ajustes personalizados" // quando não há ajustes significativos
```

**4.2 Timeline Visual**
- Exibe snapshots em ordem cronológica
- Mostra miniatura de cada estado
- Inclui sempre a imagem original como primeiro item
- Scroll horizontal para navegação
- Auto-scroll para o snapshot mais recente

**4.3 Carregar Snapshot**
- Clique em qualquer snapshot no timeline
- Restaura todos os ajustes daquele momento
- Atualiza sliders e preview em tempo real
- Toast de confirmação

**4.4 Persistência**
- Snapshots salvos no banco de dados
- Relacionados à sessão via chave estrangeira
- Ordenados por campo `order`
- Podem ser deletados (endpoint DELETE disponível)

---

### 5. Reset de Ajustes

**Descrição**: Retorna todos os ajustes aos valores padrão em um clique.

**Valores Padrão**:
```javascript
{
    saturation: 100,   // 100%
    brightness: 0,     // sem alteração
    contrast: 0,       // sem alteração
    sharpness: 0,      // sem alteração
    blur: 0            // sem desfoque
}
```

**Processo**:
1. Usuário clica em "Resetar Todos os Ajustes"
2. Frontend reseta controles visuais
3. Reaplica ajustes padrão à imagem
4. Envia atualização ao servidor (persistência)
5. Exibe toast de confirmação

---

### 6. Download de Imagem Processada

#### Descrição
Permite baixar a imagem com todos os ajustes aplicados.

#### Processo
1. Canvas renderizado com ajustes atuais
2. Conversão para Blob (JPEG 95% qualidade)
3. Criação de URL temporária
4. Download automático via elemento `<a>` invisível
5. Limpeza de memória (revoke URL)

#### Código
```javascript
async downloadImage() {
    const blob = await this.processor.getBlob(0.95);
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `processed_image_${Date.now()}.jpg`;
    a.click();

    URL.revokeObjectURL(url);
}
```

**Características**:
- Formato: JPEG
- Qualidade: 95% (otimização entre qualidade e tamanho)
- Nome: `processed_image_[timestamp].jpg`
- Download direto no navegador (sem request ao servidor)

---

### 7. Nova Imagem

**Descrição**: Reinicia o editor para processar nova imagem.

**Processo**:
1. Limpa estado da sessão atual
2. Remove snapshots do timeline (apenas visualmente)
3. Reseta controles
4. Volta para tela de upload
5. Libera recursos de memória (canvas, processor)

**Nota**: Dados no servidor (sessão antiga e snapshots) são preservados no banco de dados.

---

## Modelos de Dados

### ImageSession

**Descrição**: Representa uma sessão de edição de imagem.

**Campos**:
```python
class ImageSession(models.Model):
    id = UUIDField(primary_key=True)          # UUID único
    original_image = ImageField(upload_to='uploads/')  # Arquivo original
    adjustments = JSONField(default=dict)      # Estado atual dos ajustes
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**Métodos**:
- `get_adjustments()`: Retorna ajustes com valores padrão mesclados
- `update_adjustment(key, value)`: Atualiza ajuste específico
- `reset_adjustments()`: Restaura valores padrão

**Exemplo de adjustments JSON**:
```json
{
    "saturation": 75,
    "brightness": 20,
    "contrast": -10,
    "sharpness": 30,
    "blur": 0
}
```

---

### ProcessingSnapshot

**Descrição**: Armazena snapshots do timeline para comparação.

**Campos**:
```python
class ProcessingSnapshot(models.Model):
    id = UUIDField(primary_key=True)
    session = ForeignKey(ImageSession, related_name='snapshots')
    adjustments = JSONField()                  # Estado dos ajustes no momento
    preview_image = ImageField(upload_to='snapshots/', null=True)
    description = CharField(max_length=200)    # Descrição legível
    order = IntegerField(default=0)            # Ordem no timeline
    created_at = DateTimeField(auto_now_add=True)
```

**Relacionamento**:
- `session.snapshots.all()`: Lista todos os snapshots de uma sessão
- `session.snapshots.order_by('order')`: Ordenados para exibição

**Exemplo**:
```python
snapshot = ProcessingSnapshot.objects.create(
    session=session,
    adjustments={'saturation': 0, 'brightness': 20},
    description='Escala de cinza, Brilho +20',
    order=1
)
```

---

## API Endpoints

### Gerenciamento de Sessão

#### `POST /api/upload/`
**Descrição**: Upload de nova imagem e criação de sessão.

**Request**:
```http
POST /api/upload/
Content-Type: multipart/form-data

image: [arquivo binário]
```

**Response (200 OK)**:
```json
{
    "session_id": "8fa4e10a-533d-4c51-8d13-57cf51631918",
    "image_url": "/media/uploads/8fa4e10a-533d-4c51-8d13-57cf51631918.jpg",
    "adjustments": {
        "saturation": 100,
        "brightness": 0,
        "contrast": 0,
        "sharpness": 0,
        "blur": 0
    }
}
```

**Erros**:
- 400: Nenhuma imagem enviada
- 400: Arquivo muito grande (> 10MB)
- 400: Tipo de arquivo não permitido

---

### Ajustes

#### `GET /api/adjustments/<session_id>/`
**Descrição**: Obtém ajustes atuais da sessão.

**Response (200 OK)**:
```json
{
    "session_id": "8fa4e10a-533d-4c51-8d13-57cf51631918",
    "adjustments": {
        "saturation": 100,
        "brightness": 20,
        "contrast": 0,
        "sharpness": 0,
        "blur": 0
    }
}
```

---

#### `POST /api/adjustments/<session_id>/`
**Descrição**: Atualiza ajustes da sessão.

**Request**:
```json
{
    "adjustments": {
        "saturation": 75,
        "brightness": 30
    }
}
```

**Response (200 OK)**:
```json
{
    "success": true,
    "adjustments": {
        "saturation": 75,
        "brightness": 30,
        "contrast": 0,
        "sharpness": 0,
        "blur": 0
    }
}
```

**Nota**: Apenas os ajustes fornecidos são atualizados (merge).

---

#### `POST /api/adjustments/<session_id>/reset/`
**Descrição**: Reseta todos os ajustes para valores padrão.

**Response (200 OK)**:
```json
{
    "success": true,
    "adjustments": {
        "saturation": 100,
        "brightness": 0,
        "contrast": 0,
        "sharpness": 0,
        "blur": 0
    }
}
```

---

### Snapshots

#### `GET /api/snapshots/<session_id>/`
**Descrição**: Lista todos os snapshots da sessão.

**Response (200 OK)**:
```json
{
    "session_id": "8fa4e10a-533d-4c51-8d13-57cf51631918",
    "original_image": "/media/uploads/8fa4e10a-533d-4c51-8d13-57cf51631918.jpg",
    "current_adjustments": {
        "saturation": 100,
        "brightness": 0,
        "contrast": 0,
        "sharpness": 0,
        "blur": 0
    },
    "snapshots": [
        {
            "id": "a1b2c3d4-...",
            "description": "Escala de cinza",
            "adjustments": {"saturation": 0, "brightness": 0, ...},
            "order": 0,
            "created_at": "2025-11-29T20:30:00Z"
        }
    ]
}
```

---

#### `POST /api/snapshots/<session_id>/`
**Descrição**: Cria novo snapshot no timeline.

**Request**:
```json
{
    "description": "Versão com alto contraste",
    "adjustments": {
        "saturation": 100,
        "brightness": 0,
        "contrast": 50,
        "sharpness": 20,
        "blur": 0
    }
}
```

**Response (200 OK)**:
```json
{
    "snapshot_id": "b2c3d4e5-...",
    "description": "Versão com alto contraste",
    "adjustments": {...},
    "order": 2,
    "created_at": "2025-11-29T20:35:00Z"
}
```

---

#### `POST /api/snapshots/<session_id>/<snapshot_id>/load/`
**Descrição**: Carrega ajustes de um snapshot específico.

**Response (200 OK)**:
```json
{
    "success": true,
    "adjustments": {...},
    "snapshot_id": "b2c3d4e5-..."
}
```

**Efeito**: Atualiza `session.adjustments` com os valores do snapshot.

---

#### `DELETE /api/snapshots/<session_id>/<snapshot_id>/delete/`
**Descrição**: Remove snapshot do timeline.

**Response (200 OK)**:
```json
{
    "success": true,
    "message": "Snapshot removido"
}
```

---

### Download

#### `GET /api/download/<session_id>/`
**Descrição**: Download da imagem original (placeholder).

**Nota**: Atualmente retorna a imagem original. Em produção, deveria retornar a imagem renderizada no servidor ou recebida do cliente.

**Response**: Arquivo JPEG com header `Content-Disposition: attachment`

---

## Processamento de Imagens

### Arquitetura de Processamento

#### Client-Side (Preferencial)
**Vantagens**:
- ✅ Preview instantâneo (sem latência de rede)
- ✅ Reduz carga no servidor
- ✅ Escala melhor (processamento distribuído)
- ✅ Funciona offline para preview

**Tecnologia**: Canvas API + JavaScript
**Classe**: `ClientImageProcessor`

#### Server-Side (Backup)
**Quando usar**:
- Navegadores antigos sem suporte a Canvas
- Renderização de alta qualidade para download
- Processamento de lotes

**Tecnologia**: Pillow (PIL)
**Status**: Implementação parcial (placeholder)

---

### Fluxo de Processamento

#### 1. Carregamento da Imagem
```javascript
// Carrega imagem no canvas
const img = new Image();
img.crossOrigin = 'anonymous';
img.src = imageUrl;

// Armazena pixels originais
this.originalImageData = ctx.getImageData(0, 0, width, height);
```

#### 2. Aplicação de Ajustes (Non-Destructive)
```javascript
// SEMPRE começa da imagem original
const imageData = new ImageData(
    new Uint8ClampedArray(this.originalImageData.data),
    this.originalImageData.width,
    this.originalImageData.height
);

// Aplica ajustes em ordem específica
// 1. Saturação
// 2. Brilho
// 3. Contraste
// 4. Nitidez
// 5. Desfoque

// Renderiza resultado
ctx.putImageData(imageData, 0, 0);
```

**Ordem dos Ajustes**: A ordem é importante para qualidade!
1. **Saturação**: Primeiro para preservar informação de cor
2. **Brilho/Contraste**: Ajustes de luminosidade
3. **Nitidez**: Acentua bordas depois de ajustes básicos
4. **Desfoque**: Por último (destrutivo em relação a detalhes)

#### 3. Otimizações de Performance

**Throttling**: Limita frequência de processamento durante drag de slider
```javascript
const throttledUpdate = this.throttle(() => this.updatePreview(), 50);
// Máximo 20 atualizações por segundo
```

**Debouncing**: Adia salvamento no servidor
```javascript
clearTimeout(this.updateTimer);
this.updateTimer = setTimeout(async () => {
    // Salva no servidor após 500ms de inatividade
}, 500);
```

**Clamping**: Garante valores RGB válidos
```javascript
data[i] = Math.max(0, Math.min(255, r));
```

---

### Algoritmos Detalhados

#### Saturação (HSL Approach)
```
1. Converte RGB para luminosidade (L)
   L = 0.299*R + 0.587*G + 0.114*B

2. Interpola entre cinza e cor
   R' = L + (R - L) * (saturation / 100)
   G' = L + (G - L) * (saturation / 100)
   B' = L + (B - L) * (saturation / 100)
```

**Por que funciona**:
- saturation=0: R'=L, G'=L, B'=L (cinza)
- saturation=100: R'=R, G'=G, B'=B (original)
- saturation=200: amplifica diferença do cinza (super saturado)

---

#### Brilho (Additive)
```
R' = R + brightness * 2.55
G' = G + brightness * 2.55
B' = B + brightness * 2.55
```

**2.55**: Converte range -100/+100 para -255/+255

---

#### Contraste (Multiplicative)
```
factor = (259 * (contrast_pct * 255 + 255)) /
         (255 * (259 - contrast_pct * 255))

R' = factor * (R - 128) + 128
G' = factor * (G - 128) + 128
B' = factor * (B - 128) + 128
```

**128**: Ponto médio de 0-255
**Por que funciona**: Amplifica diferença do meio-tom

---

#### Nitidez (Unsharp Mask)
Matriz de convolução 3x3:
```
     0      -factor     0
  -factor  1+4*factor  -factor
     0      -factor     0
```

Para cada pixel, multiplica valores vizinhos pela matriz.

**Efeito**:
- Centro amplificado
- Vizinhos subtraídos
- Resultado: bordas acentuadas

---

#### Desfoque (Box Blur)
```
Para cada pixel:
  soma = 0
  conta = 0

  Para cada vizinho em raio R:
    soma += cor_vizinho
    conta++

  nova_cor = soma / conta
```

**Complexidade**: O(n × m × r²) onde r é o raio
**Otimização possível**: Blur separável (horizontal + vertical)

---

## Interface do Usuário

### Componentes Visuais

#### 1. Header
```html
<header class="header">
    <h1>Editor de Imagens</h1>
    <p>Transforme suas imagens com controles intuitivos</p>
</header>
```

**Design**:
- Ícone SVG de imagem
- Título claro
- Subtítulo explicativo

---

#### 2. Área de Upload
```html
<div class="upload-area" id="uploadArea">
    <input type="file" accept="image/*">
    <label>
        <svg>...</svg>
        <span>Clique ou arraste uma imagem aqui</span>
        <span>JPG, PNG ou GIF (máx. 10MB)</span>
    </label>
</div>
```

**Estados**:
- Normal: Borda tracejada cinza
- Hover: Borda sólida azul
- Drag-over: Background azul claro
- Error: Borda vermelha

**Acessibilidade**:
- Label associado ao input
- Texto descritivo de formatos
- Feedback visual de estados

---

#### 3. Display de Imagem
```html
<div class="image-display__container">
    <img id="currentImage" src="...">
    <canvas id="editorCanvas" style="display:none"></canvas>
    <div class="image-display__info">1920 × 1080px</div>
</div>
```

**Características**:
- Canvas oculto (processamento)
- Img visível (display)
- Info overlay com dimensões

---

#### 4. Painel de Controles

**Toggle de Escala de Cinza**:
```html
<button class="control-btn control-btn--toggle" id="grayscaleToggle">
    <svg>...</svg>
    <span>Escala de Cinza</span>
</button>
```

**Slider com Marcadores**:
```html
<div class="control-group">
    <label class="control-label">
        <svg>...</svg>
        <span>Saturação</span>
        <span class="control-value">100%</span>
    </label>
    <input type="range" min="0" max="200" value="100">
    <div class="control-markers">
        <span>0%</span>
        <span>100%</span>
        <span>200%</span>
    </div>
</div>
```

**Design**:
- Ícone visual para cada ajuste
- Label descritivo
- Valor atual em tempo real
- Marcadores de referência nos extremos

---

#### 5. Timeline de Snapshots
```html
<div class="timeline__track">
    <div class="timeline__item timeline__item--original">
        <div class="timeline__dot"></div>
        <div class="timeline__content">
            <div class="timeline__label">Original</div>
            <img class="timeline__preview" src="...">
        </div>
    </div>
    <!-- Snapshots adicionados dinamicamente -->
</div>
```

**Interatividade**:
- Scroll horizontal
- Clique para carregar snapshot
- Auto-scroll para mais recente
- Preview em miniatura

---

#### 6. Botões de Ação
```html
<section class="actions">
    <button class="action-btn action-btn--secondary">
        <svg>...</svg>
        Nova Imagem
    </button>
    <button class="action-btn action-btn--primary">
        <svg>...</svg>
        Baixar Imagem
    </button>
</section>
```

**Hierarquia Visual**:
- Primário (azul): Ação principal (Download)
- Secundário (cinza): Ação alternativa (Nova Imagem)

---

#### 7. Feedback do Sistema

**Loading Indicator**:
```html
<div class="loading" id="loading">
    <div class="loading__spinner"></div>
    <p>Processando...</p>
</div>
```

**Toast Notifications**:
```html
<div class="toast success">Imagem carregada com sucesso!</div>
<div class="toast error">Erro ao processar imagem</div>
```

**Estados**:
- `success`: Verde, ícone de check
- `error`: Vermelho, ícone de X
- `info`: Azul, ícone de info

---

### Paleta de Cores

```css
:root {
    --primary: #3b82f6;        /* Azul principal */
    --primary-hover: #2563eb;  /* Azul hover */
    --success: #10b981;        /* Verde sucesso */
    --error: #ef4444;          /* Vermelho erro */
    --gray-50: #f9fafb;        /* Background claro */
    --gray-200: #e5e7eb;       /* Bordas */
    --gray-700: #374151;       /* Texto */
    --gray-900: #111827;       /* Texto escuro */
}
```

---

### Tipografia

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
             Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;

/* Hierarquia */
h1: 2rem (32px), bold
h2: 1.5rem (24px), semibold
body: 1rem (16px), normal
small: 0.875rem (14px)
```

---

## Fluxo de Trabalho

### Fluxo Completo do Usuário

```
1. [Acessa aplicação] → localhost:8000
        ↓
2. [Vê tela de upload]
        ↓
3. [Seleciona/Arrasta imagem]
        ↓
4. [Validação frontend] → Tipo e tamanho OK?
        ↓ Sim
5. [Upload para servidor] → POST /api/upload/
        ↓
6. [Servidor cria sessão] → UUID gerado
        ↓
7. [Imagem armazenada] → media/uploads/
        ↓
8. [Editor carregado]
        ↓
9. [Imagem carregada no canvas] → Pixels originais armazenados
        ↓
10. [Usuário ajusta sliders] → Preview em tempo real (50ms throttle)
        ↓
11. [Slider released] → Salva no servidor (500ms debounce)
         ↓
12. [Usuário satisfeito] → Clica "Salvar Snapshot"
         ↓
13. [Snapshot criado] → POST /api/snapshots/
         ↓
14. [Adicionado ao timeline] → Thumbnail gerado
         ↓
15. [Mais edições...] ou [Clica Download]
         ↓
16. [Canvas → Blob → Download] → processed_image_[timestamp].jpg
         ↓
17. [Nova Imagem?] → Volta para passo 2
```

---

### Fluxo de Dados

#### Upload
```
Frontend                    Backend                  Database
   │                           │                         │
   │── FormData ─────────────→ │                         │
   │   (image file)            │                         │
   │                           │                         │
   │                           │── CREATE Session ─────→ │
   │                           │   (UUID, image)         │
   │                           │                         │
   │                           │←─ Session saved ─────── │
   │                           │                         │
   │←─ JSON Response ────────  │                         │
   │   (session_id, url)       │                         │
```

#### Ajuste em Tempo Real
```
Frontend                    Backend                  Database
   │                           │                         │
   │── Canvas Processing ───→  │ (não envia)             │
   │   (local, instant)        │                         │
   │                           │                         │
   │── Slider Release ───────→ │                         │
   │   POST /adjustments       │                         │
   │                           │                         │
   │                           │── UPDATE Session ─────→ │
   │                           │   (adjustments JSON)    │
   │                           │                         │
   │←─ Success ──────────────  │                         │
```

#### Snapshot
```
Frontend                    Backend                  Database
   │                           │                         │
   │── POST /snapshots ──────→ │                         │
   │   (adjustments, desc)     │                         │
   │                           │                         │
   │                           │── CREATE Snapshot ────→ │
   │                           │   (session FK)          │
   │                           │                         │
   │←─ Snapshot Data ─────────  │                         │
   │   (id, adjustments)       │                         │
   │                           │                         │
   │── Render Thumbnail ─────→ │ (local canvas)          │
   │   Add to Timeline         │                         │
```

---

## Tecnologias Utilizadas

### Backend

#### Django 5.2.8
- **Framework web**: MTV (Model-Template-View)
- **ORM**: Mapeamento objeto-relacional
- **Admin**: Interface administrativa automática
- **Middleware**: CSRF, CORS, sessões
- **Validação**: Forms e serializers

#### Bibliotecas Python
```toml
[project]
dependencies = [
    "django>=5.2,<6.0",
    "pillow>=11.0,<12.0",      # Processamento de imagens
    "django-cors-headers>=4.6", # CORS
]
```

#### uv (Package Manager)
- Instalação rápida de dependências
- Resolução determinística
- Cache eficiente

---

### Frontend

#### HTML5
- Semântica moderna
- Acessibilidade (ARIA)
- Forms nativos

#### CSS3
```css
/* Recursos utilizados */
- CSS Grid Layout
- Flexbox
- CSS Variables (Custom Properties)
- Transitions
- Media Queries
- Transform
```

#### JavaScript (ES6+)
```javascript
// Features utilizadas
- Classes
- Arrow Functions
- Async/Await
- Promises
- Template Literals
- Destructuring
- Spread Operator
- Modules (futuro)
```

#### Canvas API
```javascript
// Métodos principais
ctx.drawImage()
ctx.getImageData()
ctx.putImageData()
canvas.toBlob()
canvas.toDataURL()
```

---

### Infraestrutura

#### Docker
```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - media_data:/app/media
    environment:
      - DEBUG=1
```

#### SQLite
- Banco de dados file-based
- Zero configuração
- Ideal para desenvolvimento
- Migração simples para PostgreSQL/MySQL

---

## Segurança

### Proteção CSRF

#### Implementação
1. **Django gera token** via `@ensure_csrf_cookie`
2. **Cookie enviado** ao browser
3. **JavaScript lê cookie** via `document.cookie`
4. **Token incluído** em headers: `X-CSRFToken`
5. **Django valida** via `CsrfViewMiddleware`

#### Código Frontend
```javascript
getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return decodeURIComponent(value);
        }
    }
    return null;
}

// Uso
headers: {
    'X-CSRFToken': this.getCookie('csrftoken')
}
```

---

### Validação de Upload

#### Tamanho
```python
if image.size > 10485760:  # 10MB
    return JsonResponse({
        'error': 'Arquivo muito grande (máximo 10MB)'
    }, status=400)
```

#### Tipo de Arquivo
```python
allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
if image.content_type not in allowed_types:
    return JsonResponse({
        'error': 'Tipo de arquivo não permitido'
    }, status=400)
```

**Nota**: Valida MIME type real, não apenas extensão.

---

### CORS

```python
# settings.py
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOW_ALL_ORIGINS = True  # Apenas desenvolvimento!
```

**Produção**: Configurar domínios específicos
```python
CORS_ALLOWED_ORIGINS = [
    'https://exemplo.com',
    'https://app.exemplo.com',
]
```

---

### Sanitização de Nomes de Arquivo

```python
import uuid

def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)
```

**Benefícios**:
- ✅ Evita path traversal
- ✅ Previne sobrescrita
- ✅ Nomes únicos garantidos
- ✅ Sem caracteres especiais

---

### Headers de Segurança

```python
# Django automático
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
```

---

## Melhorias Futuras

### Funcionalidades
- [ ] Histórico de undo/redo completo
- [ ] Mais filtros (sepia, vignette, temperatura de cor)
- [ ] Crop e redimensionamento
- [ ] Rotação e flip
- [ ] Suporte a formatos RAW
- [ ] Processamento em batch
- [ ] Exportação em múltiplos formatos (PNG, WebP)
- [ ] Compartilhamento social direto

### Performance
- [ ] Web Workers para processamento
- [ ] WebGL para aceleração GPU
- [ ] Progressive Web App (PWA)
- [ ] Service Worker para cache
- [ ] Lazy loading de snapshots
- [ ] Otimização de algoritmos de blur/sharpen

### UX
- [ ] Modo escuro
- [ ] Atalhos de teclado
- [ ] Tutoriais interativos
- [ ] Comparação lado a lado (before/after slider)
- [ ] Presets de filtros (Instagram-like)
- [ ] Histórico visual de edições

### Infraestrutura
- [ ] Migração para PostgreSQL
- [ ] CDN para arquivos estáticos
- [ ] Redis para cache de sessões
- [ ] Celery para processamento assíncrono
- [ ] S3/Cloud Storage para mídia
- [ ] CI/CD pipeline
- [ ] Testes automatizados (unit, integration, e2e)
- [ ] Monitoramento e logging (Sentry)

---

## Conclusão

Este documento fornece uma visão completa da aplicação **Editor de Imagens Inteligente**, cobrindo desde a arquitetura até os detalhes de implementação de cada funcionalidade. A aplicação combina processamento moderno no cliente com persistência robusta no servidor, resultando em uma experiência de usuário fluida e profissional.

**Principais Destaques**:
- ✅ Edição não-destrutiva com preview em tempo real
- ✅ Sistema de snapshots para comparação visual
- ✅ Algoritmos otimizados de processamento de imagem
- ✅ Interface intuitiva e responsiva
- ✅ Segurança com validação CSRF e sanitização
- ✅ Arquitetura escalável e manutenível

Para dúvidas ou contribuições, consulte os arquivos de código-fonte ou a documentação adicional em `/docs/`.
