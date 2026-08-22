"""
Japanese → English translation using staka/fugumt-ja-en.

FuguMT is a MarianMT-based model specifically trained for Japanese,
offering significantly better quality than Helsinki-NLP/opus-mt-ja-en
on academic and technical text.

Model size: ~300 MB (same architecture as OPUS-MT).
"""

from __future__ import annotations

import re

_JP_RE = re.compile(r"[ぁ-ゟ゠-ヿ一-鿿]")

_model = None
_tokenizer = None
_device = None


def _load() -> None:
    global _model, _tokenizer, _device
    if _model is not None:
        return
    import torch
    from transformers import MarianMTModel, MarianTokenizer

    name = "staka/fugumt-ja-en"
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
    print(f"FuguMT ready on {_device}.", flush=True)


def needs_translation(text: str) -> bool:
    return bool(_JP_RE.search(text or ""))


def translate_batch(texts: list[str], max_length: int = 256) -> list[str]:
    """Translate Japanese strings to English. Non-Japanese strings pass through."""
    import torch

    _load()
    results = list(texts)
    to_translate = [(i, t) for i, t in enumerate(texts) if needs_translation(t)]

    if not to_translate:
        return results

    idxs, raw = zip(*to_translate)
    inputs = _tokenizer(
        list(raw),
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=max_length,
    ).to(_device)

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
