import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_corect_input(self):
        md = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)
"""
        title = extract_title(md)
        self.assertEqual(title, "Tolkien Fan Club")
