"""
Utility placeholders for Arxiv, Tavily, Wikipedia, etc.

In a production system, implement concrete tool wrappers here and
wire them into your research agent logic.
"""


def search_arxiv(query: str):
    raise NotImplementedError("Implement Arxiv search integration here.")


def search_wikipedia(query: str):
    raise NotImplementedError("Implement Wikipedia search integration here.")


def search_tavily(query: str):
    raise NotImplementedError("Implement Tavily/web search integration here.")
