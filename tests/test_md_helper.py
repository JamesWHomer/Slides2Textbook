import unittest

from slides2textbook import md_helper


class NormalizeDisplayMathTests(unittest.TestCase):
    def test_joins_leading_operator_to_first_expression(self):
        markdown = r"""
\[
-
E\left[X\right]
\]

$$
+
x
$$
"""

        normalized = md_helper._normalize_display_math(markdown)

        self.assertIn("\\[\n-E\\left[X\\right]", normalized)
        self.assertIn("$$\n+x", normalized)

    def test_preserves_operators_after_math_has_started(self):
        markdown = r"""
\[
x
-
y
\]
"""

        self.assertEqual(md_helper._normalize_display_math(markdown), markdown)


class ExtractOutlineTests(unittest.TestCase):
    def test_extracts_headings_in_order(self):
        markdown = (
            "## Chapter 1: Foundations\n"
            "Intro text.\n"
            "### 1.1 Basics\n"
            "More text.\n"
            "#### Details\n"
        )

        outline = md_helper.extract_outline(markdown)

        self.assertEqual(
            outline,
            "## Chapter 1: Foundations\n### 1.1 Basics\n#### Details",
        )

    def test_skips_headings_inside_fenced_code_blocks(self):
        markdown = (
            "## Real Heading\n"
            "```python\n"
            "# not a heading, a comment\n"
            "```\n"
            "~~~\n"
            "# also not a heading\n"
            "~~~\n"
            "### Another Real Heading\n"
        )

        outline = md_helper.extract_outline(markdown)

        self.assertEqual(outline, "## Real Heading\n### Another Real Heading")

    def test_respects_max_level(self):
        markdown = "## Title\n### Section\n#### Subsection\n"

        outline = md_helper.extract_outline(markdown, max_level=3)

        self.assertEqual(outline, "## Title\n### Section")

    def test_returns_empty_string_when_no_headings(self):
        self.assertEqual(md_helper.extract_outline("Just prose.\nNo headings."), "")


if __name__ == "__main__":
    unittest.main()
