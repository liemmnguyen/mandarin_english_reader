"""Integration tests for the atomic habits EPUB files."""

import os
import tempfile
import unittest
from bilingual_reader.text_extractor import TextExtractor
from bilingual_reader.aligner import BilingualAligner
from bilingual_reader.pdf_generator import PDFGenerator
from bilingual_reader.image_extractor import extract_images


class TestIntegrationAtomicHabits(unittest.TestCase):
    """Integration tests using the atomic habits EPUB files."""

    def setUp(self):
        """Set up test fixtures."""
        self.english_epub = 'examples/atomic_habits_english.epub'
        self.chinese_epub = 'examples/atomic_habits_chinese.epub'
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        # Clean up temp directory
        if os.path.exists(self.temp_dir):
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            os.rmdir(self.temp_dir)

    def test_extract_text_from_epub(self):
        """Test extracting text from atomic habits EPUB files."""
        english_text = TextExtractor.extract_from_epub(self.english_epub)
        chinese_text = TextExtractor.extract_from_epub(self.chinese_epub)
        
        self.assertIsNotNone(english_text)
        self.assertIsNotNone(chinese_text)
        self.assertGreater(len(english_text), 1000, "English text should be substantial")
        self.assertGreater(len(chinese_text), 1000, "Chinese text should be substantial")

    def test_extract_with_structure_detection(self):
        """Test structure detection on atomic habits EPUB files."""
        english_doc = TextExtractor.extract_with_structure(self.english_epub)
        chinese_doc = TextExtractor.extract_with_structure(self.chinese_epub)
        
        self.assertIsNotNone(english_doc)
        self.assertIsNotNone(chinese_doc)
        
        # Check that we got some content in each section
        total_english = len(english_doc.front_matter) + len(english_doc.main_text) + len(english_doc.back_matter)
        total_chinese = len(chinese_doc.front_matter) + len(chinese_doc.main_text) + len(chinese_doc.back_matter)
        
        self.assertGreater(total_english, 1000, "Should have substantial English content")
        self.assertGreater(total_chinese, 1000, "Should have substantial Chinese content")

    def test_extract_images(self):
        """Test image extraction from atomic habits EPUB files."""
        english_images = extract_images(self.english_epub)
        chinese_images = extract_images(self.chinese_epub)
        
        # These files may or may not have images, so we just check the function works
        self.assertIsInstance(english_images, list)
        self.assertIsInstance(chinese_images, list)

    def test_align_texts_in_paragraph_mode(self):
        """Test paragraph-level alignment of atomic habits texts."""
        english_text = TextExtractor.extract_text(self.english_epub)
        chinese_text = TextExtractor.extract_text(self.chinese_epub)
        
        aligner = BilingualAligner(lang1="en", lang2="zh")
        aligned_texts = aligner.align_texts(english_text, chinese_text, alignment_mode='paragraph')
        
        self.assertIsNotNone(aligned_texts)
        self.assertIsInstance(aligned_texts, list)
        self.assertGreater(len(aligned_texts), 0)

    def test_generate_pdf_output(self):
        """Test generating a PDF from atomic habits EPUB files."""
        output_path = os.path.join(self.temp_dir, 'atomic_habits_output.pdf')
        
        # Extract text
        english_text = TextExtractor.extract_text(self.english_epub)
        chinese_text = TextExtractor.extract_text(self.chinese_epub)
        
        # Align texts (using paragraph mode to avoid lingtrain-aligner issues)
        aligner = BilingualAligner(lang1="en", lang2="zh")
        aligned_texts = aligner.align_texts(english_text, chinese_text, alignment_mode='paragraph')
        
        # Generate PDF
        pdf_gen = PDFGenerator(output_path, title="Atomic Habits (English-Chinese)")
        pdf_gen.generate_pdf(aligned_texts)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 1000)

    def test_full_integration_with_structure(self):
        """Full integration test with structure detection and PDF generation."""
        output_path = os.path.join(self.temp_dir, 'atomic_habits_structured.pdf')
        
        # Extract with structure
        english_doc = TextExtractor.extract_with_structure_and_images(
            self.english_epub,
            extract_images_flag=True
        )
        chinese_doc = TextExtractor.extract_with_structure_and_images(
            self.chinese_epub,
            extract_images_flag=True
        )
        
        # Align documents
        aligner = BilingualAligner(lang1="en", lang2="zh")
        aligned_doc = aligner.align_documents(english_doc, chinese_doc, alignment_mode='paragraph')
        
        # Generate PDF
        pdf_gen = PDFGenerator(output_path, title="Atomic Habits (English-Chinese)")
        pdf_gen.generate_pdf_from_aligned_document(
            aligned_doc,
            lang1_name="English",
            lang2_name="中文"
        )
        
        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 1000)


if __name__ == '__main__':
    unittest.main()