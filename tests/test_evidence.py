import pytest
try:
    from ai_researcher.evidence_reviewer import EvidenceReviewer
    from ai_researcher.utils import retrieval
except Exception as e:  # pragma: no cover - optional deps may be missing
    pytest.skip(str(e), allow_module_level=True)


def test_citation_flag(monkeypatch):
    sample_text = "This cites prior work \\cite{Smith2020}."

    def fake_search(query, limit=5, api_key=None):
        return [{"title": "Smith2020", "abstract": "", "year": 2020, "citationCount": 1, "doi": "10.1/xyz"}]

    monkeypatch.setattr(retrieval, "search_papers", fake_search)
    reviewer = EvidenceReviewer()
    verdicts = reviewer.verify_citations(sample_text)
    assert verdicts and verdicts[0]["verdict"] in {"valid", "dubious", "broken"}
