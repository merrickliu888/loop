import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from utils.sources.source import Source
from utils.ai import summarize

youtube_api_key = os.environ.get("YOUTUBE_API_KEY")

class YoutubeVideo(Source):
    def __init__(self, title: str, id: str, channel: str, thumbnail_url: str, transcript: str = None):
        super().__init__(title, f"https://www.youtube.com/watch?v={id}")
        self.id = id
        self.channel = channel
        self.thumbnail_url = thumbnail_url
        self.transcript = transcript

def get_content_from_youtube(query: str) -> list[Source]:
    videos = get_youtube_videos(query)
    get_transcripts(videos)
    for v in videos:
        v.summary = summarize(v.transcript)
    return videos
        
def create_youtube_client():
    return build("youtube", "v3", developerKey=youtube_api_key)

def get_youtube_videos(query: str) -> list[YoutubeVideo]:
    youtube = create_youtube_client()
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=5
    )
    response = request.execute()
    return [YoutubeVideo(item['snippet']['title'], item['id']['videoId'], item["snippet"]["channelTitle"], item["snippet"]["thumbnails"]) for item in response["items"]]

def process_transcript(transcript: list[dict], limit: int = None) -> str:
    if limit:
        return " ".join([t["text"] for t in transcript[:limit]])
    else: 
        return " ".join([t["text"] for t in transcript])

def get_transcripts(videos: list[YoutubeVideo]) -> list[YoutubeVideo]:
    """
    TODO Note some videos could not have transcripts
    """
    try:
        unprocessed_transcripts, unretrievable_transcripts = YouTubeTranscriptApi.get_transcripts([vid.id for vid in videos])
        for vid in videos:
            if vid.id not in unretrievable_transcripts:
                vid.transcript = process_transcript(unprocessed_transcripts[vid.id], 100)
        return videos
    except Exception as e:
        raise Exception("Failed to get transcripts") from e

