"""
Processador de imagens usando a biblioteca Pillow (PIL).

Este módulo contém a classe ImageProcessor que fornece métodos estáticos
para aplicar diversos ajustes e filtros a imagens, incluindo:
    - Conversão para escala de cinza
    - Ajuste de brilho, contraste e nitidez
    - Aplicação de desfoque (blur)
    - Extração de metadados da imagem

Todas as operações são não-destrutivas, ou seja, a imagem original nunca é modificada.
"""
from PIL import Image, ImageEnhance, ImageFilter
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class ImageProcessor:
    """
    Classe utilitária para processar imagens.

    Esta classe fornece métodos estáticos para aplicar diversos ajustes a imagens
    usando a biblioteca Pillow (PIL). Todos os métodos são estáticos, pois não
    mantêm estado interno.

    Nota:
        Atualmente, a renderização é feita no cliente (frontend) para melhor performance.
        Esta classe serve como fallback para navegadores antigos ou processamento server-side.
    """

    @staticmethod
    def convert_to_grayscale(image_path):
        """
        Converte uma imagem para escala de cinza (preto e branco).

        Args:
            image_path: Caminho para o arquivo de imagem ou objeto de arquivo

        Returns:
            InMemoryUploadedFile: Imagem convertida em memória

        Exemplo:
            >>> gray_image = ImageProcessor.convert_to_grayscale('foto.jpg')
        """
        img = Image.open(image_path)

        # Converte para escala de cinza (modo 'L' = Luminance/Grayscale)
        gray_img = img.convert('L')

        return ImageProcessor._save_image(gray_img, image_path)

    @staticmethod
    def adjust_brightness(image_path, factor):
        """
        Ajusta o brilho da imagem.

        Args:
            image_path: Caminho para o arquivo de imagem ou objeto de arquivo
            factor (float): Fator de ajuste de brilho
                - 0.0 = totalmente preto
                - 1.0 = brilho original (sem alteração)
                - 2.0 = muito brilhante

        Returns:
            InMemoryUploadedFile: Imagem com brilho ajustado

        Exemplo:
            >>> # Aumentar brilho em 20%
            >>> bright_image = ImageProcessor.adjust_brightness('foto.jpg', 1.2)
            >>> # Reduzir brilho em 50%
            >>> dark_image = ImageProcessor.adjust_brightness('foto.jpg', 0.5)
        """
        img = Image.open(image_path)

        # Se a imagem estiver em escala de cinza, converte para RGB
        # (necessário para aplicar enhancements)
        if img.mode == 'L':
            img = img.convert('RGB')

        # Cria um enhancer de brilho e aplica o fator
        enhancer = ImageEnhance.Brightness(img)
        bright_img = enhancer.enhance(factor)

        return ImageProcessor._save_image(bright_img, image_path)

    @staticmethod
    def adjust_contrast(image_path, factor):
        """
        Ajusta o contraste da imagem.

        Args:
            image_path: Caminho para o arquivo de imagem ou objeto de arquivo
            factor (float): Fator de ajuste de contraste
                - 0.0 = imagem totalmente cinza (sem contraste)
                - 1.0 = contraste original (sem alteração)
                - 2.0 = contraste muito alto

        Returns:
            InMemoryUploadedFile: Imagem com contraste ajustado

        Exemplo:
            >>> # Aumentar contraste
            >>> high_contrast = ImageProcessor.adjust_contrast('foto.jpg', 1.5)
            >>> # Reduzir contraste
            >>> low_contrast = ImageProcessor.adjust_contrast('foto.jpg', 0.7)
        """
        img = Image.open(image_path)

        # Se a imagem estiver em escala de cinza, converte para RGB
        if img.mode == 'L':
            img = img.convert('RGB')

        # Cria um enhancer de contraste e aplica o fator
        enhancer = ImageEnhance.Contrast(img)
        contrast_img = enhancer.enhance(factor)

        return ImageProcessor._save_image(contrast_img, image_path)

    @staticmethod
    def adjust_sharpness(image_path, factor):
        """
        Ajusta a nitidez (sharpness) da imagem.

        Args:
            image_path: Caminho para o arquivo de imagem ou objeto de arquivo
            factor (float): Fator de ajuste de nitidez
                - 0.0 = imagem totalmente desfocada
                - 1.0 = nitidez original (sem alteração)
                - 2.0 = imagem muito nítida

        Returns:
            InMemoryUploadedFile: Imagem com nitidez ajustada

        Exemplo:
            >>> # Aumentar nitidez
            >>> sharp_image = ImageProcessor.adjust_sharpness('foto.jpg', 1.5)
            >>> # Reduzir nitidez (efeito de suavização)
            >>> soft_image = ImageProcessor.adjust_sharpness('foto.jpg', 0.5)
        """
        img = Image.open(image_path)

        # Se a imagem estiver em escala de cinza, converte para RGB
        if img.mode == 'L':
            img = img.convert('RGB')

        # Cria um enhancer de nitidez e aplica o fator
        enhancer = ImageEnhance.Sharpness(img)
        sharp_img = enhancer.enhance(factor)

        return ImageProcessor._save_image(sharp_img, image_path)

    @staticmethod
    def apply_blur(image_path, radius):
        """
        Aplica desfoque gaussiano (Gaussian blur) à imagem.

        O desfoque gaussiano é um efeito de suavização que reduz detalhes
        e ruídos na imagem, criando um efeito de "fora de foco".

        Args:
            image_path: Caminho para o arquivo de imagem ou objeto de arquivo
            radius (int): Raio do desfoque
                - 0 = sem desfoque
                - 1-5 = desfoque leve a moderado
                - 6-10 = desfoque intenso (recomendado máximo)

        Returns:
            InMemoryUploadedFile: Imagem com desfoque aplicado

        Exemplo:
            >>> # Desfoque leve
            >>> blurred = ImageProcessor.apply_blur('foto.jpg', 2)
            >>> # Desfoque intenso
            >>> very_blurred = ImageProcessor.apply_blur('foto.jpg', 8)
        """
        img = Image.open(image_path)

        # Aplica o filtro de desfoque gaussiano com o raio especificado
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=radius))

        return ImageProcessor._save_image(blurred_img, image_path)

    @staticmethod
    def _save_image(img, original_path):
        """
        Salva uma imagem processada em memória (InMemoryUploadedFile).

        Método privado que converte a imagem PIL processada em um objeto
        InMemoryUploadedFile do Django, que pode ser armazenado em ImageField.

        Args:
            img (PIL.Image): Objeto de imagem PIL processada
            original_path: Caminho ou objeto de arquivo original (para extrair nome)

        Returns:
            InMemoryUploadedFile: Arquivo de imagem em memória pronto para salvar

        Nota:
            - Converte imagens RGBA para RGB (remove transparência)
            - Salva em formato JPEG com qualidade 95%
            - Adiciona fundo branco se a imagem tiver canal alpha
        """
        # Converte RGBA para RGB se necessário (JPEG não suporta transparência)
        if img.mode == 'RGBA':
            # Cria um fundo branco do mesmo tamanho da imagem
            background = Image.new('RGB', img.size, (255, 255, 255))

            # Cola a imagem sobre o fundo branco usando o canal alpha como máscara
            # split()[3] extrai o canal alpha (índice 3 = transparência)
            background.paste(img, mask=img.split()[3])
            img = background

        # Salva a imagem em um buffer de bytes em memória
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=95)  # Qualidade 95% (boa qualidade)
        output.seek(0)  # Volta ao início do buffer para leitura

        # Extrai o nome do arquivo original
        if hasattr(original_path, 'name'):
            filename = original_path.name
        else:
            filename = 'processed.jpg'

        # Cria um InMemoryUploadedFile compatível com Django
        return InMemoryUploadedFile(
            output,                      # Buffer de bytes da imagem
            'ImageField',                # Nome do campo do formulário
            filename,                    # Nome do arquivo
            'image/jpeg',                # Tipo MIME
            sys.getsizeof(output),       # Tamanho em bytes
            None                         # Charset (None para imagens)
        )

    @staticmethod
    def get_image_info(image_path):
        """
        Obtém metadados de uma imagem.

        Extrai informações básicas sobre a imagem sem modificá-la.

        Args:
            image_path: Caminho para o arquivo de imagem ou objeto de arquivo

        Returns:
            dict: Dicionário com metadados da imagem contendo:
                - width (int): Largura em pixels
                - height (int): Altura em pixels
                - format (str): Formato do arquivo (ex: 'JPEG', 'PNG')
                - mode (str): Modo de cor (ex: 'RGB', 'RGBA', 'L')

        Exemplo:
            >>> info = ImageProcessor.get_image_info('foto.jpg')
            >>> print(info)
            {'width': 1920, 'height': 1080, 'format': 'JPEG', 'mode': 'RGB'}
        """
        img = Image.open(image_path)

        return {
            'width': img.width,    # Largura da imagem em pixels
            'height': img.height,  # Altura da imagem em pixels
            'format': img.format,  # Formato do arquivo (JPEG, PNG, etc.)
            'mode': img.mode,      # Modo de cor (RGB, RGBA, L=grayscale, etc.)
        }
