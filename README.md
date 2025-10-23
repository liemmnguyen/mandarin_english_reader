# Mandarin English Reader

A PDF generator that creates bilingual documents using Lingtrain Aligner. This tool reads books in two different languages (PDF, ePub, or txt format) and creates a PDF where the text alternates between the two languages at the sentence or paragraph level.

## Features

- **Multiple Input Formats**: Supports PDF, ePub, and plain text files
- **Flexible Alignment**: Align text at sentence or paragraph level
- **Smart Text Splitting**: Uses Lingtrain Aligner's sentence splitter for accurate text segmentation when available
- **Sequential Alignment**: Pairs text segments from both languages in order for easy reading
- **Clean PDF Output**: Generates professional-looking bilingual documents
- **Language Learning Friendly**: Perfect for parallel reading and language study

## Installation

### From Source

```bash
git clone https://github.com/liemmnguyen/mandarin_english_reader.git
cd mandarin_english_reader
pip install -e .
```

### Using pip

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

### Command Line Interface

```bash
bilingual-pdf --input1 book_english.pdf \
              --input2 book_chinese.pdf \
              --output bilingual_output.pdf \
              --mode sentence \
              --lang1 en \
              --lang2 zh \
              --title "My Bilingual Book"
```

### Parameters

- `--input1`: Path to the first language file (PDF, ePub, or txt) - **Required**
- `--input2`: Path to the second language file (PDF, ePub, or txt) - **Required**
- `--output`: Path for the output PDF file - **Required**
- `--lang1`: Language code for first file (default: `en`)
- `--lang2`: Language code for second file (default: `zh`)
- `--mode`: Alignment mode - `sentence` or `paragraph` (default: `sentence`)
- `--title`: Title for the PDF document (default: `Bilingual Document`)

### Examples

#### Sentence-level alignment (English-Chinese)

```bash
bilingual-pdf --input1 english.txt \
              --input2 chinese.txt \
              --output result.pdf \
              --mode sentence
```

#### Paragraph-level alignment (Spanish-English)

```bash
bilingual-pdf --input1 spanish.epub \
              --input2 english.epub \
              --output result.pdf \
              --mode paragraph \
              --lang1 es \
              --lang2 en
```

## Programmatic Usage

You can also use the library in your Python code:

```python
from bilingual_reader.text_extractor import TextExtractor
from bilingual_reader.aligner import BilingualAligner
from bilingual_reader.pdf_generator import PDFGenerator

# Extract text from files
text1 = TextExtractor.extract_text("book1.pdf")
text2 = TextExtractor.extract_text("book2.pdf")

# Align texts
aligner = BilingualAligner(lang1="en", lang2="zh")
aligned_texts = aligner.align_texts(text1, text2, alignment_mode="sentence")

# Generate PDF
pdf_gen = PDFGenerator("output.pdf", title="My Bilingual Book")
pdf_gen.generate_pdf(aligned_texts)
```

## How It Works

1. **Text Extraction**: The tool extracts text from your input files (PDF, ePub, or txt)
2. **Text Segmentation**: Text is split into sentences or paragraphs based on your chosen mode
3. **Sequential Alignment**: Segments from both languages are paired in order (1st with 1st, 2nd with 2nd, etc.)
4. **PDF Generation**: A new PDF is created with alternating segments from each language

This approach works best when:
- Both input files contain the same content translated into different languages
- The texts are roughly parallel in structure (same number of sentences/paragraphs)
- You want a simple, readable bilingual format for language learning

## Supported Languages

The tool supports any language pair that Lingtrain Aligner supports. Common language codes include:

- `en` - English
- `zh` - Chinese
- `es` - Spanish
- `fr` - French
- `de` - German
- `ja` - Japanese
- `ko` - Korean
- `ru` - Russian
- `ar` - Arabic

## Requirements

- Python 3.8+
- lingtrain-aligner
- PyPDF2
- ebooklib
- reportlab
- beautifulsoup4
- lxml
- click

## License

MIT License

## Troubleshooting

### Installation Issues

If you encounter issues installing dependencies, try:

```bash
# Install core dependencies only (without heavy ML libraries)
pip install PyPDF2 ebooklib reportlab beautifulsoup4 lxml click

# Then install the package
pip install -e .
```

The tool will work with basic sentence splitting even without lingtrain-aligner installed.

### PDF Generation Issues

- **Missing fonts for non-Latin scripts**: The tool uses ReportLab's built-in font support. For best results with Chinese, Japanese, or other non-Latin scripts, ensure your system has appropriate fonts installed.
- **Large files**: For very large books, processing may take several minutes. Be patient!

### Alignment Quality

For best alignment results:
- Ensure both input files contain the same content (translated versions)
- Use paragraph mode for books with clear paragraph structure
- Use sentence mode for more granular alignment

## Testing

Run the test suite:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.