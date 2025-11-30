from PIL import Image, ImageEnhance, ImageFilter
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class ImageProcessor:
    """Handle image processing operations"""

    @staticmethod
    def convert_to_grayscale(image_path):
        """Convert image to grayscale"""
        img = Image.open(image_path)
        # Convert to grayscale
        gray_img = img.convert('L')
        return ImageProcessor._save_image(gray_img, image_path)

    @staticmethod
    def adjust_brightness(image_path, factor):
        """
        Adjust image brightness
        factor: 0.0 = black, 1.0 = original, 2.0 = very bright
        """
        img = Image.open(image_path)
        if img.mode == 'L':
            # Convert grayscale to RGB for enhancement
            img = img.convert('RGB')
        enhancer = ImageEnhance.Brightness(img)
        bright_img = enhancer.enhance(factor)
        return ImageProcessor._save_image(bright_img, image_path)

    @staticmethod
    def adjust_contrast(image_path, factor):
        """
        Adjust image contrast
        factor: 0.0 = gray, 1.0 = original, 2.0 = high contrast
        """
        img = Image.open(image_path)
        if img.mode == 'L':
            img = img.convert('RGB')
        enhancer = ImageEnhance.Contrast(img)
        contrast_img = enhancer.enhance(factor)
        return ImageProcessor._save_image(contrast_img, image_path)

    @staticmethod
    def adjust_sharpness(image_path, factor):
        """
        Adjust image sharpness
        factor: 0.0 = blurred, 1.0 = original, 2.0 = sharp
        """
        img = Image.open(image_path)
        if img.mode == 'L':
            img = img.convert('RGB')
        enhancer = ImageEnhance.Sharpness(img)
        sharp_img = enhancer.enhance(factor)
        return ImageProcessor._save_image(sharp_img, image_path)

    @staticmethod
    def apply_blur(image_path, radius):
        """
        Apply Gaussian blur
        radius: blur radius (0-10 recommended)
        """
        img = Image.open(image_path)
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=radius))
        return ImageProcessor._save_image(blurred_img, image_path)

    @staticmethod
    def _save_image(img, original_path):
        """Save processed image to InMemoryUploadedFile"""
        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
            img = background

        # Save to bytes buffer
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=95)
        output.seek(0)

        # Get filename from original path
        if hasattr(original_path, 'name'):
            filename = original_path.name
        else:
            filename = 'processed.jpg'

        # Create InMemoryUploadedFile
        return InMemoryUploadedFile(
            output,
            'ImageField',
            filename,
            'image/jpeg',
            sys.getsizeof(output),
            None
        )

    @staticmethod
    def get_image_info(image_path):
        """Get image metadata"""
        img = Image.open(image_path)
        return {
            'width': img.width,
            'height': img.height,
            'format': img.format,
            'mode': img.mode,
        }
