from __future__ import annotations

from typing import List, Dict, Any
from .deep_reviewer import DeepReviewer
from .utils.cite_parse import extract_citations
from .utils.retrieval import search_papers


class EvidenceReviewer(DeepReviewer):
    """DeepReviewer with citation verification."""

    def verify_citations(self, text: str, api_key: str | None = None, top_k: int = 3) -> List[Dict[str, Any]]:
        citations = extract_citations(text)
        verdicts = []
        for cite_key, sentence in citations:
            papers = search_papers(cite_key, limit=top_k, api_key=api_key)
            if not papers:
                verdicts.append({
                    "citation": cite_key,
                    "verdict": "broken",
                    "confidence": 0.0,
                    "suggestion": "Reference not found",
                })
                continue
            # compute similarity naive: exact title match to sentence, else dubious
            match = papers[0]
            title = match.get("title", "")
            if title and title.lower() in sentence.lower():
                verdict = "valid"
                conf = 1.0
            else:
                verdict = "dubious"
                conf = 0.5
            verdicts.append({
                "citation": cite_key,
                "verdict": verdict,
                "confidence": conf,
                "suggestion": match.get("title", "") or "Check reference",
            })
        return verdicts

    def evaluate(self, paper_context, mode: str = "Standard Mode", reviewer_num: int = 4, max_tokens: int = 35000, api_key: str | None = None):
        reviews = super().evaluate(paper_context, mode=mode, reviewer_num=reviewer_num, max_tokens=max_tokens)
        for review in reviews:
            raw = review.get("raw_text", "")
            review["citation_evidence"] = self.verify_citations(raw, api_key=api_key)
        return reviews
