"""Module for extracting text from various file formats (PDF, ePub, txt)."""

import os
from typing import List, Optional
from dataclasses import dataclass
import PyPDF2
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

from .document_structure import DocumentSection, split_document
from .image_extractor import ImageBlock, extract_images


@dataclass
class DocumentWithImages:
    """Document section with associated images."""

    front_matter: str
    main_text: str
    back_matter: str
    images: List[ImageBlock]

    def __init__(
        self,
        front_matter: str = "",
        main_text: str = "",
        back_matter: str = "",
        images: Optional[List[ImageBlock]] = None
    ):
        self.front_matter = front_matter
        self.main_text = main_text
        self.back_matter = back_matter
        self.images = images if images is not None else []


class TextExtractor:
    """Extract text from various file formats."""

    @staticmethod
    def extract_from_pdf(file_path: str) -> str:
        """Extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        text = []
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return '\n'.join(text)

    @staticmethod
    def extract_from_epub(file_path: str) -> str:
        """Extract text from an ePub file.
        
        Args:
            file_path: Path to the ePub file
            
        Returns:
            Extracted text as a string
        """
        book = epub.read_epub(file_path)
        text = []
        
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                chapter_text = soup.get_text()
                if chapter_text.strip():
                    text.append(chapter_text)
        
        return '\n'.join(text)

    @staticmethod
    def extract_from_txt(file_path: str) -> str:
        """Extract text from a text file.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Extracted text as a string
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text from a file based on its extension.

        Args:
            file_path: Path to the file

        Returns:
            Extracted text as a string

        Raises:
            ValueError: If file format is not supported
        """
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.pdf':
            return TextExtractor.extract_from_pdf(file_path)
        elif ext == '.epub':
            return TextExtractor.extract_from_epub(file_path)
        elif ext == '.txt':
            return TextExtractor.extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def extract_with_structure(
        file_path: str,
        start_marker: Optional[str] = None,
        end_marker: Optional[str] = None,
        start_position: Optional[int] = None,
        end_position: Optional[int] = None
    ) -> DocumentSection:
        """Extract text with structure detection (front matter, main text, back matter).

        This method first extracts all text, then uses chapter marker detection
        or manual specification to split the document into sections.

        Args:
            file_path: Path to the file
            start_marker: Custom text marker for where main text starts (e.g., "Chapter 1")
            end_marker: Custom text marker for where back matter starts (e.g., "Appendix")
            start_position: Manual character position for main text start (takes precedence)
            end_position: Manual character position for back matter start (takes precedence)

        Returns:
            DocumentSection with front_matter, main_text, and back_matter

        Raises:
            ValueError: If file format is not supported
        """
        # First, extract all text using existing method
        full_text = TextExtractor.extract_text(file_path)

        # Split into structured sections
        return split_document(
            text=full_text,
            start_marker=start_marker,
            end_marker=end_marker,
            start_position=start_position,
            end_position=end_position
        )

    @staticmethod
    def extract_with_structure_and_images(
        file_path: str,
        extract_images_flag: bool = True,
        start_marker: Optional[str] = None,
        end_marker: Optional[str] = None,
        start_position: Optional[int] = None,
        end_position: Optional[int] = None
    ) -> DocumentWithImages:
        """Extract text and images with structure detection.

        Args:
            file_path: Path to the file
            extract_images_flag: Whether to extract images
            start_marker: Custom text marker for where main text starts
            end_marker: Custom text marker for where back matter starts
            start_position: Manual character position for main text start
            end_position: Manual character position for back matter start

        Returns:
            DocumentWithImages with front_matter, main_text, back_matter, and images

        Raises:
            ValueError: If file format is not supported
        """
        # Extract text with structure
        doc_section = TextExtractor.extract_with_structure(
            file_path=file_path,
            start_marker=start_marker,
            end_marker=end_marker,
            start_position=start_position,
            end_position=end_position
        )

        # Extract images if requested
        images = []
        if extract_images_flag:
            try:
                images = extract_images(file_path)
            except Exception as e:
                print(f"Warning: Could not extract images from {file_path}: {e}")
                images = []

        return DocumentWithImages(
            front_matter=doc_section.front_matter,
            main_text=doc_section.main_text,
            back_matter=doc_section.back_matter,
            images=images
        )
