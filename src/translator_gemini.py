"""
Japanese → English translation via Gemini 2.0 Flash.

Batches multiple papers into a single API call (10 papers per call by default)
to stay within the free-tier rate limits (15 req/min, 1,500 req/day).

API key: set GEMINI_API_KEY environment variable, or pass api_key= explicitly.

    from src.translator_gemini import GeminiTranslator
    tr = GeminiTranslator()
    english = tr.translate_batch(["日本語タイトル1", "日本語タイトル2"])
"""

from __future__ import annotations

import json
import os
import re
import time

_JP_RE = re.compile(r"[ぁ-ゟ゠-ヿ一-鿿]")

_SYSTEM_PROMPT = """\
You are a professional academic translator specialising in Japanese scholarly papers.
Translate the given Japanese academic titles/abstracts to English accurately.
- Preserve all technical terms, proper nouns, and abbreviations.
- Do NOT add explanations or notes.
- Return ONLY a valid JSON array of objects with "id" (integer) and "translation" (string).
"""


class GeminiTranslator:
    """Translate Japanese text batches using Gemini 2.0 Flash."""

    def __init__(
        self,
        api_key:    str | None = None,
        model_name: str = "gemini-2.0-flash",
        batch_size: int = 10,
        rpm_limit:  int = 14,   # stay just under the 15 req/min free-tier limit
    ) -> None:
        key = api_key or os.environ.get("GEMINI_API_KEY", "")
        if not key:
            raise ValueError(
                "Set GEMINI_API_KEY environment variable or pass api_key= to GeminiTranslator()"
            )
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("pip install google-generativeai")

        genai.configure(api_key=key)
        self._model      = genai.GenerativeModel(model_name)
        self._batch_size = batch_size
        self._rpm_limit  = rpm_limit
        self._call_times: list[float] = []

    # ------------------------------------------------------------------

    def translate_batch(self, texts: list[str]) -> list[str]:
        """Translate a list of strings. Non-Japanese strings pass through."""
        results = list(texts)  # copy; non-JP entries stay as-is
        to_translate: list[tuple[int, str]] = [
            (i, t) for i, t in enumerate(texts) if _JP_RE.search(t or "")
        ]
        if not to_translate:
            return results

        # Process in batches
        for start in range(0, len(to_translate), self._batch_size):
            batch = to_translate[start : start + self._batch_size]
            translated = self._call_api(batch)
            for idx, en in zip([b[0] for b in batch], translated):
                results[idx] = en

        return results

    def translate(self, text: str) -> str:
        return self.translate_batch([text])[0]

    # ------------------------------------------------------------------

    def _rate_limit(self) -> None:
        """Block if we are approaching the RPM limit."""
        now = time.monotonic()
        self._call_times = [t for t in self._call_times if now - t < 60]
        if len(self._call_times) >= self._rpm_limit:
            sleep_for = 60 - (now - self._call_times[0]) + 0.5
            if sleep_for > 0:
                time.sleep(sleep_for)
        self._call_times.append(time.monotonic())

    def _call_api(self, batch: list[tuple[int, str]]) -> list[str]:
        """Send one Gemini request and return translated strings in order."""
        payload = [{"id": i, "text": t} for i, (_, t) in enumerate(batch)]
        prompt = (
            _SYSTEM_PROMPT
            + "\n\nTranslate these academic texts:\n"
            + json.dumps(payload, ensure_ascii=False, indent=2)
        )

        self._rate_limit()
        for attempt in range(3):
            try:
                response = self._model.generate_content(prompt)
                raw = response.text.strip()
                # Strip markdown code fences if present
                raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()
                items = json.loads(raw)
                # Build ordered list
                lookup = {item["id"]: item["translation"] for item in items}
                return [lookup.get(i, batch[i][1]) for i in range(len(batch))]
            except Exception as e:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                else:
                    # On final failure return originals
                    print(f"  [warn] Gemini translation failed: {e}", flush=True)
                    return [t for (_, t) in batch]
        return [t for (_, t) in batch]
