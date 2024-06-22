import arxiv

class ResearchPaper:
    def __init__(self, title: str, abstract: str, authors, pdf_url: str, abs_url: str) -> None:
        self.title = title
        self.abstract = abstract
        self.authors = authors
        self.pdf_url = pdf_url
        self.abs_url = abs_url

def create_arxiv_client():
    return arxiv.Client()

def get_arvix_papers(query: str):
    arxiv_client = create_arxiv_client()
    search = arxiv.Search(query=query, max_results=5)
    results = arxiv_client.results(search)
    return [ResearchPaper(result.title, result.summary, result.authors, result.pdf_url, result.entry_id) for result in results]

if __name__ == "__main__":
    papers = get_arvix_papers("transformers")
    print([papers[i].pdf_url for i in range(len(papers))])

