# Example Files

This directory contains sample text files to test the bilingual PDF generator.

## Files

- `sample_english.txt` - English version of "The Little Prince" excerpt
- `sample_chinese.txt` - Chinese version of "The Little Prince" excerpt

## Usage

### Sentence-level alignment

```bash
bilingual-pdf --input1 examples/sample_english.txt \
              --input2 examples/sample_chinese.txt \
              --output examples/output_sentence.pdf \
              --mode sentence \
              --title "The Little Prince (English-Chinese)"
```

### Paragraph-level alignment

```bash
bilingual-pdf --input1 examples/sample_english.txt \
              --input2 examples/sample_chinese.txt \
              --output examples/output_paragraph.pdf \
              --mode paragraph \
              --title "The Little Prince (English-Chinese)"
```

## Expected Output

The generated PDF will contain alternating text segments from both languages:
- In **sentence mode**: Each sentence from the English text is followed by the corresponding Chinese sentence
- In **paragraph mode**: Each paragraph from the English text is followed by the corresponding Chinese paragraph

This creates a reader-friendly bilingual document ideal for language learning.
