"""Tests for pdf_generator module."""

import os
import tempfile
import unittest
from bilingual_reader.pdf_generator import PDFGenerator


class TestPDFGenerator(unittest.TestCase):
    """Test cases for PDFGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_path = os.path.join(self.temp_dir, "test_output.pdf")
        self.generator = PDFGenerator(self.output_path, title="Test Document")

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.output_path):
            os.unlink(self.output_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_initialization(self):
        """Test PDFGenerator initialization."""
        self.assertEqual(self.generator.output_path, self.output_path)
        self.assertEqual(self.generator.title, "Test Document")
        self.assertIsNotNone(self.generator.styles)

    def test_sanitize_text(self):
        """Test text sanitization."""
        text = "Text with <tags> & special chars"
        sanitized = self.generator._sanitize_text(text)
        self.assertNotIn("<", sanitized)
        self.assertNotIn(">", sanitized)
        self.assertIn("&lt;", sanitized)
        self.assertIn("&gt;", sanitized)
        self.assertIn("&amp;", sanitized)

    def test_generate_pdf_basic(self):
        """Test basic PDF generation."""
        aligned_texts = [
            ("First English sentence.", "第一个中文句子。"),
            ("Second English sentence.", "第二个中文句子。"),
        ]
        
        self.generator.generate_pdf(aligned_texts)
        
        # Check that PDF file was created
        self.assertTrue(os.path.exists(self.output_path))
        # Check that file has content
        self.assertGreater(os.path.getsize(self.output_path), 0)

    def test_generate_pdf_empty_segments(self):
        """Test PDF generation with empty segments."""
        aligned_texts = [
            ("First sentence.", ""),
            ("", "第二个句子。"),
            ("Third sentence.", "第三个句子。"),
        ]
        
        self.generator.generate_pdf(aligned_texts)
        
        # Should handle empty segments gracefully
        self.assertTrue(os.path.exists(self.output_path))
        self.assertGreater(os.path.getsize(self.output_path), 0)

    def test_generate_pdf_special_characters(self):
        """Test PDF generation with special characters."""
        aligned_texts = [
            ("Text with <brackets> & ampersand", "特殊字符"),
            ("Quote: \"Hello\"", "引号"),
        ]
        
        self.generator.generate_pdf(aligned_texts)
        
        self.assertTrue(os.path.exists(self.output_path))
        self.assertGreater(os.path.getsize(self.output_path), 0)


if __name__ == '__main__':
    unittest.main()
