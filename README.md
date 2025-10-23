# Mandarin English Reader

A powerful PDF generator that creates professional bilingual documents with intelligent structure detection and image support. This tool reads books in two different languages (PDF, ePub, or txt format) and creates a beautifully formatted PDF where text alternates between languages at the sentence or paragraph level.

## ✨ Features

### Core Features
- **Multiple Input Formats**: Supports PDF, ePub, and plain text files
- **Flexible Alignment**: Align text at sentence or paragraph level using Lingtrain Aligner
- **Structure-Aware Processing**: Automatically detects and handles front matter, main text, and back matter separately
- **Image Support**: Extracts and renders images from PDF and ePub files with multiple matching modes
- **Smart Chapter Detection**: Automatically identifies chapter markers in English and Chinese (with support for other patterns)
- **Professional PDF Output**: Generates clean, well-formatted bilingual documents
- **Language Learning Friendly**: Perfect for parallel reading and language study

### Advanced Features
- **Automatic Boundary Detection**: Intelligently identifies where main content starts and ends
- **Manual Override Options**: Custom markers for precise control over document structure
- **Image Matching Algorithms**: Position-based, page-based, or proximity-based image alignment
- **Image Optimization**: Automatic resizing and compression for optimal PDF size
- **Caption Preservation**: Extracts and displays image captions from source documents
- **Backward Compatible**: All new features are optional; works with simple text-only mode

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Quick Install

```bash
git clone https://github.com/liemmnguyen/mandarin_english_reader.git
cd mandarin_english_reader
pip install -r requirements.txt
pip install -e .
```

### Installation Notes

**For ePub users (recommended):** The tool works best with ePub files for image extraction and caption support.

**For PDF users:** PyMuPDF (fitz) is required for image extraction from PDFs. This is included in requirements.txt.

**Optional dependencies:** If you only need basic paragraph-level alignment without sentence splitting, you can skip installing lingtrain-aligner and its heavy ML dependencies. The tool will still work with paragraph mode.

## Usage

### Quick Start

Generate a bilingual PDF with default settings (structure detection and image extraction enabled):

```bash
bilingual-pdf --input1 book_english.epub \
              --input2 book_chinese.epub \
              --output bilingual_output.pdf
```

### Complete Example

```bash
bilingual-pdf --input1 book_english.epub \
              --input2 book_chinese.epub \
              --output bilingual_output.pdf \
              --mode sentence \
              --lang1 en \
              --lang2 zh \
              --title "The Little Prince | 小王子" \
              --extract-images \
              --image-match-mode inline
```

### All Parameters

#### Required Parameters
- `--input1`: Path to the first language file (PDF, ePub, or txt)
- `--input2`: Path to the second language file (PDF, ePub, or txt)
- `--output`: Path for the output PDF file

#### Basic Parameters
- `--lang1`: Language code for first file (default: `en`)
- `--lang2`: Language code for second file (default: `zh`)
- `--mode`: Alignment mode - `sentence` or `paragraph` (default: `sentence`)
- `--title`: Title for the PDF document (default: `Bilingual Document`)

#### Structure Detection Parameters
- `--detect-structure` / `--no-detect-structure`: Enable/disable automatic structure detection (default: `enabled`)
- `--start-marker1`: Custom marker for where main text starts in first file (e.g., `"Chapter 1"`)
- `--start-marker2`: Custom marker for where main text starts in second file (e.g., `"第一章"`)
- `--end-marker1`: Custom marker for where back matter starts in first file (e.g., `"Appendix"`)
- `--end-marker2`: Custom marker for where back matter starts in second file (e.g., `"附录"`)

#### Image Parameters
- `--extract-images` / `--no-extract-images`: Enable/disable image extraction (default: `enabled`)
- `--image-match-mode`: Image matching algorithm - `inline`, `position`, `page`, or `proximity` (default: `inline`)
  - `inline`: Images appear with their text, no matching
  - `position`: Match by index (1st with 1st, 2nd with 2nd, etc.)
  - `page`: Match by relative page/document position
  - `proximity`: Match based on nearby aligned text

### Examples

#### Example 1: Basic Usage (Text Only)

Simple sentence-level alignment without images:

```bash
bilingual-pdf --input1 english.txt \
              --input2 chinese.txt \
              --output result.pdf \
              --no-extract-images
```

#### Example 2: ePub with Images (Default)

Process ePub files with automatic structure detection and images:

```bash
bilingual-pdf --input1 book_en.epub \
              --input2 book_zh.epub \
              --output bilingual.pdf \
              --title "My Bilingual Book"
```

#### Example 3: Custom Chapter Markers

When automatic detection doesn't work, specify custom markers:

