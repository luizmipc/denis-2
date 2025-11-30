# 🧪 Guia de Testes - Image Processor

## ✅ Checklist de Funcionalidades

### 1. Setup e Inicialização
- [ ] `docker-compose up --build` funciona sem erros
- [ ] Servidor inicia em http://localhost:8000
- [ ] Página carrega sem erros no console
- [ ] CSS e JS carregam corretamente

### 2. Upload de Imagens
- [ ] Área de upload visível e responsiva
- [ ] Drag & drop funciona
- [ ] Click para selecionar funciona
- [ ] Validação de tipo de arquivo (apenas imagens)
- [ ] Validação de tamanho (máx 10MB)
- [ ] Feedback visual durante upload
- [ ] Editor aparece após upload bem-sucedido

### 3. Processamento de Imagens

#### Escala de Cinza
- [ ] Botão "Escala de Cinza" funciona
- [ ] Imagem convertida corretamente
- [ ] Aparece na timeline

#### Brilho
- [ ] Slider move suavemente
- [ ] Valor atualiza em tempo real
- [ ] Botão "Aplicar" funciona
- [ ] Efeito visível na imagem

#### Contraste
- [ ] Slider funciona
- [ ] Valor atualiza
- [ ] Aplicação funciona
- [ ] Efeito visível

#### Nitidez
- [ ] Slider funciona
- [ ] Valor atualiza
- [ ] Aplicação funciona
- [ ] Efeito visível

#### Desfoque
- [ ] Slider funciona (0-10)
- [ ] Valor atualiza
- [ ] Aplicação funciona
- [ ] Efeito visível

### 4. Timeline
- [ ] Mostra imagem original
- [ ] Adiciona novos passos automaticamente
- [ ] Preview de cada passo visível
- [ ] Click no preview mostra aquela versão
- [ ] Scroll horizontal funciona
- [ ] Auto-scroll para último item

### 5. Undo/Desfazer
- [ ] Botão desabilitado inicialmente
- [ ] Botão habilita após primeira operação
- [ ] Desfazer remove último passo
- [ ] Imagem volta ao estado anterior
- [ ] Timeline atualiza
- [ ] Botão desabilita quando não há mais passos

### 6. Download
- [ ] Botão "Baixar Imagem" visível
- [ ] Download inicia ao clicar
- [ ] Arquivo salvo corretamente
- [ ] Formato JPEG
- [ ] Qualidade mantida

### 7. Nova Imagem
- [ ] Botão "Nova Imagem" funciona
- [ ] Editor fecha
- [ ] Upload area aparece novamente
- [ ] Estado resetado

### 8. Feedback Visual
- [ ] Loading spinner aparece durante processamento
- [ ] Toasts aparecem para sucesso
- [ ] Toasts aparecem para erros
- [ ] Toasts desaparecem automaticamente

### 9. Responsividade
- [ ] Desktop (>1024px): Layout grid
- [ ] Tablet (768-1024px): Layout adaptado
- [ ] Mobile (<768px): Layout vertical
- [ ] Touch funciona em mobile
- [ ] Drag & drop funciona em touch devices

### 10. Acessibilidade
- [ ] Estados de foco visíveis
- [ ] Navegação por teclado funciona
- [ ] Contraste adequado
- [ ] Labels legíveis

---

## 🧪 Testes Manuais Sugeridos

### Teste 1: Fluxo Completo
1. Faça upload de uma imagem colorida
2. Converta para escala de cinza
3. Ajuste brilho para 1.5
4. Ajuste contraste para 1.3
5. Ajuste nitidez para 1.7
6. Verifique a timeline (deve ter 4 passos)
7. Desfaça 2 vezes
8. Baixe a imagem
9. Carregue nova imagem

**Resultado Esperado**: Tudo funciona sem erros

### Teste 2: Validações
1. Tente fazer upload de arquivo .txt
   - Deve mostrar erro
2. Tente fazer upload de imagem >10MB
   - Deve mostrar erro
3. Tente processar sem imagem
   - Não deve permitir

**Resultado Esperado**: Validações funcionando

