import os
import yagmail
from utils.db import create_supabase_client
from utils.ai import create_search_query, summarize
from utils.sources.youtube import get_youtube_videos, get_transcripts
from utils.sources.arxiv_retrieval import get_arvix_papers

email = os.environ.get("EMAIL")
password = os.environ.get("EMAIL_PASSWORD")

class Content: # TODO make all sources inherit from this
    def __init__(self, title: str, summary: dict, url: str):
        self.title = title
        self.summary = summary
        self.url = url

def create_email_body(recipient_email: str) -> str:
    supabase_cleint = create_supabase_client()

    # Get topic of interest from supabase
    topic = supabase_cleint.table("subscribers").select("topic").eq("email", recipient_email).execute().get("data")[0]
    
    sources = {
        "Youtube": [],
        "Arxiv": []
    }

    # Youtube
    youtube_query = create_search_query(topic, "To learn", "Youtube")
    videos = get_youtube_videos(youtube_query)
    get_transcripts(videos)
    for vid in videos:
        sources["Youtube"].append(Content(vid.title, summarize(vid.transcript), vid.video_url))

    # Use cohere to come up with search query based on topic and source
    arxiv_query = create_search_query(topic, "To learn", "Arxiv")
    papers = get_arvix_papers(arxiv_query)
    for paper in papers:
        sources["Arxiv"].append(Content(paper.title, summarize(paper.abstract), paper.pdf_url))

    # Create HTML for email with content and links
    email_body = email_html(topic, sources)
    return email_body

def send_email(recipient: str, sender: str, body: str, subject: str = "Loop: Daily Content") -> None:
    with yagmail.SMTP(email, password) as email_client:
        email_client.send(
            to=recipient,
            subject=subject,
            contents=body,
            headers={"From": sender}
        )

def email_html(topic: str, sources: dict[str, list[Content]]) -> str:
    content_body = ""
    
    # Loop through content and create list
    for source, documents in sources.items():
        content_body += f"<h2>{source}</h2>"
        content_body += "<ul>"
        for doc in documents:
            content_body += f"<li><a href='{doc.url}'>{doc.title}</a>: {doc.summary}</li>"
        content_body += "</ul>"
    
    return f"""
    <html>
        <head></head>
        <body>
            <h1>Loop</h1>
            <p>Here is some content you might be interested in related to "{topic}":</p>
            {content_body}
        </body>
    </html>
    """
