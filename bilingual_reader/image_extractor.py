"""Module for extracting images from PDF and ePub files."""

import os
import io
from typing import List, Tuple, Optional, Union
from dataclasses import dataclass
from PIL import Image
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# PyMuPDF imports (try/except for graceful degradation)
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False


@dataclass
class ImageBlock:
    """Represents an extracted image with metadata."""

    image: Image.Image
    caption: str
    position: float  # Relative position in document (0.0 to 1.0)
    page: Optional[int]  # Page number (for PDFs)
    index: int  # Sequential index in document

    def __init__(
        self,
        image: Image.Image,
        caption: str = "",
        position: float = 0.0,
        page: Optional[int] = None,
        index: int = 0
    ):
        self.image = image
        self.caption = caption
        self.position = position
        self.page = page
        self.index = index


@dataclass
class ContentBlock:
    """Represents a block of content (either text or image)."""

    content_type: str  # "text" or "image"
    content: Union[str, ImageBlock]
    position: float  # Relative position in document (0.0 to 1.0)

    def __init__(self, content_type: str, content: Union[str, ImageBlock], position: float = 0.0):
        self.content_type = content_type
        self.content = content
        self.position = position


def optimize_image(
    image: Image.Image,
    max_width: int = 800,
    max_height: int = 1200,
    quality: int = 85
) -> Image.Image:
    """Optimize image size and quality.

    Args:
        image: PIL Image to optimize
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        quality: JPEG quality (1-100)

    Returns:
        Optimized PIL Image
    """
    # Get original dimensions
    width, height = image.size

    # Calculate scaling factor to fit within max dimensions
    width_ratio = max_width / width if width > max_width else 1.0
    height_ratio = max_height / height if height > max_height else 1.0
    scale_factor = min(width_ratio, height_ratio)

    # Resize if needed
    if scale_factor < 1.0:
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        image = image.resize((new_width, new_height), Image.LANCZOS)

    # Convert to RGB if necessary (for JPEG compatibility)
    if image.mode in ('RGBA', 'LA', 'P'):
        # Create white background
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    return image


