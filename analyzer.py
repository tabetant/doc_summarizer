import json
import os

import anthropic
from rich.console import Console

if not os.environ.get("ANTHROPIC_API_KEY"):
    raise EnvironmentError(
        "ANTHROPIC_API_KEY is not set. Export it in your shell before running."
    )

_err = Console(stderr=True)

_SYSTEM_PROMPT = (
    "You are a business document analyst. Your job is to read a document and extract "
    "structured information from it. You must respond with valid JSON only — no markdown "
    "code fences, no explanation, no preamble. Your response must be a single JSON object."
)

_USER_PROMPT_TEMPLATE = """\
Analyze the following business document and return a JSON object with exactly these four keys:

"summary": A 3 to 5 sentence plain-English overview of the document's purpose and main content.

"action_items": A JSON array of objects. Each object has:
  - "task": string describing the action required
  - "owner": string with the person or team responsible, or null if not mentioned
  - "deadline": string with the deadline or timeframe, or null if not mentioned

"key_decisions": A JSON array of strings. Each string is one decision or conclusion that \
was made or established in the document.

"open_questions": A JSON array of strings. Each string is one unresolved issue, open question, \
or item flagged for follow-up.

If a section has no relevant content, use an empty array [] for arrays or an empty string "" \
for the summary.

Document:
---
{document_text}
---"""

_MAX_CHARS = 180_000


class AnalyzerError(Exception):
    pass


def analyze_document(document_text: str) -> dict:
    if len(document_text) > _MAX_CHARS:
        _err.print(
            f"[yellow]Warning: document is {len(document_text):,} characters — "
            f"truncating to {_MAX_CHARS:,} for analysis.[/yellow]"
        )
        document_text = document_text[:_MAX_CHARS] + "\n\n[Document truncated for length]"

    user_message = _USER_PROMPT_TEMPLATE.format(document_text=document_text)

    client = anthropic.Anthropic()
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            system=_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": "{"},
            ],
        )
    except anthropic.APIError as e:
        raise AnalyzerError(f"Claude API error: {e}") from e

    raw = "{" + response.content[0].text

    # Fallback: strip markdown fences if prefill somehow didn't prevent them
    if raw.strip().startswith("```"):
        raw = raw.strip().lstrip("`").lstrip("json").strip()
        if raw.endswith("```"):
            raw = raw[:-3].strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        raise AnalyzerError(
            f"Claude returned invalid JSON: {e}\nRaw response (first 500 chars): {raw[:500]}"
        ) from e

    return result
