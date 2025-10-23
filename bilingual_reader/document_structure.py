"""Data structures and utilities for document structure analysis."""

import re
from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class DocumentSection:
    """Represents a structured document with front matter, main text, and back matter."""

    front_matter: str
    main_text: str
    back_matter: str

    def __init__(self, front_matter: str = "", main_text: str = "", back_matter: str = ""):
        """Initialize document section.

        Args:
            front_matter: Text before main content (title, preface, TOC, etc.)
            main_text: Main body content
            back_matter: Text after main content (appendix, notes, etc.)
        """
        self.front_matter = front_matter
        self.main_text = main_text
        self.back_matter = back_matter


# Comprehensive chapter marker patterns for English and Chinese
CHAPTER_PATTERNS = [
    # English patterns
    r'^chapter\s+\d+',           # "Chapter 1", "Chapter 12"
    r'^chapter\s+[ivxlcdm]+',    # "Chapter I", "Chapter XII" (Roman numerals)
    r'^chapter\s+one',           # "Chapter One", "Chapter Two"
    r'^ch\.\s*\d+',              # "Ch. 1", "Ch.1"
    r'^part\s+\d+',              # "Part 1", "Part 2"
    r'^part\s+[ivxlcdm]+',       # "Part I", "Part II"
    r'^book\s+\d+',              # "Book 1", "Book 2"
    r'^book\s+[ivxlcdm]+',       # "Book I", "Book II"
    r'^\d+\.\s+[A-Z]',           # "1. Introduction", "2. Background"
    r'^section\s+\d+',           # "Section 1", "Section 2"
    r'^prologue',                # "Prologue"
    r'^epilogue',                # "Epilogue"
    r'^introduction$',           # "Introduction"
    r'^preface$',                # "Preface"

    # Chinese patterns
    r'^第[一二三四五六七八九十百千0-9]+章',      # "第一章", "第12章"
    r'^第[一二三四五六七八九十百千0-9]+节',      # "第一节", "第12节"
    r'^第[一二三四五六七八九十百千0-9]+部分',    # "第一部分"
    r'^第[一二三四五六七八九十百千0-9]+卷',      # "第一卷"
    r'^第[一二三四五六七八九十百千0-9]+回',      # "第一回" (classical Chinese)
    r'^卷[一二三四五六七八九十百千0-9]+',        # "卷一"
    r'^篇[一二三四五六七八九十百千0-9]+',        # "篇一"
    r'^序章',                                      # "序章" (Prologue)
    r'^终章',                                      # "终章" (Epilogue)
    r'^引言',                                      # "引言" (Introduction)
    r'^前言',                                      # "前言" (Preface)
    r'^楔子',                                      # "楔子" (Prologue in novels)

    # Mixed/numbered patterns
    r'^[0-9]+\s*[\.、]\s*[\u4e00-\u9fff]',       # "1. 引言", "1、背景"
    r'^[一二三四五六七八九十]+[\.、]',           # "一、", "二、"
]


def detect_main_text_start(text: str, custom_marker: Optional[str] = None) -> int:
    """Detect where the main text starts based on chapter markers.

    Args:
        text: The full text to analyze
        custom_marker: Optional custom marker to look for (takes precedence)

    Returns:
        Character position where main text starts (0 if not found)
    """
    if custom_marker:
        # Use custom marker if provided
        match = re.search(re.escape(custom_marker), text, re.IGNORECASE)
        if match:
            return match.start()

    # Try each pattern
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line_stripped = line.strip()

        # Skip empty lines
        if not line_stripped:
            continue

        # Check against all chapter patterns
        for pattern in CHAPTER_PATTERNS:
            if re.match(pattern, line_stripped, re.IGNORECASE):
                # Found a chapter marker - calculate character position
                char_position = sum(len(lines[j]) + 1 for j in range(i))  # +1 for newline
                return char_position

    # No chapter marker found
    return 0


def detect_main_text_end(text: str, start_pos: int = 0) -> Optional[int]:
    """Detect where the main text ends (start of back matter).

    Args:
        text: The full text to analyze
        start_pos: Position where main text starts

    Returns:
        Character position where back matter starts (None if not found)
    """
    # Common back matter markers
    back_matter_patterns = [
        r'^appendix',
        r'^bibliography',
        r'^references',
        r'^index$',
        r'^glossary',
        r'^notes$',
        r'^acknowledgements',
        r'^afterword',
        r'^about the author',
        r'^附录',      # Appendix
        r'^参考文献',   # References
        r'^索引',      # Index
        r'^词汇表',    # Glossary
        r'^注释',      # Notes
        r'^后记',      # Afterword
        r'^致谢',      # Acknowledgements
    ]

    text_from_start = text[start_pos:]
    lines = text_from_start.split('\n')

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        # Skip empty lines
        if not line_stripped:
            continue

        # Check against back matter patterns
        for pattern in back_matter_patterns:
            if re.match(pattern, line_stripped, re.IGNORECASE):
                # Found back matter - calculate absolute character position
                char_position = start_pos + sum(len(lines[j]) + 1 for j in range(i))
                return char_position

    # No back matter found
    return None


def split_document(
    text: str,
    start_marker: Optional[str] = None,
    end_marker: Optional[str] = None,
    start_position: Optional[int] = None,
    end_position: Optional[int] = None
) -> DocumentSection:
    """Split a document into front matter, main text, and back matter.

    Args:
        text: The full document text
        start_marker: Custom marker for where main text starts (optional)
        end_marker: Custom marker for where back matter starts (optional)
        start_position: Manual character position for main text start (takes precedence)
        end_position: Manual character position for back matter start (takes precedence)

    Returns:
        DocumentSection with the three parts split
    """
    # Determine start position
    if start_position is not None:
        main_start = start_position
    else:
        main_start = detect_main_text_start(text, start_marker)

    # Determine end position
    if end_position is not None:
        main_end = end_position
    elif end_marker:
        # Use custom end marker if provided
        match = re.search(re.escape(end_marker), text[main_start:], re.IGNORECASE)
        if match:
            main_end = main_start + match.start()
        else:
            main_end = len(text)
    else:
        detected_end = detect_main_text_end(text, main_start)
        main_end = detected_end if detected_end is not None else len(text)

    # Split the document
    front_matter = text[:main_start].strip()
    main_text = text[main_start:main_end].strip()
    back_matter = text[main_end:].strip() if main_end < len(text) else ""

    return DocumentSection(
        front_matter=front_matter,
        main_text=main_text,
        back_matter=back_matter
    )


def get_chapter_info(text: str) -> List[Tuple[int, str]]:
    """Extract all chapter positions and titles from text.

    Args:
        text: The text to analyze

    Returns:
        List of tuples (character_position, chapter_title)
    """
    chapters = []
    lines = text.split('\n')

    char_position = 0
    for line in lines:
        line_stripped = line.strip()

        if line_stripped:
            # Check against all chapter patterns
            for pattern in CHAPTER_PATTERNS:
                if re.match(pattern, line_stripped, re.IGNORECASE):
                    chapters.append((char_position, line_stripped))
                    break

        char_position += len(line) + 1  # +1 for newline

    return chapters
