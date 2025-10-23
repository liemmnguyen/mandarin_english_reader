# Quick Start Guide

Get started with Mandarin English Reader in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/liemmnguyen/mandarin_english_reader.git
cd mandarin_english_reader

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Your First Bilingual PDF

### Step 1: Prepare Your Files

You need two text files containing the same content in different languages. For this tutorial, we'll use the included example files:

- `examples/sample_english.txt` - English text
- `examples/sample_chinese.txt` - Chinese text

### Step 2: Generate the PDF

Run this command:

```bash
bilingual-pdf --input1 examples/sample_english.txt \
              --input2 examples/sample_chinese.txt \
              --output my_first_bilingual.pdf \
              --mode sentence
```

### Step 3: View Your PDF

Open `my_first_bilingual.pdf` in any PDF viewer. You'll see alternating English and Chinese sentences!

## Common Use Cases

### Reading Novels

Convert a novel in two languages into a bilingual reader:

```bash
bilingual-pdf --input1 english_novel.pdf \
              --input2 chinese_novel.pdf \
              --output bilingual_novel.pdf \
              --mode paragraph
```

### Language Learning

Create study materials with sentence-level alignment:

```bash
bilingual-pdf --input1 lesson_en.txt \
              --input2 lesson_zh.txt \
              --output study_material.pdf \
              --mode sentence \
              --title "Lesson 1: Basic Conversation"
```

### ePub Books

The tool supports ePub format too:

```bash
bilingual-pdf --input1 book_en.epub \
              --input2 book_zh.epub \
              --output bilingual_book.pdf \
              --mode paragraph
```

## Tips for Best Results

1. **Use matching content**: Both files should contain the same content translated into different languages
2. **Choose the right mode**: 
   - Use `sentence` mode for short texts and language learning
   - Use `paragraph` mode for longer texts and novels
3. **Specify languages**: Use `--lang1` and `--lang2` to specify language codes for better text splitting
4. **Custom titles**: Use `--title` to give your PDF a meaningful title

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the [examples](examples/) directory for sample files
- Try the programmatic API for integration into your own projects

## Getting Help

If you encounter any issues:
1. Check the [Troubleshooting](README.md#troubleshooting) section in README.md
2. Make sure all dependencies are installed correctly
3. Verify your input files are in supported formats (PDF, ePub, or txt)
4. Open an issue on GitHub with details about your problem

Happy reading! 📚
