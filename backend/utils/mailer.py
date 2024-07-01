import os
import yagmail
from utils.db import create_supabase_client
from utils.ai import create_search_query
from utils.sources.source import Source
from utils.sources.youtube import get_content_from_youtube
from utils.sources.arxiv_retrieval import get_content_from_arxiv

email = os.environ.get("EMAIL")
password = os.environ.get("EMAIL_PASSWORD")

def send_email(recipient: str, body: str, subject: str = "Loop: Daily Content") -> None:
    with yagmail.SMTP(email, password) as email_client:
        email_client.send(
            to=recipient,
            subject=subject,
            contents=body,
            headers={"From": email}
        )

def create_email_body(recipient_email: str) -> str:
    supabase_client = create_supabase_client()

    # Get topic of interest from supabase
    topic = supabase_client.table("subscribers").select("topic").eq("email_address", recipient_email).execute().data[0]["topic"]

    sources = dict()
    # youtube_query = create_search_query(topic, "to stay in the loop", "Youtube")
    sources["Youtube"] = get_content_from_youtube(topic)
    # arxiv_query = create_search_query(topic, "to stay in the loop", "Arxiv")
    sources["Arxiv"] = get_content_from_arxiv(topic)

    # Create HTML for email with content and links
    email_body = email_html(topic, sources)
    return email_body

def email_html(topic: str, sources: dict[str, list[Source]]) -> str:
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
