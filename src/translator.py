"""
Japanese → English translation using Helsinki-NLP/opus-mt-ja-en.

Model is downloaded on first use (~300 MB, cached in ~/.cache/huggingface/).
Requires: sentencepiece (pip install sentencepiece)
"""

from __future__ import annotations

import re

_model = None
_tokenizer = None
_device = None

_JP_RE = re.compile(r"[ぁ-ゟ゠-ヿ一-鿿]")


def _load() -> None:
    global _model, _tokenizer, _device
    if _model is not None:
        return
    import torch
    from transformers import MarianMTModel, MarianTokenizer

    name = "Helsinki-NLP/opus-mt-ja-en"
    print(f"Loading translation model {name} …", flush=True)
    _tokenizer = MarianTokenizer.from_pretrained(name)
    _model = MarianMTModel.from_pretrained(name)
    _model.eval()

    if torch.backends.mps.is_available():
        _device = torch.device("mps")
    elif torch.cuda.is_available():
        _device = torch.device("cuda")
    else:
        _device = torch.device("cpu")

    _model = _model.to(_device)
    print(f"Translation model ready on {_device}.", flush=True)


def needs_translation(text: str) -> bool:
    """Return True if text contains Japanese characters."""
    return bool(_JP_RE.search(text or ""))


def translate_batch(texts: list[str], max_length: int = 256) -> list[str]:
    """Translate Japanese strings to English.  Non-Japanese strings pass through."""
    import torch

    _load()

    results = [""] * len(texts)
    to_translate: list[tuple[int, str]] = []

    for i, t in enumerate(texts):
        if needs_translation(t):
            to_translate.append((i, t))
        else:
            results[i] = t

    if not to_translate:
        return results

    idxs, raw = zip(*to_translate)
    inputs = _tokenizer(
        list(raw),
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=max_length,
    )
    inputs = {k: v.to(_device) for k, v in inputs.items()}

    with torch.no_grad():
        translated_ids = _model.generate(
            **inputs,
            max_length=max_length,
            num_beams=4,
            early_stopping=True,
        )

    decoded = _tokenizer.batch_decode(translated_ids, skip_special_tokens=True)
    for idx, en in zip(idxs, decoded):
        results[idx] = en

    return results


def translate(text: str, max_length: int = 256) -> str:
    return translate_batch([text], max_length=max_length)[0]