def extract_images_from_pdf(file_path: str) -> List[ImageBlock]:
    """Extract images from a PDF file using PyMuPDF.

    Args:
        file_path: Path to the PDF file

    Returns:
        List of ImageBlock objects

    Raises:
        ImportError: If PyMuPDF is not installed
    """
    if not HAS_PYMUPDF:
        raise ImportError(
            "PyMuPDF (fitz) is required for PDF image extraction. "
            "Install it with: pip install PyMuPDF"
        )

    images = []
    doc = fitz.open(file_path)
    total_pages = len(doc)
    image_index = 0

    for page_num in range(total_pages):
        page = doc[page_num]
        image_list = page.get_images()

        for img_index, img_info in enumerate(image_list):
            try:
                # Extract image
                xref = img_info[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # Convert to PIL Image
                pil_image = Image.open(io.BytesIO(image_bytes))

                # Filter out very small images (likely decorative)
                if pil_image.width < 50 or pil_image.height < 50:
                    continue

                # Optimize image
                pil_image = optimize_image(pil_image)

                # Try to extract caption (text directly below image)
                caption = ""
                # Note: Extracting captions from PDF is complex, leaving as empty for now

                # Calculate position (relative to document)
                position = (page_num + 0.5) / total_pages

                images.append(ImageBlock(
                    image=pil_image,
                    caption=caption,
                    position=position,
                    page=page_num + 1,  # 1-indexed
                    index=image_index
                ))

                image_index += 1

            except Exception as e:
                # Skip problematic images
                print(f"Warning: Could not extract image {img_index} from page {page_num + 1}: {e}")
                continue

    doc.close()
    return images


def extract_images_from_epub(file_path: str) -> List[ImageBlock]:
    """Extract images from an ePub file.

    Args:
        file_path: Path to the ePub file

    Returns:
        List of ImageBlock objects
    """
    images = []
    book = epub.read_epub(file_path)
    image_index = 0

    # First, get all image items from the ePub
    epub_images = {}
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_IMAGE:
            # Store images by their href/filename
            epub_images[item.get_name()] = item.get_content()

    # Now parse HTML documents to find where images are used
    documents = [item for item in book.get_items() if item.get_type() == ebooklib.ITEM_DOCUMENT]
    total_docs = len(documents)

    for doc_index, item in enumerate(documents):
        soup = BeautifulSoup(item.get_content(), 'html.parser')

        # Find all img tags
        img_tags = soup.find_all('img')

        for img_tag in img_tags:
            try:
                # Get image source
                img_src = img_tag.get('src', '')
                if not img_src:
                    continue

                # Clean up the path (remove ../ and leading /)
                img_src = img_src.replace('../', '').lstrip('/')

                # Try to find the image in our epub_images dict
                image_bytes = None
                for key, value in epub_images.items():
                    if img_src in key or key.endswith(img_src):
                        image_bytes = value
                        break

                if not image_bytes:
                    continue

                # Convert to PIL Image
                pil_image = Image.open(io.BytesIO(image_bytes))

                # Filter out very small images
                if pil_image.width < 50 or pil_image.height < 50:
                    continue

                # Optimize image
                pil_image = optimize_image(pil_image)

                # Extract caption from alt text or figcaption
                caption = ""

                # Try alt text
                alt_text = img_tag.get('alt', '').strip()
                if alt_text:
                    caption = alt_text

                # Try figcaption (if img is inside a figure)
                figure = img_tag.find_parent('figure')
                if figure:
                    figcaption = figure.find('figcaption')
                    if figcaption:
                        caption = figcaption.get_text().strip()

                # Calculate position (relative to document)
                position = (doc_index + 0.5) / total_docs if total_docs > 0 else 0.5

                images.append(ImageBlock(
                    image=pil_image,
                    caption=caption,
                    position=position,
                    page=None,  # ePub doesn't have page numbers
                    index=image_index
                ))

                image_index += 1

            except Exception as e:
                # Skip problematic images
                print(f"Warning: Could not extract image from ePub: {e}")
                continue

    return images


def extract_images(file_path: str) -> List[ImageBlock]:
    """Extract images from a file based on its extension.

    Args:
        file_path: Path to the file

    Returns:
        List of ImageBlock objects

    Raises:
        ValueError: If file format is not supported
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        return extract_images_from_pdf(file_path)
    elif ext == '.epub':
        return extract_images_from_epub(file_path)
    elif ext == '.txt':
        return []  # Text files don't contain images
    else:
        raise ValueError(f"Unsupported file format for image extraction: {ext}")


def match_images_by_position(
    images1: List[ImageBlock],
    images2: List[ImageBlock]
) -> Tuple[List[Tuple[ImageBlock, ImageBlock]], List[ImageBlock], List[ImageBlock]]:
    """Match images by their index position in the document.

    Args:
        images1: Images from first document
        images2: Images from second document

    Returns:
        Tuple of (matched_pairs, unmatched_from_doc1, unmatched_from_doc2)
    """
    matched = []
    min_count = min(len(images1), len(images2))

    # Match by index
    for i in range(min_count):
        matched.append((images1[i], images2[i]))

    # Unmatched images
    unmatched1 = images1[min_count:] if len(images1) > min_count else []
    unmatched2 = images2[min_count:] if len(images2) > min_count else []

    return matched, unmatched1, unmatched2


def match_images_by_page(
    images1: List[ImageBlock],
    images2: List[ImageBlock]
) -> Tuple[List[Tuple[ImageBlock, ImageBlock]], List[ImageBlock], List[ImageBlock]]:
    """Match images by their relative page position in the document.

    For ePubs without page numbers, falls back to position-based matching.

    Args:
        images1: Images from first document
        images2: Images from second document

    Returns:
        Tuple of (matched_pairs, unmatched_from_doc1, unmatched_from_doc2)
    """
    # If either document doesn't have page numbers, fall back to position matching
    if not images1 or not images2 or images1[0].page is None or images2[0].page is None:
        return match_images_by_position(images1, images2)

    # Use relative position (normalized page number) for matching
    matched = []
    unmatched1 = list(images1)
    unmatched2 = list(images2)

    # Match images with similar relative positions
    for img1 in images1:
        best_match = None
        best_distance = float('inf')

        for img2 in unmatched2:
            distance = abs(img1.position - img2.position)
            if distance < best_distance:
                best_distance = distance
                best_match = img2

        # If the best match is reasonably close (within 10% of document), consider it matched
        if best_match and best_distance < 0.1:
            matched.append((img1, best_match))
            unmatched1.remove(img1)
            unmatched2.remove(best_match)

    return matched, unmatched1, unmatched2


def match_images_by_proximity(
    images1: List[ImageBlock],
    images2: List[ImageBlock],
    aligned_text_positions: List[Tuple[float, float]]
) -> Tuple[List[Tuple[ImageBlock, ImageBlock]], List[ImageBlock], List[ImageBlock]]:
    """Match images based on proximity to aligned text segments.

    Args:
        images1: Images from first document
        images2: Images from second document
        aligned_text_positions: List of (pos1, pos2) tuples for aligned text segments

    Returns:
        Tuple of (matched_pairs, unmatched_from_doc1, unmatched_from_doc2)
    """
    # For now, use position-based matching as a simple implementation
    # A more sophisticated version would analyze which text segments images are near
    return match_images_by_position(images1, images2)