```bash
bilingual-pdf --input1 english.pdf \
              --input2 chinese.pdf \
              --output result.pdf \
              --start-marker1 "PROLOGUE" \
              --start-marker2 "序章" \
              --end-marker1 "AFTERWORD" \
              --end-marker2 "后记"
```

#### Example 4: Position-Based Image Matching

Match images by their order in the document:

```bash
bilingual-pdf --input1 book_en.epub \
              --input2 book_zh.epub \
              --output result.pdf \
              --image-match-mode position
```

#### Example 5: Paragraph Mode for Different Languages

Spanish-English alignment with paragraph mode:

```bash
bilingual-pdf --input1 spanish.epub \
              --input2 english.epub \
              --output result.pdf \
              --mode paragraph \
              --lang1 es \
              --lang2 en
```

#### Example 6: Disable Structure Detection

For simple documents without chapters:

```bash
bilingual-pdf --input1 story_en.txt \
              --input2 story_zh.txt \
              --output result.pdf \
              --no-detect-structure
```

## Programmatic Usage

You can use the library in your Python code for more control:

### Basic Usage (Text Only)

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

### Advanced Usage (With Structure Detection)

```python
from bilingual_reader.text_extractor import TextExtractor
from bilingual_reader.aligner import BilingualAligner
from bilingual_reader.pdf_generator import PDFGenerator

# Extract with structure detection
doc1 = TextExtractor.extract_with_structure(
    "book1.epub",
    start_marker="Chapter 1"
)
doc2 = TextExtractor.extract_with_structure(
    "book2.epub",
    start_marker="第一章"
)

# Align documents
aligner = BilingualAligner(lang1="en", lang2="zh")
aligned_doc = aligner.align_documents(doc1, doc2, alignment_mode="sentence")

# Generate PDF with structure
pdf_gen = PDFGenerator("output.pdf", title="My Bilingual Book")
pdf_gen.generate_pdf_from_aligned_document(
    aligned_doc,
    lang1_name="English",
    lang2_name="中文"
)
```

### Complete Usage (With Images)

```python
from bilingual_reader.text_extractor import TextExtractor
from bilingual_reader.aligner import BilingualAligner
from bilingual_reader.pdf_generator import PDFGenerator

# Extract text and images with structure detection
doc1 = TextExtractor.extract_with_structure_and_images(
    "book1.epub",
    extract_images_flag=True,
    start_marker="Chapter 1"
)
doc2 = TextExtractor.extract_with_structure_and_images(
    "book2.epub",
    extract_images_flag=True,
    start_marker="第一章"
)

print(f"Extracted {len(doc1.images)} images from book 1")
print(f"Extracted {len(doc2.images)} images from book 2")

# Align documents with images
aligner = BilingualAligner(lang1="en", lang2="zh")
aligned_doc = aligner.align_documents_with_images(
    doc1, doc2,
    alignment_mode="sentence",
    image_match_mode="position"  # or "inline", "page", "proximity"
)

# Generate PDF with images
pdf_gen = PDFGenerator("output.pdf", title="My Bilingual Book")
pdf_gen.generate_pdf_from_aligned_document_with_images(
    aligned_doc,
    lang1_name="English",
    lang2_name="中文",
    image_match_mode="position"
)
```

## How It Works

### Processing Pipeline

1. **Document Parsing**: Extracts text and images from your input files (PDF, ePub, or txt)

2. **Structure Detection** (if enabled):
   - Automatically identifies chapter markers (e.g., "Chapter 1", "第一章")
   - Detects front matter (preface, TOC, copyright)
   - Detects back matter (appendix, notes, index)
   - Splits document into three sections

3. **Image Processing** (if enabled):
   - Extracts images from PDF (using PyMuPDF) or ePub files
   - Filters out tiny decorative images (< 50x50px)
   - Optimizes images (resize to max 800px width, compress)
   - Extracts captions from ePub HTML or PDF metadata

4. **Text Segmentation**:
   - Splits text into sentences (using Lingtrain Aligner) or paragraphs
   - Main text is aligned; front/back matter kept separate

5. **Image Matching** (based on selected mode):
   - **Inline**: No matching, images flow with their text
   - **Position**: Match 1st↔1st, 2nd↔2nd, etc.
   - **Page**: Match by relative document position
   - **Proximity**: Match by nearby aligned text

6. **PDF Generation**:
   - Front matter displayed side-by-side (not sentence-aligned)
   - Main text alternates between languages with images
   - Back matter displayed side-by-side
   - Matched images shown side-by-side; unmatched full-width

### Example Output Format

#### Front Matter Section
```
════════════════════════════════════════
           Front Matter
════════════════════════════════════════
Language 1 (en):
Title: The Little Prince
By: Antoine de Saint-Exupéry
Translator's Note: ...

Language 2 (zh):
标题：小王子
作者：安托万·德·圣埃克苏佩里
译者的话：...
```

