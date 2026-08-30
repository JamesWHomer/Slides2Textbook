import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from slides2textbook import llm_tools
from slides2textbook.llm_classes import ModelProvider


class WaitForOpenAIResponseTests(unittest.TestCase):
    @patch("slides2textbook.llm_tools.time.sleep")
    @patch("slides2textbook.llm_tools._openai_client")
    def test_polls_until_response_completes(self, openai_client, sleep):
        queued = SimpleNamespace(
            id="resp_123",
            status="queued",
            error=None,
            incomplete_details=None,
        )
        in_progress = SimpleNamespace(
            id="resp_123",
            status="in_progress",
            error=None,
            incomplete_details=None,
        )
        completed = SimpleNamespace(
            id="resp_123",
            status="completed",
            error=None,
            incomplete_details=None,
        )
        responses = MagicMock()
        responses.retrieve.side_effect = [in_progress, completed]
        openai_client.return_value.responses = responses

        result = llm_tools._wait_for_openai_response(queued)

        self.assertIs(result, completed)
        self.assertEqual(responses.retrieve.call_count, 2)
        self.assertEqual(sleep.call_count, 2)
        sleep.assert_called_with(llm_tools.OPENAI_POLL_INTERVAL_SECONDS)

    @patch("slides2textbook.llm_tools.time.sleep")
    def test_raises_for_failed_response(self, sleep):
        failed = SimpleNamespace(
            id="resp_failed",
            status="failed",
            error={"code": "server_error", "message": "generation failed"},
            incomplete_details=None,
        )

        with self.assertRaisesRegex(
            RuntimeError,
            "resp_failed.*status='failed'.*generation failed",
        ):
            llm_tools._wait_for_openai_response(failed)

        sleep.assert_not_called()


class GenerateOpenAITests(unittest.TestCase):
    @patch("slides2textbook.llm_tools.TokenCount.add_openai")
    @patch("slides2textbook.llm_tools._wait_for_openai_response")
    @patch("slides2textbook.llm_tools._openai_client")
    def test_creates_background_stored_response(
        self,
        openai_client,
        wait_for_response,
        add_openai,
    ):
        initial = SimpleNamespace(id="resp_123", status="queued")
        usage = object()
        completed = SimpleNamespace(
            id="resp_123",
            status="completed",
            usage=usage,
            output_text="Generated chapter",
        )
        openai_client.return_value.responses.create.return_value = initial
        wait_for_response.return_value = completed

        result = llm_tools.generate_openai(
            "developer instructions",
            "chapter context",
            model="gpt-test",
            effort="high",
        )

        openai_client.return_value.responses.create.assert_called_once_with(
            model="gpt-test",
            reasoning={"effort": "high"},
            instructions="developer instructions",
            input="chapter context",
            background=True,
            store=True,
        )
        wait_for_response.assert_called_once_with(initial)
        add_openai.assert_called_once_with(usage)
        self.assertEqual(result.output_text, "Generated chapter")


class DetermineProviderAndModelTests(unittest.TestCase):
    def test_prefixed_providers(self):
        self.assertIs(llm_tools.determine_provider("openai/gpt-5.4"), ModelProvider.OPENAI)
        self.assertIs(llm_tools.determine_provider("gemini/gemini-3.0-flash"), ModelProvider.GEMINI)
        self.assertIs(llm_tools.determine_provider("google/gemini-3.0-flash"), ModelProvider.GEMINI)
        self.assertIs(
            llm_tools.determine_provider("openrouter/openai/gpt-5.4"),
            ModelProvider.OPENROUTER,
        )

    def test_determine_model_strips_only_provider_prefix(self):
        self.assertEqual(llm_tools.determine_model("openai/gpt-5.4"), "gpt-5.4")
        self.assertEqual(
            llm_tools.determine_model("openrouter/openai/gpt-5.4"),
            "openai/gpt-5.4",
        )
        self.assertEqual(llm_tools.determine_model("gpt-5.4"), "gpt-5.4")


def _openrouter_completion(content="Generated chapter", usage=None):
    return SimpleNamespace(
        id="gen-123",
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        usage=usage,
    )


class GenerateOpenRouterTests(unittest.TestCase):
    @patch("slides2textbook.llm_tools._openrouter_client")
    def test_sends_chat_completion_with_reasoning(self, openrouter_client):
        usage = SimpleNamespace(
            prompt_tokens=10,
            completion_tokens=20,
            prompt_tokens_details=SimpleNamespace(cached_tokens=4),
            completion_tokens_details=SimpleNamespace(reasoning_tokens=6),
        )
        create = openrouter_client.return_value.chat.completions.create
        create.return_value = _openrouter_completion(usage=usage)

        result = llm_tools.generate_openrouter(
            "developer instructions",
            "chapter context",
            model="openai/gpt-5.4",
            effort="high",
        )

        create.assert_called_once_with(
            model="openai/gpt-5.4",
            messages=[
                {"role": "system", "content": "developer instructions"},
                {"role": "user", "content": "chapter context"},
            ],
            extra_body={"reasoning": {"effort": "high"}},
        )
        self.assertEqual(result.output_text, "Generated chapter")
        self.assertEqual(result.token_count.input_tokens, 10)
        self.assertEqual(result.token_count.cached_tokens, 4)
        self.assertEqual(result.token_count.output_tokens, 20)
        self.assertEqual(result.token_count.reasoning_tokens, 6)

    @patch("slides2textbook.llm_tools._openrouter_client")
    def test_omits_reasoning_without_effort(self, openrouter_client):
        create = openrouter_client.return_value.chat.completions.create
        create.return_value = _openrouter_completion()

        llm_tools.generate_openrouter("dev", "user", model="openai/gpt-5.4")

        self.assertIsNone(create.call_args.kwargs["extra_body"])

    @patch("slides2textbook.llm_tools._openrouter_client")
    def test_raises_when_response_has_no_text(self, openrouter_client):
        create = openrouter_client.return_value.chat.completions.create
        create.return_value = _openrouter_completion(content=None)

        with self.assertRaisesRegex(RuntimeError, "gen-123.*did not include text output"):
            llm_tools.generate_openrouter("dev", "user", model="openai/gpt-5.4")

    @patch("slides2textbook.llm_tools._openrouter_client")
    def test_generate_dispatches_openrouter_models(self, openrouter_client):
        create = openrouter_client.return_value.chat.completions.create
        create.return_value = _openrouter_completion()

        result = llm_tools.generate("dev", "user", model_str="openrouter/openai/gpt-5.4")

        self.assertEqual(create.call_args.kwargs["model"], "openai/gpt-5.4")
        self.assertEqual(result.output_text, "Generated chapter")


if __name__ == "__main__":
    unittest.main()
