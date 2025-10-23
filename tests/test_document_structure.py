"""Tests for document structure detection module."""

import unittest
from bilingual_reader.document_structure import (
    DocumentSection,
    detect_main_text_start,
    detect_main_text_end,
    split_document,
    get_chapter_info
)


class TestDocumentSection(unittest.TestCase):
    """Test cases for DocumentSection dataclass."""

    def test_initialization(self):
        """Test DocumentSection initialization."""
        doc = DocumentSection(
            front_matter="Preface",
            main_text="Chapter 1",
            back_matter="Appendix"
        )
        self.assertEqual(doc.front_matter, "Preface")
        self.assertEqual(doc.main_text, "Chapter 1")
        self.assertEqual(doc.back_matter, "Appendix")

    def test_empty_initialization(self):
        """Test DocumentSection with empty strings."""
        doc = DocumentSection()
        self.assertEqual(doc.front_matter, "")
        self.assertEqual(doc.main_text, "")
        self.assertEqual(doc.back_matter, "")


class TestChapterDetection(unittest.TestCase):
    """Test cases for chapter marker detection."""

    def test_detect_english_chapter(self):
        """Test detection of English chapter markers."""
        text = """Title Page

Copyright Notice

Chapter 1
This is the first chapter."""

        pos = detect_main_text_start(text)
        self.assertGreater(pos, 0)
        self.assertIn("Chapter 1", text[pos:pos+20])

    def test_detect_chinese_chapter(self):
        """Test detection of Chinese chapter markers."""
        text = """标题页

版权信息

第一章
这是第一章的内容。"""

        pos = detect_main_text_start(text)
        self.assertGreater(pos, 0)
        self.assertIn("第一章", text[pos:pos+10])

    def test_detect_roman_numeral_chapter(self):
        """Test detection of Roman numeral chapters."""
        text = """Preface by the Author

Chapter I
The story begins here."""

        pos = detect_main_text_start(text)
        self.assertGreater(pos, 0)
        self.assertIn("Chapter I", text[pos:pos+20])

    def test_no_chapter_found(self):
        """Test when no chapter marker is found."""
        text = """This is just plain text without any chapter markers.
It should return 0."""

        pos = detect_main_text_start(text)
        self.assertEqual(pos, 0)

    def test_custom_marker(self):
        """Test using a custom marker."""
        text = """Introduction

MAIN CONTENT STARTS HERE

This is the actual content."""

        pos = detect_main_text_start(text, custom_marker="MAIN CONTENT")
        self.assertGreater(pos, 0)
        self.assertIn("MAIN CONTENT", text[pos:pos+30])


class TestBackMatterDetection(unittest.TestCase):
    """Test cases for back matter detection."""

    def test_detect_appendix(self):
        """Test detection of appendix."""
        text = """Chapter 1
Content here.

Appendix
Additional information."""

        start_pos = detect_main_text_start(text)
        end_pos = detect_main_text_end(text, start_pos)

        self.assertIsNotNone(end_pos)
        self.assertIn("Appendix", text[end_pos:end_pos+20])

    def test_detect_chinese_appendix(self):
        """Test detection of Chinese appendix."""
        text = """第一章
正文内容。

附录
附加信息。"""

        start_pos = detect_main_text_start(text)
        end_pos = detect_main_text_end(text, start_pos)

        self.assertIsNotNone(end_pos)
        self.assertIn("附录", text[end_pos:end_pos+10])

    def test_no_back_matter(self):
        """Test when no back matter is found."""
        text = """Chapter 1
The content continues to the end."""

        start_pos = detect_main_text_start(text)
        end_pos = detect_main_text_end(text, start_pos)

        self.assertIsNone(end_pos)


class TestSplitDocument(unittest.TestCase):
    """Test cases for document splitting."""

    def test_split_with_all_sections(self):
        """Test splitting a document with front, main, and back matter."""
        text = """Title: My Book
By: Author Name

Chapter 1
This is the first chapter.
It has multiple sentences.

Chapter 2
This is the second chapter.

Appendix A
Additional notes here."""

        doc = split_document(text)

        self.assertIn("Title: My Book", doc.front_matter)
        self.assertIn("Chapter 1", doc.main_text)
        self.assertIn("Appendix A", doc.back_matter)

    def test_split_with_custom_markers(self):
        """Test splitting with custom markers."""
        text = """Front stuff

START HERE
Main content

END HERE
Back stuff"""

        doc = split_document(
            text,
            start_marker="START HERE",
            end_marker="END HERE"
        )

        self.assertIn("Front stuff", doc.front_matter)
        self.assertIn("Main content", doc.main_text)
        self.assertIn("Back stuff", doc.back_matter)

    def test_split_with_manual_positions(self):
        """Test splitting with manual character positions."""
        text = "0123456789ABCDEFGHIJKLMNOP"

        doc = split_document(
            text,
            start_position=10,
            end_position=20
        )

        self.assertEqual(doc.front_matter, "0123456789")
        self.assertEqual(doc.main_text, "ABCDEFGHIJ")
        self.assertEqual(doc.back_matter, "KLMNOP")

    def test_split_no_front_matter(self):
        """Test splitting when document starts with main text."""
        text = """Chapter 1
Main content here."""

        doc = split_document(text)

        self.assertEqual(doc.front_matter, "")
        self.assertIn("Chapter 1", doc.main_text)

    def test_split_chinese_document(self):
        """Test splitting a Chinese document."""
        text = """书名：我的书
作者：作者名

第一章
这是第一章的内容。

第二章
这是第二章的内容。

附录
附加信息。"""

        doc = split_document(text)

        self.assertIn("书名", doc.front_matter)
        self.assertIn("第一章", doc.main_text)
        self.assertIn("附录", doc.back_matter)


class TestGetChapterInfo(unittest.TestCase):
    """Test cases for extracting chapter information."""

    def test_get_chapters(self):
        """Test extracting chapter positions and titles."""
        text = """Title Page

Chapter 1
Content 1

Chapter 2
Content 2

Chapter 3
Content 3"""

        chapters = get_chapter_info(text)

        self.assertEqual(len(chapters), 3)
        self.assertIn("Chapter 1", chapters[0][1])
        self.assertIn("Chapter 2", chapters[1][1])
        self.assertIn("Chapter 3", chapters[2][1])

    def test_get_chinese_chapters(self):
        """Test extracting Chinese chapters."""
        text = """标题页

第一章
内容一

第二章
内容二"""

        chapters = get_chapter_info(text)

        self.assertGreaterEqual(len(chapters), 2)
        self.assertIn("第一章", chapters[0][1])

    def test_no_chapters(self):
        """Test when no chapters are found."""
        text = """This is a document without chapters.
Just plain text."""

        chapters = get_chapter_info(text)

        self.assertEqual(len(chapters), 0)


if __name__ == '__main__':
    unittest.main()
