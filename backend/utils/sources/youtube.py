import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

youtube_api_key = os.environ.get("YOUTUBE_API_KEY")

class YoutubeVideo:
    def __init__(self, title: str, id: str, channel: str, thumbnail_url: str, transcript: str = None) -> None:
        self.title = title
        self.id = id
        self.video_url = f"https://www.youtube.com/watch?v={id}"
        self.channel = channel
        self.thumbnail_url = thumbnail_url
        self.transcript = transcript
        
def create_youtube_client():
    return build("youtube", "v3", developerKey=youtube_api_key)

def get_youtube_videos(query: str):
    youtube = create_youtube_client()
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=5
    )
    response = request.execute()
    return [YoutubeVideo(item['snippet']['title'], item['id']['videoId'], item["snippet"]["channelTitle"], item["snippet"]["thumbnails"]) for item in response["items"]]

def process_transcript(transcript: list[dict]):
    """
    TODO Don't need to process the whole video, so maybe limit
    """
    return " ".join([t["text"] for t in transcript])

def get_transcripts(videos: list[YoutubeVideo]):
    """
    TODO Note some videos could not have transcripts
    """
    try:
        unprocessed_transcripts, unretrievable_transcripts = YouTubeTranscriptApi.get_transcripts([vid.id for vid in videos])
        for vid in videos:
            if vid.id not in unretrievable_transcripts:
                vid.transcript = process_transcript(unprocessed_transcripts[vid.id])
        return videos
    except Exception as e:
        raise Exception("Failed to get transcripts") from e

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    print(youtube_api_key)
    videos = get_youtube_videos("python programming")
    print([videos[i].video_url for i in range(len(videos))])
    get_transcripts(videos)
    print([videos[i].transcript for i in range(len(videos))])
