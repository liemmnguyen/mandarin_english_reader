"""Module for generating PDF documents with aligned bilingual text."""

import os
import io
from typing import List, Tuple
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image as RLImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from PIL import Image as PILImage

from .aligner import AlignedDocument, AlignedDocumentWithImages
from .image_extractor import ImageBlock


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

    def _pil_image_to_reportlab(
        self,
        pil_image: PILImage.Image,
        max_width: float = 6 * inch,
        max_height: float = 8 * inch
    ) -> RLImage:
        """Convert PIL Image to ReportLab Image with size constraints.

        Args:
            pil_image: PIL Image to convert
            max_width: Maximum width in reportlab units
            max_height: Maximum height in reportlab units

        Returns:
            ReportLab Image object
        """
        # Save PIL image to bytes buffer
        img_buffer = io.BytesIO()
        pil_image.save(img_buffer, format='JPEG', quality=85)
        img_buffer.seek(0)

        # Create ReportLab image
        rl_image = RLImage(img_buffer)

        # Get original dimensions
        orig_width = pil_image.width
        orig_height = pil_image.height

        # Calculate scaling to fit within max dimensions while maintaining aspect ratio
        width_ratio = max_width / orig_width
        height_ratio = max_height / orig_height
        scale_factor = min(width_ratio, height_ratio, 1.0)  # Don't scale up

        # Set final dimensions
        rl_image.drawWidth = orig_width * scale_factor
        rl_image.drawHeight = orig_height * scale_factor

        return rl_image

    def _create_matched_image_table(
        self,
        img1: ImageBlock,
        img2: ImageBlock
    ) -> Table:
        """Create a side-by-side table for matched images.

        Args:
            img1: First image block
            img2: Second image block

        Returns:
            ReportLab Table with images side-by-side
        """
        # Convert images to ReportLab format (half width each for side-by-side)
        max_img_width = 2.5 * inch
        rl_img1 = self._pil_image_to_reportlab(img1.image, max_width=max_img_width)
        rl_img2 = self._pil_image_to_reportlab(img2.image, max_width=max_img_width)

        # Create table data
        table_data = [[rl_img1, rl_img2]]

        # Add captions if they exist
        if img1.caption or img2.caption:
            caption1 = Paragraph(
                f"<i>{self._sanitize_text(img1.caption)}</i>" if img1.caption else "",
                self.styles['Normal']
            )
            caption2 = Paragraph(
                f"<i>{self._sanitize_text(img2.caption)}</i>" if img2.caption else "",
                self.styles['Normal']
            )
            table_data.append([caption1, caption2])

        # Create table
        table = Table(table_data, colWidths=[3 * inch, 3 * inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        return table

    def _create_single_image_element(
        self,
        img: ImageBlock
    ) -> List:
        """Create full-width image element with optional caption.

        Args:
            img: Image block

        Returns:
            List of ReportLab flowables (image + caption)
        """
        elements = []

        # Convert image to ReportLab format (full width)
        rl_img = self._pil_image_to_reportlab(img.image, max_width=6 * inch)
        elements.append(rl_img)

        # Add caption if exists
        if img.caption:
            caption = Paragraph(
                f"<i>{self._sanitize_text(img.caption)}</i>",
                self.styles['Normal']
            )
            elements.append(caption)
            elements.append(Spacer(1, 0.1 * inch))

        return elements

    def generate_pdf_from_aligned_document_with_images(
        self,
        aligned_doc: AlignedDocumentWithImages,
        lang1_name: str = "Language 1",
        lang2_name: str = "Language 2",
        image_match_mode: str = "inline"
    ):
        """Generate PDF from AlignedDocumentWithImages.

        Args:
            aligned_doc: AlignedDocumentWithImages with text and images
            lang1_name: Name of first language
            lang2_name: Name of second language
            image_match_mode: How images were matched ("inline", "position", "page", "proximity")
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
                    for para in text2.split('\n\n'):
                        if para.strip():
                            story.append(Paragraph(
                                self._sanitize_text(para),
                                self.styles['FrontMatter']
                            ))

            story.append(PageBreak())

        # Add main text section with images
        if aligned_doc.main_text:
            story.append(Paragraph("Main Text", self.styles['SectionHeader']))
            story.append(Spacer(1, 0.1 * inch))

            # Track which images have been displayed
            displayed_matched = set()
            displayed_unmatched1 = set()
            displayed_unmatched2 = set()

            # For inline mode, interleave images with text based on position
            if image_match_mode == "inline":
                # Combine all images into a single list with language indicator
                all_images = []
                for img in aligned_doc.unmatched_images1:
                    all_images.append((img, 1))  # lang1
                for img in aligned_doc.unmatched_images2:
                    all_images.append((img, 2))  # lang2

                # Sort by position
                all_images.sort(key=lambda x: x[0].position)

                img_index = 0
                for idx, (text1, text2) in enumerate(aligned_doc.main_text):
                    # Display images that appear before this text segment
                    while img_index < len(all_images):
                        img, lang = all_images[img_index]
                        # Rough heuristic: image position corresponds to text segment
                        segment_position = (idx + 0.5) / len(aligned_doc.main_text)
                        if img.position <= segment_position:
                            # Display image for its language
                            if lang == 1:
                                for elem in self._create_single_image_element(img):
                                    story.append(elem)
                                story.append(Spacer(1, 0.15 * inch))
                            img_index += 1
                        else:
                            break

                    # Display text
                    if text1.strip():
                        para1 = Paragraph(
                            self._sanitize_text(text1),
                            self.styles['Language1']
                        )
                        story.append(para1)

                    if text2.strip():
                        # Display images for lang2 before the text if applicable
                        para2 = Paragraph(
                            self._sanitize_text(text2),
                            self.styles['Language2']
                        )
                        story.append(para2)

                    if idx < len(aligned_doc.main_text) - 1:
                        story.append(Spacer(1, 0.1 * inch))

                # Display any remaining images
                while img_index < len(all_images):
                    img, lang = all_images[img_index]
                    for elem in self._create_single_image_element(img):
                        story.append(elem)
                    story.append(Spacer(1, 0.15 * inch))
                    img_index += 1

            else:
                # For matched modes, display matched images side-by-side
                # and unmatched images inline

                # Display matched images first (or intersperse with text)
                for matched_img1, matched_img2 in aligned_doc.matched_images:
                    table = self._create_matched_image_table(matched_img1, matched_img2)
                    story.append(table)
                    story.append(Spacer(1, 0.2 * inch))

                # Display text
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

                    if idx < len(aligned_doc.main_text) - 1:
                        story.append(Spacer(1, 0.1 * inch))

                # Display unmatched images at the end
                for img in aligned_doc.unmatched_images1:
                    story.append(Spacer(1, 0.15 * inch))
                    for elem in self._create_single_image_element(img):
                        story.append(elem)

                for img in aligned_doc.unmatched_images2:
                    story.append(Spacer(1, 0.15 * inch))
                    for elem in self._create_single_image_element(img):
                        story.append(elem)

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
                    for para in text2.split('\n\n'):
                        if para.strip():
                            story.append(Paragraph(
                                self._sanitize_text(para),
                                self.styles['BackMatter']
                            ))

        # Build the PDF
        self.doc.build(story)
