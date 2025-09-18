# core/search_client.py
from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 3) -> str:
    """
    Performs a DuckDuckGo web search and returns top results as text.
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(f"{r['title']}: {r['body']} ({r['href']})")
        if not results:
            return "No relevant results found."
        return "\n\n".join(results)
    except Exception as e:
        return f"Web search error: {e}"
