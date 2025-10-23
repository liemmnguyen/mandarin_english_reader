"""Module for aligning text from two languages."""

from typing import List, Tuple
try:
    from lingtrain_aligner import splitter
    USE_LINGTRAIN = True
except ImportError:
    USE_LINGTRAIN = False


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
