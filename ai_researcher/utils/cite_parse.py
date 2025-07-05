import re
from typing import List, Tuple

CITE_REGEX = re.compile(r"\\cite\{([^}]+)\}")
BRACKET_REGEX = re.compile(r"\[(\d+)\]")


def extract_citations(text: str) -> List[Tuple[str, str]]:
    """Return list of (key_or_num, surrounding_sentence)."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    results = []
    for sent in sentences:
        for m in CITE_REGEX.finditer(sent):
            results.append((m.group(1), sent.strip()))
        for m in BRACKET_REGEX.finditer(sent):
            results.append((m.group(1), sent.strip()))
    return results