#### Main Text Section (Sentence Mode)
```
════════════════════════════════════════
            Main Text
════════════════════════════════════════
Once upon a time, there was a little prince who lived on a small planet.
从前，有一个小王子住在一个小星球上。

The planet was so small that he could walk around it in just a few minutes.
这个星球非常小，他只需要几分钟就可以绕着它走一圈。

[Image: The Little Prince on his planet]

One day, he decided to leave his planet and explore the universe.
有一天，他决定离开他的星球去探索宇宙。
...
```

#### Back Matter Section
```
════════════════════════════════════════
           Back Matter
════════════════════════════════════════
Language 1 (en):
Appendix A: About the Author
...

Language 2 (zh):
附录A：关于作者
...
```

### When This Works Best

This tool is ideal for:
- **Language learners** reading parallel texts
- **Translators** reviewing translations side-by-side
- **Teachers** creating bilingual teaching materials
- **Students** studying foreign literature
- **Publishers** creating bilingual editions

Works best when:
- Both files contain the same content in different languages
- Texts are roughly parallel in structure
- Documents have clear chapter markers (or you can specify custom markers)
- ePub format is used for best image and caption support

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

### Core Dependencies
- Python 3.8 or higher
- PyPDF2 (PDF text extraction)
- PyMuPDF/fitz (PDF image extraction)
- ebooklib (ePub processing)
- reportlab (PDF generation)
- beautifulsoup4 (HTML parsing)
- lxml (XML processing)
- click (CLI interface)
- Pillow/PIL (Image processing)

### Optional Dependencies
- lingtrain-aligner (for sentence-level alignment)
  - Required for `--mode sentence`
  - Not needed for `--mode paragraph`
  - Includes heavy ML dependencies (PyTorch, transformers, etc.)

All dependencies are listed in `requirements.txt` and can be installed with:
```bash
pip install -r requirements.txt
```

## License

MIT License

## Troubleshooting

### Installation Issues

#### Heavy Dependencies
If you encounter issues with PyTorch or other ML dependencies:

```bash
# Install core dependencies only (paragraph mode will work)
pip install PyPDF2 PyMuPDF ebooklib reportlab beautifulsoup4 lxml click Pillow

# Then install the package
pip install -e .
```

You can use `--mode paragraph` without lingtrain-aligner.

#### PyMuPDF Installation
If PyMuPDF fails to install:
```bash
# Try installing from conda
conda install -c conda-forge pymupdf

# Or use pre-built wheels
pip install --upgrade pymupdf
```

### Structure Detection Issues

#### Chapter Not Detected
If automatic chapter detection fails:

**Problem**: Your book uses non-standard chapter markers
**Solution**: Use custom markers:
```bash
bilingual-pdf --input1 book1.epub --input2 book2.epub \
              --start-marker1 "Introduction" \
              --start-marker2 "引言" \
              --output result.pdf
```

#### Too Much/Little in Front Matter
**Problem**: Structure detection is too aggressive or not aggressive enough
**Solution**: Disable structure detection or use manual markers:
```bash
# Disable completely
bilingual-pdf --input1 book1.epub --input2 book2.epub \
              --no-detect-structure --output result.pdf

# Or specify exact boundaries
bilingual-pdf --input1 book1.epub --input2 book2.epub \
              --start-marker1 "Chapter One" \
              --output result.pdf
```

### Image Extraction Issues

#### No Images Extracted
**Possible causes**:
1. Images are too small (< 50x50px) and filtered out
2. PyMuPDF not installed for PDF files
3. Images are embedded in unusual formats

**Solutions**:
```bash
# Check if extraction is enabled
bilingual-pdf ... --extract-images

# Try with ePub format (better image support)
# Convert PDF to ePub using Calibre or similar tool
```

#### Images Not Matching Correctly
**Problem**: Images paired incorrectly between documents
**Solution**: Try different matching modes:
```bash
# Try position-based matching
bilingual-pdf ... --image-match-mode position

# Or use inline mode (no matching)
bilingual-pdf ... --image-match-mode inline
```

#### Out of Memory with Images
**Problem**: Too many or too large images
**Solution**: Images are auto-optimized, but you can disable extraction:
```bash
bilingual-pdf ... --no-extract-images
```

### PDF Generation Issues

#### Missing Fonts for Non-Latin Scripts
**Problem**: Chinese, Japanese, Arabic, etc. characters not displaying correctly
**Solution**: ReportLab uses built-in Unicode support. If issues persist:
- Ensure your system has Unicode fonts installed
- Consider using ePub input (better Unicode handling)
- Update reportlab: `pip install --upgrade reportlab`

#### Large Output Files
**Problem**: Generated PDF is too large
**Solutions**:
- Disable image extraction: `--no-extract-images`
- Images are already optimized (max 800px width, 85% JPEG quality)
- Use text-only mode for extremely large books

