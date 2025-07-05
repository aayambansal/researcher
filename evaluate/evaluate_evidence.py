import json
from pathlib import Path
from typing import List

from ai_researcher.evidence_reviewer import EvidenceReviewer


def evaluate(papers: List[str], api_key: str | None = None):
    reviewer = EvidenceReviewer()
    results = []
    for paper in papers:
        rev = reviewer.evaluate(paper, api_key=api_key)[0]
        broken = [v for v in rev.get("citation_evidence", []) if v["verdict"] == "broken"]
        results.append(len(broken))
    return sum(results) / len(papers) if papers else 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="Path to JSON list of paper texts")
    parser.add_argument("--api_key")
    args = parser.parse_args()

    papers = json.loads(Path(args.data).read_text())
    rate = evaluate(papers, api_key=args.api_key)
    print(json.dumps({"broken_rate": rate}, indent=2))
