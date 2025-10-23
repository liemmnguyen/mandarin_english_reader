"""Module for aligning text from two languages."""

from typing import List, Tuple, NamedTuple, Optional
try:
    from lingtrain_aligner import splitter
    USE_LINGTRAIN = True
except ImportError:
    USE_LINGTRAIN = False

from .document_structure import DocumentSection
from .text_extractor import DocumentWithImages
from .image_extractor import (
    ImageBlock,
    match_images_by_position,
    match_images_by_page,
    match_images_by_proximity
)


class AlignedDocument(NamedTuple):
    """Structure for aligned bilingual documents with front/main/back matter."""

    front_matter: List[Tuple[str, str]]
    main_text: List[Tuple[str, str]]
    back_matter: List[Tuple[str, str]]


class AlignedDocumentWithImages(NamedTuple):
    """Structure for aligned bilingual documents with images."""

    front_matter: List[Tuple[str, str]]
    main_text: List[Tuple[str, str]]
    back_matter: List[Tuple[str, str]]
    matched_images: List[Tuple[ImageBlock, ImageBlock]]
    unmatched_images1: List[ImageBlock]
    unmatched_images2: List[ImageBlock]


class BilingualAligner:
    """Align texts in two languages."""

    def __init__(self, lang1: str = "en", lang2: str = "zh"):
        """Initialize the aligner with language codes.
        
        Args:
            lang1: Language code for first language (default: "en")
            lang2: Language code for second language (default: "zh")
        """
        self.lang1 = lang1
        self.lang2 = lang2

    def align_texts(
        self,
        text1: str,
        text2: str,
        alignment_mode: str = "sentence"
    ) -> List[Tuple[str, str]]:
        """Align two texts at sentence or paragraph level.
        
        This method uses a simple sequential alignment strategy where
        segments from both texts are paired in order. For more complex
        alignment, consider using lingtrain-aligner's full workflow.
        
        Args:
            text1: Text in first language
            text2: Text in second language
            alignment_mode: "sentence" or "paragraph" alignment
            
        Returns:
            List of tuples containing aligned text segments
        """
        # Split texts based on alignment mode
        if alignment_mode == "paragraph":
            segments1 = self._split_paragraphs(text1)
            segments2 = self._split_paragraphs(text2)
        else:  # sentence mode
            if not USE_LINGTRAIN:
                raise ImportError(
                    "lingtrain-aligner is required for sentence-level alignment. "
                    "Install it with: pip install lingtrain-aligner"
                )
            segments1 = splitter.split_by_sentences_wrapper(text1, self.lang1)
            segments2 = splitter.split_by_sentences_wrapper(text2, self.lang2)

        # Simple sequential alignment
        # Pair segments in order, padding with empty strings if lengths differ
        max_len = max(len(segments1), len(segments2))
        result = []
        
        for i in range(max_len):
            seg1 = segments1[i] if i < len(segments1) else ""
            seg2 = segments2[i] if i < len(segments2) else ""
            
            # Only add if at least one segment has content
            if seg1.strip() or seg2.strip():
                result.append((seg1.strip(), seg2.strip()))
        
        return result

    def align_documents(
        self,
        doc1: DocumentSection,
        doc2: DocumentSection,
        alignment_mode: str = "sentence"
    ) -> AlignedDocument:
        """Align two structured documents with front matter, main text, and back matter.

        Front and back matter are concatenated side-by-side (not sentence-aligned).
        Main text is aligned sentence-by-sentence or paragraph-by-paragraph.

        Args:
            doc1: First document section (typically English)
            doc2: Second document section (typically Chinese)
            alignment_mode: "sentence" or "paragraph" alignment for main text

        Returns:
            AlignedDocument with front_matter, main_text, and back_matter aligned
        """
        # Handle front matter - simple concatenation (side-by-side)
        front_matter_aligned = []
        if doc1.front_matter or doc2.front_matter:
            front_matter_aligned = [(doc1.front_matter, doc2.front_matter)]

        # Handle main text - sentence/paragraph alignment
        main_text_aligned = []
        if doc1.main_text or doc2.main_text:
            main_text_aligned = self.align_texts(
                doc1.main_text,
                doc2.main_text,
                alignment_mode=alignment_mode
            )

        # Handle back matter - simple concatenation (side-by-side)
        back_matter_aligned = []
        if doc1.back_matter or doc2.back_matter:
            back_matter_aligned = [(doc1.back_matter, doc2.back_matter)]

        return AlignedDocument(
            front_matter=front_matter_aligned,
            main_text=main_text_aligned,
            back_matter=back_matter_aligned
        )

    def align_documents_with_images(
        self,
        doc1: DocumentWithImages,
        doc2: DocumentWithImages,
        alignment_mode: str = "sentence",
        image_match_mode: str = "inline"
    ) -> AlignedDocumentWithImages:
        """Align two documents with images.

        Args:
            doc1: First document with images
            doc2: Second document with images
            alignment_mode: "sentence" or "paragraph" alignment for text
            image_match_mode: "inline", "position", "page", or "proximity" for images

        Returns:
            AlignedDocumentWithImages with aligned text and images
        """
        # Handle front matter - simple concatenation (side-by-side)
        front_matter_aligned = []
        if doc1.front_matter or doc2.front_matter:
            front_matter_aligned = [(doc1.front_matter, doc2.front_matter)]

        # Handle main text - sentence/paragraph alignment
        main_text_aligned = []
        if doc1.main_text or doc2.main_text:
            main_text_aligned = self.align_texts(
                doc1.main_text,
                doc2.main_text,
                alignment_mode=alignment_mode
            )

        # Handle back matter - simple concatenation (side-by-side)
        back_matter_aligned = []
        if doc1.back_matter or doc2.back_matter:
            back_matter_aligned = [(doc1.back_matter, doc2.back_matter)]

        # Handle images
        matched_images = []
        unmatched_images1 = []
        unmatched_images2 = []

        if image_match_mode == "inline":
            # No matching - treat all images as unmatched
            unmatched_images1 = doc1.images
            unmatched_images2 = doc2.images
        elif image_match_mode == "position":
            matched_images, unmatched_images1, unmatched_images2 = match_images_by_position(
                doc1.images, doc2.images
            )
        elif image_match_mode == "page":
            matched_images, unmatched_images1, unmatched_images2 = match_images_by_page(
                doc1.images, doc2.images
            )
        elif image_match_mode == "proximity":
            # TODO: Pass aligned text positions for better matching
            matched_images, unmatched_images1, unmatched_images2 = match_images_by_proximity(
                doc1.images, doc2.images, []
            )

        return AlignedDocumentWithImages(
            front_matter=front_matter_aligned,
            main_text=main_text_aligned,
            back_matter=back_matter_aligned,
            matched_images=matched_images,
            unmatched_images1=unmatched_images1,
            unmatched_images2=unmatched_images2
        )

    def _split_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs.
        
        Args:
            text: Text to split
            
        Returns:
            List of paragraphs
        """
        # Split by double newlines or multiple newlines
        paragraphs = []
        current_para = []
        
        for line in text.split('\n'):
            line = line.strip()
            if line:
                current_para.append(line)
            elif current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
        
        # Add last paragraph if exists
        if current_para:
            paragraphs.append(' '.join(current_para))
        
        return [p for p in paragraphs if p]
