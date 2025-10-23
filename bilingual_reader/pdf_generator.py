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

from .aligner import AlignedDocument


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

        # Front matter style (slightly smaller, italic)
        styles.add(ParagraphStyle(
            name='FrontMatter',
            parent=styles['Normal'],
            fontSize=10,
            leading=13,
            spaceBefore=3,
            spaceAfter=3,
            alignment=TA_LEFT,
            textColor='#333333',
        ))

        # Back matter style (slightly smaller)
        styles.add(ParagraphStyle(
            name='BackMatter',
            parent=styles['Normal'],
            fontSize=10,
            leading=13,
            spaceBefore=3,
            spaceAfter=3,
            alignment=TA_LEFT,
            textColor='#555555',
        ))

        # Section header style
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            spaceBefore=18,
            spaceAfter=12,
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

    def generate_pdf_from_aligned_document(
        self,
        aligned_doc: AlignedDocument,
        lang1_name: str = "Language 1",
        lang2_name: str = "Language 2"
    ):
        """Generate PDF from an AlignedDocument with front/main/back matter.

        Front and back matter are displayed side-by-side (concatenated).
        Main text is displayed with sentence/paragraph alignment.

        Args:
            aligned_doc: AlignedDocument with front_matter, main_text, back_matter
            lang1_name: Name of first language for display
            lang2_name: Name of second language for display
        """
        story = []

        # Add title
        title = Paragraph(self.title, self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.2 * inch))

        # Add front matter section (if present)
        if aligned_doc.front_matter:
            story.append(Paragraph("Front Matter", self.styles['SectionHeader']))
            story.append(Spacer(1, 0.1 * inch))

            for text1, text2 in aligned_doc.front_matter:
                if text1.strip():
                    story.append(Paragraph(
                        f"<b>{lang1_name}:</b>",
                        self.styles['FrontMatter']
                    ))
                    # Split long front matter into paragraphs for better display
                    for para in text1.split('\n\n'):
                        if para.strip():
                            story.append(Paragraph(
                                self._sanitize_text(para),
                                self.styles['FrontMatter']
                            ))

                story.append(Spacer(1, 0.15 * inch))

                if text2.strip():
                    story.append(Paragraph(
                        f"<b>{lang2_name}:</b>",
                        self.styles['FrontMatter']
                    ))
                    # Split long front matter into paragraphs for better display
                    for para in text2.split('\n\n'):
                        if para.strip():
                            story.append(Paragraph(
                                self._sanitize_text(para),
                                self.styles['FrontMatter']
                            ))

            # Page break after front matter
            story.append(PageBreak())

        # Add main text section (aligned)
        if aligned_doc.main_text:
            story.append(Paragraph("Main Text", self.styles['SectionHeader']))
            story.append(Spacer(1, 0.1 * inch))

            for idx, (text1, text2) in enumerate(aligned_doc.main_text):
                if text1.strip():
                    para1 = Paragraph(
                        self._sanitize_text(text1),
                        self.styles['Language1']
                    )
                    story.append(para1)

                if text2.strip():
                    para2 = Paragraph(
                        self._sanitize_text(text2),
                        self.styles['Language2']
                    )
                    story.append(para2)

                # Add spacing between alignment pairs
                if idx < len(aligned_doc.main_text) - 1:
                    story.append(Spacer(1, 0.1 * inch))

        # Add back matter section (if present)
        if aligned_doc.back_matter:
            story.append(PageBreak())
            story.append(Paragraph("Back Matter", self.styles['SectionHeader']))
            story.append(Spacer(1, 0.1 * inch))

            for text1, text2 in aligned_doc.back_matter:
                if text1.strip():
                    story.append(Paragraph(
                        f"<b>{lang1_name}:</b>",
                        self.styles['BackMatter']
                    ))
                    # Split long back matter into paragraphs for better display
                    for para in text1.split('\n\n'):
                        if para.strip():
                            story.append(Paragraph(
                                self._sanitize_text(para),
                                self.styles['BackMatter']
                            ))

                story.append(Spacer(1, 0.15 * inch))

                if text2.strip():
                    story.append(Paragraph(
                        f"<b>{lang2_name}:</b>",
                        self.styles['BackMatter']
                    ))
                    # Split long back matter into paragraphs for better display
                    for para in text2.split('\n\n'):
                        if para.strip():
                            story.append(Paragraph(
                                self._sanitize_text(para),
                                self.styles['BackMatter']
                            ))

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
