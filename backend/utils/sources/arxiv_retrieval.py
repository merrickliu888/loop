import arxiv
from utils.sources.source import Source
from utils.ai import summarize

class ResearchPaper(Source):
    def __init__(self, title: str, abstract: str, authors, pdf_url: str, abs_url: str):
        super().__init__(title, pdf_url)
        self.abstract = abstract
        self.authors = authors
        self.abs_url = abs_url

def get_content_from_arxiv(query: str) -> list[Source]:
    papers = get_arvix_papers(query)
    for p in papers:
        p.summary = summarize(p.abstract)
    return papers

def create_arxiv_client():
    return arxiv.Client()

def get_arvix_papers(query: str) -> list[ResearchPaper]:
    arxiv_client = create_arxiv_client()
    search = arxiv.Search(query=query, max_results=3)
    results = arxiv_client.results(search)
    return [ResearchPaper(result.title, result.summary, result.authors, result.pdf_url, result.entry_id) for result in results]