#### Slow Processing
**Problem**: Processing takes a long time
**Causes**:
- Sentence-level alignment with lingtrain (uses ML models)
- Large files with many images
- Complex PDF structure

**Solutions**:
```bash
# Use paragraph mode (faster)
bilingual-pdf ... --mode paragraph

# Disable images
bilingual-pdf ... --no-extract-images

# Disable structure detection
bilingual-pdf ... --no-detect-structure
```

### Alignment Quality Issues

#### Misaligned Text
**Problem**: Sentences don't match up correctly
**Common causes**:
1. Books have different front/back matter
2. One translation added/removed content
3. Different paragraph structures

**Solutions**:
```bash
# Use structure detection to handle front/back matter
bilingual-pdf ... --detect-structure

# Try paragraph mode instead of sentence mode
bilingual-pdf ... --mode paragraph

# Specify custom chapter markers
bilingual-pdf ... --start-marker1 "Chapter 1" --start-marker2 "第一章"
```

#### Empty Sections
**Problem**: PDF has blank front matter or main text sections
**Cause**: Structure detection couldn't find boundaries
**Solution**:
- Check your chapter markers manually
- Use custom markers
- Or disable structure detection: `--no-detect-structure`

## Testing

Run the test suite:

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run specific test modules
python -m unittest tests.test_document_structure -v
python -m unittest tests.test_aligner -v
python -m unittest tests.test_text_extractor -v
python -m unittest tests.test_pdf_generator -v
```

## Recent Updates

### Version 2.0 (2025)
- ✨ **Structure-Aware Alignment**: Automatic detection of front matter, main text, and back matter
- 🖼️ **Image Support**: Full image extraction and rendering from PDF and ePub
- 🎯 **Smart Chapter Detection**: Recognizes English and Chinese chapter patterns
- 🔧 **Custom Markers**: Manual boundary specification for precise control
- 📊 **Multiple Image Matching Modes**: Position, page, proximity, and inline modes
- 🎨 **Image Optimization**: Automatic resizing and compression
- 📝 **Caption Preservation**: Extracts and displays image captions
- 🚀 **Enhanced CLI**: New options for structure and image control
- 🔄 **Backward Compatible**: All new features are optional

### Version 1.0
- Basic text extraction from PDF, ePub, and txt files
- Sentence and paragraph-level alignment
- Simple PDF generation

## Project Structure

```
mandarin_english_reader/
├── bilingual_reader/
│   ├── __init__.py
│   ├── cli.py                    # Command-line interface
│   ├── text_extractor.py         # Text and image extraction
│   ├── aligner.py                # Text alignment logic
│   ├── pdf_generator.py          # PDF generation
│   ├── document_structure.py     # Structure detection (chapters, etc.)
│   └── image_extractor.py        # Image processing
├── tests/
│   ├── test_text_extractor.py
│   ├── test_aligner.py
│   ├── test_pdf_generator.py
│   └── test_document_structure.py
├── requirements.txt
├── setup.py
└── README.md
```

## Contributing

Contributions are welcome! Here's how you can help:

### Areas for Contribution
- 🌍 **Language Support**: Add support for more chapter marker patterns
- 🎨 **PDF Styling**: Improve output formatting and styling options
- 🔍 **Better Structure Detection**: Machine learning-based chapter detection
- 📊 **Enhanced Image Matching**: Improve proximity-based matching algorithm
- 🧪 **Testing**: Add more test cases and edge cases
- 📚 **Documentation**: Improve examples and tutorials
- 🐛 **Bug Fixes**: Report and fix issues

### Development Setup
```bash
git clone https://github.com/liemmnguyen/mandarin_english_reader.git
cd mandarin_english_reader
pip install -e ".[dev]"  # Install with development dependencies
python -m unittest discover -v  # Run tests
```

### Submitting Changes
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python -m unittest discover -v`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Acknowledgments

- **Lingtrain Aligner**: For excellent sentence-level text segmentation
- **PyMuPDF**: For reliable PDF image extraction
- **ReportLab**: For flexible PDF generation
- **BeautifulSoup**: For HTML/XML parsing

## License

MIT License - see LICENSE file for details

## Support

- 📧 **Issues**: [GitHub Issues](https://github.com/liemmnguyen/mandarin_english_reader/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/liemmnguyen/mandarin_english_reader/discussions)
- 📖 **Documentation**: This README and inline code documentation

## Roadmap

Future enhancements planned:
- [ ] Web interface for easier use
- [ ] Support for more file formats (MOBI, AZW3)
- [ ] Advanced image matching using computer vision
- [ ] Customizable PDF styling and themes
- [ ] Export to other formats (HTML, ePub)
- [ ] Batch processing for multiple books
- [ ] Integration with translation APIs