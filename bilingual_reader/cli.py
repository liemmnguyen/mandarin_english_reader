"""Command-line interface for the bilingual PDF generator."""

import click
import os
from .text_extractor import TextExtractor
from .aligner import BilingualAligner
from .pdf_generator import PDFGenerator


@click.command()
@click.option(
    '--input1',
    required=True,
    type=click.Path(exists=True),
    help='Path to the first language file (PDF, ePub, or txt)'
)
@click.option(
    '--input2',
    required=True,
    type=click.Path(exists=True),
    help='Path to the second language file (PDF, ePub, or txt)'
)
@click.option(
    '--output',
    required=True,
    type=click.Path(),
    help='Path for the output PDF file'
)
@click.option(
    '--lang1',
    default='en',
    help='Language code for first file (default: en)'
)
@click.option(
    '--lang2',
    default='zh',
    help='Language code for second file (default: zh)'
)
@click.option(
    '--mode',
    type=click.Choice(['sentence', 'paragraph'], case_sensitive=False),
    default='sentence',
    help='Alignment mode: sentence or paragraph (default: sentence)'
)
@click.option(
    '--title',
    default='Bilingual Document',
    help='Title for the PDF document'
)
@click.option(
    '--detect-structure/--no-detect-structure',
    default=True,
    help='Automatically detect front/back matter and main text (default: enabled)'
)
@click.option(
    '--start-marker1',
    default=None,
    help='Custom marker for where main text starts in first file (e.g., "Chapter 1")'
)
@click.option(
    '--start-marker2',
    default=None,
    help='Custom marker for where main text starts in second file (e.g., "第一章")'
)
@click.option(
    '--end-marker1',
    default=None,
    help='Custom marker for where back matter starts in first file (e.g., "Appendix")'
)
@click.option(
    '--end-marker2',
    default=None,
    help='Custom marker for where back matter starts in second file (e.g., "附录")'
)
def main(input1, input2, output, lang1, lang2, mode, title, detect_structure,
         start_marker1, start_marker2, end_marker1, end_marker2):
    """Generate a bilingual PDF with aligned text from two language sources.

    This tool reads books in two different languages (PDF, ePub, or txt format)
    and creates a PDF where the text alternates between the two languages
    at the sentence or paragraph level using Lingtrain Aligner.

    With structure detection enabled (default), the tool automatically identifies
    front matter (preface, TOC), main text, and back matter (appendix, notes),
    and handles them appropriately.

    Example:
        bilingual-pdf --input1 book_en.pdf --input2 book_zh.pdf --output bilingual.pdf --mode sentence

    Example with custom markers:
        bilingual-pdf --input1 book_en.pdf --input2 book_zh.pdf --output out.pdf \\
            --start-marker1 "Chapter 1" --start-marker2 "第一章"
    """
    click.echo("Bilingual PDF Generator")
    click.echo("=" * 50)

    if detect_structure:
        # Extract text with structure detection
        click.echo(f"\n1. Extracting text with structure detection from {input1}...")
        try:
            doc1 = TextExtractor.extract_with_structure(
                input1,
                start_marker=start_marker1,
                end_marker=end_marker1
            )
            click.echo(f"   ✓ Front matter: {len(doc1.front_matter)} chars")
            click.echo(f"   ✓ Main text: {len(doc1.main_text)} chars")
            click.echo(f"   ✓ Back matter: {len(doc1.back_matter)} chars")
        except Exception as e:
            click.echo(f"   ✗ Error extracting text from {input1}: {e}", err=True)
            return

        click.echo(f"\n2. Extracting text with structure detection from {input2}...")
        try:
            doc2 = TextExtractor.extract_with_structure(
                input2,
                start_marker=start_marker2,
                end_marker=end_marker2
            )
            click.echo(f"   ✓ Front matter: {len(doc2.front_matter)} chars")
            click.echo(f"   ✓ Main text: {len(doc2.main_text)} chars")
            click.echo(f"   ✓ Back matter: {len(doc2.back_matter)} chars")
        except Exception as e:
            click.echo(f"   ✗ Error extracting text from {input2}: {e}", err=True)
            return

        # Align documents
        click.echo(f"\n3. Aligning documents using {mode} mode...")
        try:
            aligner = BilingualAligner(lang1=lang1, lang2=lang2)
            aligned_doc = aligner.align_documents(doc1, doc2, alignment_mode=mode)
            click.echo(f"   ✓ Front matter: {len(aligned_doc.front_matter)} sections")
            click.echo(f"   ✓ Main text: {len(aligned_doc.main_text)} aligned segments")
            click.echo(f"   ✓ Back matter: {len(aligned_doc.back_matter)} sections")
        except Exception as e:
            click.echo(f"   ✗ Error aligning documents: {e}", err=True)
            return

        # Generate PDF
        click.echo(f"\n4. Generating PDF at {output}...")
        try:
            pdf_gen = PDFGenerator(output, title=title)
            pdf_gen.generate_pdf_from_aligned_document(
                aligned_doc,
                lang1_name=f"Language 1 ({lang1})",
                lang2_name=f"Language 2 ({lang2})"
            )
            click.echo(f"   ✓ PDF generated successfully!")
        except Exception as e:
            click.echo(f"   ✗ Error generating PDF: {e}", err=True)
            return

    else:
        # Legacy mode: extract text without structure detection
        click.echo(f"\n1. Extracting text from {input1}...")
        try:
            text1 = TextExtractor.extract_text(input1)
            click.echo(f"   ✓ Extracted {len(text1)} characters from first file")
        except Exception as e:
            click.echo(f"   ✗ Error extracting text from {input1}: {e}", err=True)
            return

        click.echo(f"\n2. Extracting text from {input2}...")
        try:
            text2 = TextExtractor.extract_text(input2)
            click.echo(f"   ✓ Extracted {len(text2)} characters from second file")
        except Exception as e:
            click.echo(f"   ✗ Error extracting text from {input2}: {e}", err=True)
            return

        # Align texts
        click.echo(f"\n3. Aligning texts using {mode} mode...")
        try:
            aligner = BilingualAligner(lang1=lang1, lang2=lang2)
            aligned_texts = aligner.align_texts(text1, text2, alignment_mode=mode)
            click.echo(f"   ✓ Created {len(aligned_texts)} aligned segments")
        except Exception as e:
            click.echo(f"   ✗ Error aligning texts: {e}", err=True)
            return

        # Generate PDF
        click.echo(f"\n4. Generating PDF at {output}...")
        try:
            pdf_gen = PDFGenerator(output, title=title)
            pdf_gen.generate_pdf(
                aligned_texts,
                lang1_name=f"Language 1 ({lang1})",
                lang2_name=f"Language 2 ({lang2})"
            )
            click.echo(f"   ✓ PDF generated successfully!")
        except Exception as e:
            click.echo(f"   ✗ Error generating PDF: {e}", err=True)
            return

    click.echo(f"\n{'=' * 50}")
    click.echo(f"✓ Complete! Output saved to: {output}")


if __name__ == '__main__':
    main()
