import unittest

from slides2textbook.main import get_chapter_context

CHAPTERS = [
    "## Chapter 1: Intro\n### 1.1 History\nChapter one body.",
    "## Chapter 2: Basics\n### 2.1 Terms\nChapter two body.",
    "## Chapter 3: Advanced\n### 3.1 Theory\nChapter three body.",
]


class GetChapterContextTests(unittest.TestCase):
    def test_first_chapter_includes_title_instructions(self):
        prompt = get_chapter_context("slides", "", 0, [], "My Book")

        self.assertIn("first chapter of the textbook", prompt)
        self.assertIn("My Book", prompt)
        self.assertIn("Current chapter input context:\n\nslides", prompt)

    def test_default_excludes_previous_chapters(self):
        prompt = get_chapter_context("slides", "", 2, CHAPTERS[:2], "My Book")

        self.assertNotIn("Previous chapter", prompt)
        self.assertNotIn("Chapter one body", prompt)
        self.assertNotIn("Chapter two body", prompt)
        self.assertNotIn("first chapter of the textbook", prompt)

    def test_prev_chapters_one_includes_only_latest(self):
        prompt = get_chapter_context(
            "slides", "", 2, CHAPTERS[:2], "My Book", prev_chapters=1
        )

        self.assertIn("Previous chapter:\n", prompt)
        self.assertIn("Chapter two body", prompt)
        self.assertNotIn("Chapter one body", prompt)

    def test_prev_chapters_negative_includes_all(self):
        prompt = get_chapter_context(
            "slides", "", 3, CHAPTERS, "My Book", prev_chapters=-1
        )

        self.assertIn("Previous 3 chapters:\n", prompt)
        for chapter in CHAPTERS:
            self.assertIn(chapter, prompt)

    def test_prev_chapters_larger_than_history_includes_all(self):
        prompt = get_chapter_context(
            "slides", "", 2, CHAPTERS[:2], "My Book", prev_chapters=10
        )

        self.assertIn("Previous 2 chapters:\n", prompt)
        self.assertIn("Chapter one body", prompt)
        self.assertIn("Chapter two body", prompt)

    def test_outline_covers_chapters_not_fully_included(self):
        prompt = get_chapter_context(
            "slides",
            "",
            3,
            CHAPTERS,
            "My Book",
            prev_chapters=1,
            include_outline=True,
        )

        self.assertIn("Outline of earlier chapters", prompt)
        self.assertIn("## Chapter 1: Intro", prompt)
        self.assertIn("### 1.1 History", prompt)
        self.assertIn("## Chapter 2: Basics", prompt)
        self.assertNotIn("Chapter one body", prompt)
        self.assertNotIn("Chapter two body", prompt)
        self.assertIn("Chapter three body", prompt)

    def test_no_outline_when_all_chapters_fully_included(self):
        prompt = get_chapter_context(
            "slides",
            "",
            2,
            CHAPTERS[:2],
            "My Book",
            prev_chapters=-1,
            include_outline=True,
        )

        self.assertNotIn("Outline of earlier chapters", prompt)

    def test_instructions_are_prepended(self):
        prompt = get_chapter_context("slides", "Be concise.", 0, [], "My Book")

        self.assertTrue(prompt.startswith("Whole Textbook Instructions:\nBe concise."))


if __name__ == "__main__":
    unittest.main()