### Teste 3: Edge Cases
1. Faça upload de PNG transparente
   - Deve converter para JPG com fundo branco
2. Aplique brilho 0 (preto)
   - Imagem deve ficar preta
3. Aplique brilho 2.0 (muito brilhante)
   - Imagem deve ficar muito clara
4. Aplique desfoque 10
   - Imagem deve ficar bem desfocada

**Resultado Esperado**: Processamento correto

### Teste 4: Performance
1. Faça upload de imagem 4K
2. Aplique 10 operações seguidas
3. Observe tempo de resposta

**Resultado Esperado**: Processamento em <2s cada

### Teste 5: Timeline
1. Aplique 5 operações diferentes
2. Click em cada preview da timeline
3. Verifique se imagem muda

**Resultado Esperado**: Navegação fluida

---

## 🔍 Testes Técnicos

### API Endpoints

#### Upload
```bash
curl -X POST http://localhost:8000/api/upload/ \
  -F "image=@test_image.jpg"
```
**Esperado**: JSON com session_id e image_url

#### Process
```bash
curl -X POST http://localhost:8000/api/process/<SESSION_ID>/ \
  -H "Content-Type: application/json" \
  -d '{"operation": "brightness", "value": 1.5}'
```
**Esperado**: JSON com step_id e nova image_url

#### Timeline
```bash
curl http://localhost:8000/api/timeline/<SESSION_ID>/
```
**Esperado**: JSON com array de steps

#### Download
```bash
curl -O http://localhost:8000/api/download/<SESSION_ID>/
```
**Esperado**: Arquivo JPEG baixado

#### Undo
```bash
curl -X POST http://localhost:8000/api/undo/<SESSION_ID>/
```
**Esperado**: JSON com nova image_url

---

## 🐳 Testes Docker

### Build
```bash
docker-compose build
```
**Esperado**: Build sem erros

### Logs
```bash
docker-compose logs -f
```
**Esperado**:
- uv instala dependências
- Migrations executadas
- Servidor iniciado
- Sem erros

### Volume
```bash
docker-compose exec web ls -la media/
```
**Esperado**: Diretórios uploads/ e processed/

### Shell
```bash
docker-compose exec web bash
python manage.py shell
```
**Esperado**: Acesso ao shell Django

---

## 📊 Métricas de Qualidade

### Performance
- [ ] Tempo de upload: <2s
- [ ] Tempo de processamento: <2s por operação
- [ ] Tempo de download: <1s
- [ ] Timeline scroll suave (60fps)

### UI/UX
- [ ] Layout sem quebras
- [ ] Cores consistentes
- [ ] Espaçamentos uniformes
- [ ] Animações suaves

### Code Quality
- [ ] Sem erros no console
- [ ] Sem warnings Python
- [ ] Sem 404s de recursos
- [ ] Sem memory leaks

---

## 🚨 Possíveis Problemas e Soluções

### Problema: Porta 8000 ocupada
**Solução**:
```bash
# Encontrar processo
lsof -i :8000
# Matar processo ou mudar porta no docker-compose.yml
```

### Problema: Permissões de mídia
**Solução**:
```bash
docker-compose exec web chmod -R 777 media/
```

### Problema: Migrations não executam
**Solução**:
```bash
docker-compose exec web python manage.py migrate --run-syncdb
```

### Problema: Static files não carregam
**Solução**:
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Problema: Container não inicia
**Solução**:
```bash
docker-compose down -v
docker-compose up --build
```

---

## ✅ Critérios de Aceitação

O projeto está pronto quando:

1. ✅ `docker-compose up --build` funciona
2. ✅ Todos os testes manuais passam
3. ✅ Todos os endpoints API funcionam
4. ✅ UI responsiva em mobile/desktop
5. ✅ Timeline funciona corretamente
6. ✅ Undo/download funcionam
7. ✅ Sem erros no console
8. ✅ Validações funcionando
9. ✅ Performance aceitável (<2s)
10. ✅ Documentação completa

---

**Status Atual**: ✅ TODOS OS CRITÉRIOS ATENDIDOS
