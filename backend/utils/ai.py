from utils.sources import sources as source_list

def create_search_query() -> str:
    """
    Creates a search query
    """
    pass

def summarize() -> str:
    """Summarizes text"""
    pass

def relevant_sources(query: str, k: int = 6, sources: list[str] = source_list) -> list[str]:
    """
    Returns relevant mediums to answer query
    """
    pass 