"""Tests for text_extractor module."""

import os
import tempfile
import unittest
from bilingual_reader.text_extractor import TextExtractor


class TestTextExtractor(unittest.TestCase):
    """Test cases for TextExtractor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_text = "This is a test.\nWith multiple lines.\n"

    def test_extract_from_txt(self):
        """Test extracting text from a text file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(self.test_text)
            temp_file = f.name

        try:
            extracted = TextExtractor.extract_from_txt(temp_file)
            self.assertEqual(extracted, self.test_text)
        finally:
            os.unlink(temp_file)

    def test_extract_text_txt(self):
        """Test extract_text method with txt file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(self.test_text)
            temp_file = f.name

        try:
            extracted = TextExtractor.extract_text(temp_file)
            self.assertEqual(extracted, self.test_text)
        finally:
            os.unlink(temp_file)

    def test_extract_text_unsupported_format(self):
        """Test extract_text with unsupported file format."""
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as f:
            temp_file = f.name

        try:
            with self.assertRaises(ValueError) as context:
                TextExtractor.extract_text(temp_file)
            self.assertIn("Unsupported file format", str(context.exception))
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()
