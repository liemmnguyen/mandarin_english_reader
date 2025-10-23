import unittest
from your_module import extract_text_from_epub, detect_structure, align_texts, extract_images, generate_pdf

class TestIntegrationAtomicHabits(unittest.TestCase):

    def setUp(self):
        self.english_epub = 'examples/atomic_habits_english.epub'
        self.chinese_epub = 'examples/atomic_habits_chinese.epub'

    def tearDown(self):
        # Clean up actions if needed
        pass

    def test_extract_text_from_epub(self):
        english_text = extract_text_from_epub(self.english_epub)
        chinese_text = extract_text_from_epub(self.chinese_epub)
        self.assertIsNotNone(english_text)
        self.assertIsNotNone(chinese_text)

    def test_extract_with_structure_detection(self):
        structured_data = detect_structure(self.english_epub)
        self.assertIsNotNone(structured_data)

    def test_extract_images(self):
        english_images = extract_images(self.english_epub)
        chinese_images = extract_images(self.chinese_epub)
        self.assertGreater(len(english_images), 0)
        self.assertGreater(len(chinese_images), 0)

    def test_align_texts_in_paragraph_mode(self):
        aligned_texts = align_texts(self.english_epub, self.chinese_epub, mode='paragraph')
        self.assertIsNotNone(aligned_texts)

    def test_align_texts_in_sentence_mode(self):
        aligned_texts = align_texts(self.english_epub, self.chinese_epub, mode='sentence')
        self.assertIsNotNone(aligned_texts)

    def test_generate_pdf_output(self):
        pdf_path = generate_pdf(self.english_epub, self.chinese_epub)
        self.assertTrue(pdf_path.endswith('.pdf'))

    def test_full_integration(self):
        # Run all steps for a full integration test
        english_text = extract_text_from_epub(self.english_epub)
        chinese_text = extract_text_from_epub(self.chinese_epub)
        structured_data = detect_structure(self.english_epub)
        aligned_texts = align_texts(self.english_epub, self.chinese_epub)
        english_images = extract_images(self.english_epub)
        chinese_images = extract_images(self.chinese_epub)
        pdf_path = generate_pdf(self.english_epub, self.chinese_epub)
        self.assertTrue(os.path.exists(pdf_path))

if __name__ == '__main__':
    unittest.main()