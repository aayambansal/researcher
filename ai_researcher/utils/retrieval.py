import json
import requests
import sqlite3
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path(__file__).resolve().parent / "retrieval_cache.db"

# Initialize SQLite database
conn = sqlite3.connect(DB_PATH)
conn.execute(
    "CREATE TABLE IF NOT EXISTS search_cache (query TEXT PRIMARY KEY, response TEXT)"
)
conn.commit()
conn.close()


def search_papers(query: str, limit: int = 5, api_key: str | None = None) -> List[Dict[str, Any]]:
    """Search Semantic Scholar and return minimal paper info with caching."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT response FROM search_cache WHERE query=?", (query,))
    row = cur.fetchone()
    if row:
        data = json.loads(row[0])
        conn.close()
        return data

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,year,citationCount,externalIds",
    }
    headers = {"x-api-key": api_key} if api_key else {}
    resp = requests.get(
        "https://api.semanticscholar.org/graph/v1/paper/search", params=params, headers=headers
    )
    resp.raise_for_status()
    data = resp.json().get("data", [])
    # Minimal normalization
    papers = []
    for p in data:
        papers.append({
            "title": p.get("title"),
            "abstract": p.get("abstract"),
            "year": p.get("year"),
            "citationCount": p.get("citationCount"),
            "doi": p.get("externalIds", {}).get("DOI"),
        })

    cur.execute(
        "INSERT OR REPLACE INTO search_cache(query, response) VALUES (?, ?)",
        (query, json.dumps(papers)),
    )
    conn.commit()
    conn.close()
    return papers
