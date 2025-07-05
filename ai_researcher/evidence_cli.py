import argparse
import json
from pathlib import Path

from pypdf import PdfReader

from .evidence_reviewer import EvidenceReviewer


def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text


def main():
    parser = argparse.ArgumentParser(description="EvidenceReviewer CLI")
    parser.add_argument("--pdf", required=True, help="Path to PDF file")
    parser.add_argument("--mode", default="Standard Mode", help="Review mode")
    parser.add_argument("--api_key", default=None, help="Semantic Scholar API key")
    args = parser.parse_args()

    reviewer = EvidenceReviewer()
    paper_text = load_pdf(args.pdf)
    review = reviewer.evaluate(paper_text, mode=args.mode, api_key=args.api_key)[0]
    print(json.dumps(review, indent=2))


if __name__ == "__main__":
    main()
