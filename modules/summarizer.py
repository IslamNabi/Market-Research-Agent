from typing import List, Dict
from config import client
import json


class Summarizer:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def extract_structured(self, raw_results: List[Dict]) -> List[Dict]:
        """
        Extract structured JSON data (name, description, sector, founded_year, website, notes)
        from raw Google CSE search results using the AI model.
        """
        content = (
            "Extract JSON objects for each of the following search results. "
            "For each result return: name, description, sector (if known), founded_year (if known), "
            "website, notes. If unknown use null. Return only a JSON array, no extra text.\n\nResults:\n"
        )

        for r in raw_results:
            content += (
                f"- Title: {r.get('title')}\n"
                f"  Snippet: {r.get('snippet')}\n"
                f"  Link: {r.get('link')}\n\n"
            )

        resp = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": content}],
            max_tokens=800,
            temperature=0.0,
        )

        text = resp.choices[0].message.content.strip()

        # Robust JSON extraction
        try:
            start = text.find("[")
            end = text.rfind("]") + 1
            return json.loads(text[start:end])
        except Exception:
            # Fallback to basic mapping if AI output is not valid JSON
            return [
                {
                    "name": r.get("title"),
                    "description": r.get("snippet"),
                    "sector": None,
                    "founded_year": None,
                    "website": r.get("link"),
                    "notes": "",
                }
                for r in raw_results
            ]

    def summarize_market(self, structured_list: List[Dict]) -> str:
        """
        Produce a textual market research summary from structured data.
        """
        text = "\n".join(
            [
                f"Name: {s.get('name')}, Sector: {s.get('sector')}, Founded: {s.get('founded_year')} -- {s.get('description')}"
                for s in structured_list
            ]
        )

        prompt = (
            "Write a professional market research summary using these entries. "
            "Highlight trends, notable companies, and quick recommendations.\n\n" + text
        )

        resp = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.2,
        )

        return resp.choices[0].message.content
