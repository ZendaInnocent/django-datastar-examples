"""
Search service module for Django Datastar Examples.

This module provides the search API using Django Q objects (via QEntry)
for filtering and relevance ranking.
"""

from typing import List, Dict, Any

from examples.search import SearchIndex, get_search_index, rebuild_search_index


def search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Execute search query and return formatted results.

    Uses Django QEntry objects (extends Q) for flexible filtering with
    relevance ranking (title > description > content).

    Args:
        query: Search query string
        limit: Maximum number of results to return

    Returns:
        List of dictionaries containing search results with keys:
        - title: Entry title
        - description: Entry description
        - url: Target URL
        - category: Category badge text
        - type: "example" or "doc"
    """
    index = get_search_index()
    return index.search(query, limit)


def get_all_examples() -> List[Dict[str, Any]]:
    """Get all indexed examples."""
    index = get_search_index()
    return [entry.to_dict() for entry in index.entries if entry.type == 'example']


def get_all_docs() -> List[Dict[str, Any]]:
    """Get all indexed documentation."""
    index = get_search_index()
    return [entry.to_dict() for entry in index.entries if entry.type == 'doc']


def get_index_stats() -> Dict[str, int]:
    """Get search index statistics."""
    index = get_search_index()
    examples = [e for e in index.entries if e.type == 'example']
    docs = [e for e in index.entries if e.type == 'doc']

    return {
        'total_entries': len(index.entries),
        'examples_count': len(examples),
        'docs_count': len(docs),
    }


def rebuild_index() -> SearchIndex:
    """
    Rebuild the search index.

    Returns:
        The rebuilt SearchIndex instance
    """
    return rebuild_search_index()
