"""Module for generating PDF documents with aligned bilingual text."""

import os
from typing import List, Tuple
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY


class PDFGenerator:
    """Generate PDF documents with aligned bilingual text."""

    def __init__(
        self,
        output_path: str,
        page_size=letter,
        title: str = "Bilingual Document"
    ):
        """Initialize the PDF generator.
        
        Args:
            output_path: Path where the PDF will be saved
            page_size: Page size (default: letter)
            title: Document title
        """
        self.output_path = output_path
        self.page_size = page_size
        self.title = title
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=page_size,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        self.styles = self._setup_styles()

    def _setup_styles(self):
        """Setup paragraph styles for the document."""
        styles = getSampleStyleSheet()
        
        # Style for language 1 (e.g., English)
        styles.add(ParagraphStyle(
            name='Language1',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            spaceBefore=6,
            spaceAfter=6,
            alignment=TA_LEFT,
        ))
        
        # Style for language 2 (e.g., Chinese)
        styles.add(ParagraphStyle(
            name='Language2',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            spaceBefore=6,
            spaceAfter=12,
            alignment=TA_LEFT,
        ))
        
        # Title style
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            leading=22,
            spaceBefore=12,
            spaceAfter=24,
            alignment=TA_LEFT,
        ))
        
        return styles

    def generate_pdf(
        self,
        aligned_texts: List[Tuple[str, str]],
        lang1_name: str = "Language 1",
        lang2_name: str = "Language 2"
    ):
        """Generate the PDF with aligned bilingual text.
        
        Args:
            aligned_texts: List of tuples containing aligned text segments
            lang1_name: Name of first language for display
            lang2_name: Name of second language for display
        """
        story = []
        
        # Add title
        title = Paragraph(self.title, self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.2 * inch))
        
        # Add aligned text segments
        for idx, (text1, text2) in enumerate(aligned_texts):
            if text1.strip():
                # Add language 1 text
                para1 = Paragraph(
                    self._sanitize_text(text1),
                    self.styles['Language1']
                )
                story.append(para1)
            
            if text2.strip():
                # Add language 2 text
                para2 = Paragraph(
                    self._sanitize_text(text2),
                    self.styles['Language2']
                )
                story.append(para2)
            
            # Add extra spacing between alignment pairs
            if idx < len(aligned_texts) - 1:
                story.append(Spacer(1, 0.1 * inch))
        
        # Build the PDF
        self.doc.build(story)

    def _sanitize_text(self, text: str) -> str:
        """Sanitize text for PDF generation.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text safe for PDF generation
        """
        # Replace problematic characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        # Remove control characters except newlines and tabs
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
        
        return text.strip()
