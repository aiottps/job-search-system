from typing import List, Dict, Any

class CitationBuilder:
    def __init__(self):
        self.citations = {}

    def add_citation(self, citation: Dict[str, Any]):
        if not citation:
            return
        c_id = citation.get("citation_id")
        if c_id and c_id not in self.citations:
            # Ensure no secrets (basic check)
            content = citation.get("content", "")
            if any(secret in content for secret in ["API_KEY", "PASSWORD", "TOKEN"]):
                return
            self.citations[c_id] = citation

    def get_citations(self) -> List[Dict[str, Any]]:
        return list(self.citations.values())

    def clear(self):
        self.citations = {}
