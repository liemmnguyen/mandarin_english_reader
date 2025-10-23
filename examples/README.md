# Example Files

This directory contains sample files to test the bilingual PDF generator.

## Files

- `sample_english.txt` - English version of "The Little Prince" excerpt
- `sample_chinese.txt` - Chinese version of "The Little Prince" excerpt
- `atomic_habits_english.epub` - English version of "Atomic Habits" by James Clear
- `atomic_habits_chinese.epub` - Chinese version of "Atomic Habits" (原子习惯)

## Usage

### Basic Examples with Text Files

#### Sentence-level alignment

```bash
bilingual-pdf --input1 examples/sample_english.txt \
              --input2 examples/sample_chinese.txt \
              --output examples/output_sentence.pdf \
              --mode sentence \
              --title "The Little Prince (English-Chinese)"
```

#### Paragraph-level alignment

```bash
bilingual-pdf --input1 examples/sample_english.txt \
              --input2 examples/sample_chinese.txt \
              --output examples/output_paragraph.pdf \
              --mode paragraph \
              --title "The Little Prince (English-Chinese)"
```

### Advanced Examples with EPUB Files

#### Atomic Habits - Basic Generation

Generate a bilingual PDF with default settings (structure detection and image extraction enabled):

```bash
bilingual-pdf --input1 examples/atomic_habits_english.epub \
              --input2 examples/atomic_habits_chinese.epub \
              --output examples/atomic_habits_bilingual.pdf \
              --title "Atomic Habits | 原子习惯"
```

#### Atomic Habits - Sentence-level Alignment

For more granular alignment at the sentence level:

```bash
bilingual-pdf --input1 examples/atomic_habits_english.epub \
              --input2 examples/atomic_habits_chinese.epub \
              --output examples/atomic_habits_sentence.pdf \
              --mode sentence \
              --title "Atomic Habits | 原子习惯"
```

#### Atomic Habits - Paragraph-level Alignment (Faster)

For faster processing with paragraph-level alignment:

```bash
bilingual-pdf --input1 examples/atomic_habits_english.epub \
              --input2 examples/atomic_habits_chinese.epub \
              --output examples/atomic_habits_paragraph.pdf \
              --mode paragraph \
              --title "Atomic Habits | 原子习惯"
```

#### Atomic Habits - With Image Extraction

Extract and include images from the EPUB files:

```bash
bilingual-pdf --input1 examples/atomic_habits_english.epub \
              --input2 examples/atomic_habits_chinese.epub \
              --output examples/atomic_habits_with_images.pdf \
              --extract-images \
              --image-match-mode position \
              --title "Atomic Habits | 原子习惯"
```

#### Atomic Habits - Custom Structure Detection

If automatic structure detection doesn't work perfectly, you can specify custom chapter markers:

```bash
bilingual-pdf --input1 examples/atomic_habits_english.epub \
              --input2 examples/atomic_habits_chinese.epub \
              --output examples/atomic_habits_custom.pdf \
              --start-marker1 "Introduction" \
              --start-marker2 "引言" \
              --title "Atomic Habits | 原子习惯"
```

#### Atomic Habits - Without Structure Detection

For a simpler output without front/back matter separation:

```bash
bilingual-pdf --input1 examples/atomic_habits_english.epub \
              --input2 examples/atomic_habits_chinese.epub \
              --output examples/atomic_habits_simple.pdf \
              --no-detect-structure \
              --title "Atomic Habits | 原子习惯"
```

## Testing

You can run integration tests with the atomic habits files:

```bash
# Run all integration tests
python -m unittest tests.test_integration_atomic_habits -v

# Run a specific test
python -m unittest tests.test_integration_atomic_habits.TestIntegrationAtomicHabits.test_generate_pdf_output -v
```

## Expected Output

The generated PDF will contain alternating text segments from both languages:
- In **sentence mode**: Each sentence from the English text is followed by the corresponding Chinese sentence
- In **paragraph mode**: Each paragraph from the English text is followed by the corresponding Chinese paragraph

With structure detection enabled, the PDF will have three sections:
1. **Front Matter**: Preface, table of contents, copyright (side-by-side, not sentence-aligned)
2. **Main Text**: Aligned bilingual content with alternating language segments
3. **Back Matter**: Appendix, notes, index (side-by-side, not sentence-aligned)

This creates a reader-friendly bilingual document ideal for language learning.
