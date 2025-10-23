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
def main(input1, input2, output, lang1, lang2, mode, title):
    """Generate a bilingual PDF with aligned text from two language sources.
    
    This tool reads books in two different languages (PDF, ePub, or txt format)
    and creates a PDF where the text alternates between the two languages
    at the sentence or paragraph level using Lingtrain Aligner.
    
    Example:
        bilingual-pdf --input1 book_en.pdf --input2 book_zh.pdf --output bilingual.pdf --mode sentence
    """
    click.echo("Bilingual PDF Generator")
    click.echo("=" * 50)
    
    # Extract text from input files
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
