"""Tests for aligner module."""

import unittest
from bilingual_reader.aligner import BilingualAligner, AlignedDocument
from bilingual_reader.document_structure import DocumentSection


class TestBilingualAligner(unittest.TestCase):
    """Test cases for BilingualAligner class."""

    def setUp(self):
        """Set up test fixtures."""
        self.aligner = BilingualAligner(lang1="en", lang2="zh")
        
        self.text1 = "This is sentence one. This is sentence two. This is sentence three."
        self.text2 = "这是第一句。这是第二句。这是第三句。"
        
        self.para_text1 = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        self.para_text2 = "第一段。\n\n第二段。\n\n第三段。"

    def test_initialization(self):
        """Test aligner initialization."""
        self.assertEqual(self.aligner.lang1, "en")
        self.assertEqual(self.aligner.lang2, "zh")

    def test_split_paragraphs(self):
        """Test paragraph splitting."""
        paragraphs = self.aligner._split_paragraphs(self.para_text1)
        self.assertEqual(len(paragraphs), 3)
        self.assertIn("First paragraph", paragraphs[0])
        self.assertIn("Second paragraph", paragraphs[1])
        self.assertIn("Third paragraph", paragraphs[2])

    def test_align_texts_sentence_mode(self):
        """Test text alignment in sentence mode."""
        aligned = self.aligner.align_texts(self.text1, self.text2, alignment_mode="sentence")
        self.assertIsInstance(aligned, list)
        self.assertGreater(len(aligned), 0)
        # Each item should be a tuple of two strings
        for item in aligned:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], str)

    def test_align_texts_paragraph_mode(self):
        """Test text alignment in paragraph mode."""
        aligned = self.aligner.align_texts(
            self.para_text1,
            self.para_text2,
            alignment_mode="paragraph"
        )
        self.assertIsInstance(aligned, list)
        self.assertEqual(len(aligned), 3)

    def test_align_empty_texts(self):
        """Test alignment with empty texts."""
        aligned = self.aligner.align_texts("", "", alignment_mode="sentence")
        self.assertEqual(len(aligned), 0)

    def test_align_unequal_lengths(self):
        """Test alignment when texts have different numbers of segments."""
        text1 = "First sentence. Second sentence. Third sentence."
        text2 = "第一句。"
        aligned = self.aligner.align_texts(text1, text2, alignment_mode="sentence")
        # Should handle unequal lengths gracefully
        self.assertIsInstance(aligned, list)
        self.assertGreater(len(aligned), 0)

    def test_align_documents_with_structure(self):
        """Test aligning documents with structure (front/main/back matter)."""
        doc1 = DocumentSection(
            front_matter="Title: My Book\nBy: John Doe",
            main_text="Chapter 1. This is the first chapter. Chapter 2. This is the second.",
            back_matter="Appendix A. Additional notes."
        )

        doc2 = DocumentSection(
            front_matter="标题：我的书\n作者：张三",
            main_text="第一章。这是第一章。第二章。这是第二章。",
            back_matter="附录A。附加说明。"
        )

        aligned_doc = self.aligner.align_documents(doc1, doc2, alignment_mode="paragraph")

        self.assertIsInstance(aligned_doc, AlignedDocument)
        self.assertGreater(len(aligned_doc.front_matter), 0)
        self.assertGreater(len(aligned_doc.main_text), 0)
        self.assertGreater(len(aligned_doc.back_matter), 0)

    def test_align_documents_no_front_matter(self):
        """Test aligning documents without front matter."""
        doc1 = DocumentSection(
            front_matter="",
            main_text="First paragraph.\n\nSecond paragraph.",
            back_matter=""
        )

        doc2 = DocumentSection(
            front_matter="",
            main_text="第一段。\n\n第二段。",
            back_matter=""
        )

        aligned_doc = self.aligner.align_documents(doc1, doc2, alignment_mode="paragraph")

        self.assertEqual(len(aligned_doc.front_matter), 0)
        self.assertGreater(len(aligned_doc.main_text), 0)
        self.assertEqual(len(aligned_doc.back_matter), 0)

    def test_align_documents_empty(self):
        """Test aligning empty documents."""
        doc1 = DocumentSection()
        doc2 = DocumentSection()

        aligned_doc = self.aligner.align_documents(doc1, doc2)

        self.assertEqual(len(aligned_doc.front_matter), 0)
        self.assertEqual(len(aligned_doc.main_text), 0)
        self.assertEqual(len(aligned_doc.back_matter), 0)


if __name__ == '__main__':
    unittest.main()
